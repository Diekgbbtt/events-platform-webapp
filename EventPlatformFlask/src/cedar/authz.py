from enum import Enum
import cedarpy
from typing import Any, Callable, TypeAlias, TypeVar


class SecurityException(Exception):
    """Exception raised when an action is not authorized by security policy"""

    def __init__(self, msg):
        self.msg = msg


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
        return ...    # TODO

    def entity_json(self, subject: object) -> dict[str, Any]:
        """
        Convert object to full Cedar entity JSON for the entity store

        Returns complete entity with UID, attributes, and parents
        """
        cedar_type = ...    # TODO
        object_id = ...     # TODO
        attributes = {...}  # TODO
        parents = [...]     # TODO

        return {
            "uid": {"type": cedar_type, "id": object_id},
            "attrs": attributes,
            "parents": parents,
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
            if not isinstance(entity, dict):
                entities_json.append(self.serializer.entity_json(entity))

        # Build and send authorization request
        request = {
            "principal": principal_uid,
            "action": action,
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
                f"Action '{action}' not allowed for {self.serializer.entity_reference(principal)} on {self.serializer.entity_reference(resource)}"
            )
        elif result.decision == cedarpy.Decision.NoDecision:
            raise SecurityException(
                f"Failed to decide: action '{action}' for {self.serializer.entity_reference(principal)} on {self.serializer.entity_reference(resource)}\n{result.diagnostics.errors}"
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
