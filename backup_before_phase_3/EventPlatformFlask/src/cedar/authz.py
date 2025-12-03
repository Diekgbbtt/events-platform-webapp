import datetime
from enum import Enum
from types import NoneType
import cedarpy
from typing import Any, Callable, TypeAlias, TypeVar

from sqlalchemy import null
from sqlalchemy import inspect
from model import db, REGULARUSER, PREMIUMUSER, MODERATOR, ADMIN


ROLE_ORDER: tuple[str, ...] = (REGULARUSER, PREMIUMUSER, MODERATOR, ADMIN)


def _build_role_entities() -> list[dict[str, Any]]:
    """
    Emit the linear role hierarchy:
    REGULARUSER <- PREMIUMUSER
    PREMIUMUSER <- MODERATOR
    PREMIUMUSER <- ADMIN
    """
    entities: list[dict[str, Any]] = []
    for _, role in enumerate(ROLE_ORDER):
        parents = []
        if role == PREMIUMUSER:
            parents.append({"type": "Role", "id": REGULARUSER})
        elif role in (MODERATOR, ADMIN):
            parents.append({"type": "Role", "id": PREMIUMUSER})
        entities.append({"uid": {"type": "Role", "id": role}, "attrs": {}, "parents": parents})
    return entities


class SecurityException(Exception):
    """Exception raised when an action is not authorized by security policy"""

    def __init__(self, msg, page='sec_error.html', params=None):
        self.msg = msg
        self.page = page
        self.params = params or {}


class EntitySerializer:
    """Converts Python objects to Cedar entities for authorization"""

    def __init__(self):
        pass

    def entity_reference(self, subject: object) -> str:
        """
        Convert object to a Cedar entity reference string (UID)

        Format: `EntityType::"object_id"`
        Example: `User::"123"` or `Document::"456"`
        """
        identifier = getattr(subject, "id", getattr(subject, "name", None))
        if identifier is None:
            raise ValueError(f"Cannot generate identifier for {subject}")

        return f"{subject.__class__.__name__}::\"{str(identifier).strip()}\""


    def action_reference(self, action: str) -> str:
        """
        Convert action string to Cedar action reference

        Ensures action has proper `Action::` prefix for Cedar
        """
        return f'Action::"{action}"' if not action.startswith("Action::") else action

    def entity_json(self, subject: object) -> dict[str, Any]:
        """
        Convert object to full Cedar entity JSON for the entity store

        Returns complete entity with UID, attributes, and parents
        """
        attributes = {}
        mapper = inspect(subject).mapper

        for attr in mapper.column_attrs + mapper.relationships:
            k = attr.key
            if k in ["id", "_sa_instance_state", "password", "roles", "logs"]:
                continue
            v = getattr(subject, k)
            
            if isinstance(v, list):
                serialized_value = self._serialize_attribute_values(v)
                # if not len(serialized_value) == 0:
                # attributes[k] = serialized_value

            else: 
                serialized_value = self._serialize_attribute_value(v)
                if serialized_value is None and k in ["email", "gender", "name", "surname"]:
                    serialized_value = ""
                # if serialized_value is not None:
            
            attributes[k] = serialized_value
        
        cedar_type = subject.__class__.__name__
        object_id = str(getattr(subject, "id", getattr(subject, "name", None)))
        parents: list[dict[str, Any]] = []
        if cedar_type == "Person":
            roles = getattr(subject, "roles", None) or []
            seen_roles: set[str] = set()
            append_parent = parents.append
            for role in roles:
                name = getattr(role, "name", None)
                if not name:
                    continue
                normalized = str(name).strip()
                if not normalized or normalized in seen_roles:
                    continue
                seen_roles.add(normalized)
                append_parent({"type": "Role", "id": normalized})


        return {
            "uid": {"type": cedar_type, "id": object_id},
            "attrs": attributes,
            "parents": parents,
        }



    def _serialize_attribute_value(self, value: Any) -> Any | None:
        # DONE here misssing handling of dict lists. both primitive types and classes
        # list of primitive types --> return it, should be JSON encoded (?)
        # list of instances of type db.Model _entity_pointer() for each
        
        # e.g. list of logs, requesters
        if isinstance(value, (int, str, bool, datetime.datetime)):
            return value
        if isinstance(value, dict):
            nested: dict[str, Any] = {}
            for key, nested_value in value.items():
                converted = self._serialize_attribute_value(nested_value)
                if converted is not None:
                    nested[key] = converted
            return nested if nested else None

        if isinstance(value, db.Model):
            return self._entity_pointer(value)

        return None
    
    def _serialize_attribute_values(self, values: list[Any]) -> Any | None:
        serialized_values = []
        for v in values:
            serialized_values.append(self._serialize_attribute_value(v))
        return serialized_values
    
    def _entity_pointer(self, subject: object) -> dict[str, Any]:
        identifier = getattr(subject, "id", getattr(subject, "name", None))
        if identifier is None:
            identifier = str(subject)        
        return {
            "__entity" : {
                "type": subject.__class__.__name__,
                "id": str(identifier).strip()
            }
        }


class CedarClient:
    """Client for making Cedar authorization requests"""

    def __init__(
        self,
        policies: str,
        serializer: EntitySerializer,
        schema: str | None = None,
        verbose: bool = False,
    ):
        """
        Initialize Cedar client

        Args:
            policies: Cedar policy text
            serializer: Entity serializer for converting Python objects
            schema: Optional Cedar schema for validation
            verbose: Enable verbose logging
        """
        self.policies = policies
        self.serializer = serializer
        self.schema = schema
        self.verbose = verbose
        self._static_entities = _build_role_entities()

    def is_authorized(
        self,
        principal: str | object,
        action: str,
        resource: str | object,
        context: dict = {},
        entities: list[str | object] | None = None,
    ) -> cedarpy.AuthzResult:
        """
        Check if principal is authorized to perform action on resource

        Args:
            principal: The entity performing the action (e.g., User object)
            action: The action being performed (e.g., "read", "write")
            resource: The resource being accessed (e.g., Document object)
            entities: Additional entities needed for policy evaluation
            context: Additional information to attach to the request

        Returns:
            Cedar authorization result
        """
        if isinstance(principal, str):
            principal_uid = principal
        else:
            principal_uid = self.serializer.entity_reference(principal)

        if isinstance(resource, str):
            resource_uid = resource
        else:
            resource_uid = self.serializer.entity_reference(resource)

        # By default, include principal and resource in the entity store
        if entities is None:
            entities = []
            if not isinstance(principal, str):
                entities.append(principal)
            if not isinstance(resource, str):
                entities.append(resource)

        # Serialize all entities if they are not dicts already
        entities_json = []
        for entity in entities:
            if isinstance(entity, dict):
                entities_json.append(entity)
            else:
                ent_json = self.serializer.entity_json(entity)
                if ent_json not in entities_json:
                    entities_json.append(ent_json)
        # always add roles entities with hierarchy
        entities_json.extend(self._static_entities)

        # Build and send authorization request
        request = {
            "principal": principal_uid,
            "action": self.serializer.action_reference(action),
            "resource": resource_uid,
            "context": context,
        }
        return cedarpy.is_authorized(
            request, self.policies, entities_json, self.schema, self.verbose
        )

    def assert_allowed(
        self,
        principal: str | object,
        action: str,
        resource: str | object,
        context: dict = {},
        entities: list[object] | None = None,
    ):
        """
        Assert that an action is allowed, raise SecurityException if not

        Convenience method for when you want to fail fast on unauthorized actions
        """
        result = self.is_authorized(principal, action, resource, context, entities)
        if result.decision == cedarpy.Decision.Deny:
            raise SecurityException(
                f"Action '{action}' not allowed for {principal if isinstance(principal, str) else self.serializer.entity_reference(principal)} on {resource if isinstance(resource, str) else self.serializer.entity_reference(resource)}", page='sec_error.html'
            )
        elif result.decision == cedarpy.Decision.NoDecision:
            raise SecurityException(
                f"Failed to decide: action '{action}' for {principal if isinstance(principal, str) else self.serializer.entity_reference(principal)} on {resource if isinstance(resource, str) else self.serializer.entity_reference(resource)}\n{result.diagnostics.errors}", page='sec_error.html'
            )


# Usage example:
"""
# 1. Define your data models (using SQLAlchemy, Django, etc.)
class User:
    def __init__(self, id, username, email, department):
        self.id = id
        self.username = username  
        self.email = email
        self.department = department

class Document:
    def __init__(self, id, title, owner, confidential=False):
        self.id = id
        self.title = title
        self.owner = owner  # User object
        self.confidential = confidential

# 2. Create and configure the serializer
serializer = EntitySerializer()

# Register User type
serializer.register(
    User,                           # Python type
    "User",                        # Cedar entity type  
    lambda u: {                    # Attribute extractor
        "username": u.username,
        "email": u.email,
        "department": u.department
    },
    lambda u: []                   # Parent extractor (empty for users)
)

# Register Document type  
serializer.register(
    Document,
    "Document", 
    lambda d: {
        "title": d.title,
        "confidential": d.confidential,
        "owner": serializer.entity_reference_json(d.owner)  # Reference to owner
    },
    lambda d: []                   # No parent hierarchy for documents
)

# 3. Create Cedar client with policies
cedar_policies = '''
    permit(principal is User, action == Action::"read", resource is Document) 
    when { resource.owner == principal };
    
    permit(principal is User, action == Action::"read", resource is Document)
    when { principal.department == "Admin" };
'''

client = CedarClient(cedar_policies, serializer)

# 4. Use in your application
user = User(1, "alice", "alice@company.com", "Engineering")
document = Document(1, "Secret Plans", user, confidential=True)

# Check authorization
result = client.is_authorized(user, "read", document)
if result.allowed:
    print("Access granted!")
else:
    print("Access denied!")

# Or use assert_allowed for fail-fast behavior
try:
    client.assert_allowed(user, "read", document)
    # Proceed with operation
except SecurityException as e:
    print(f"Security error: {e.msg}")

# You can attach a context and a custom entity store:
client.assert_allowed(user, "read", document
                      # The context stores environemntal information that is 
                      # not strictly about the principal, action or resource
                      context={"in_lockdown_mode": true},
                      # The entity store enables Cedar to access attributes
                      # of entities and evaluate membership predicates ("in")
                      entities=[
                        user, document, another_document, ...
                      ])
"""
