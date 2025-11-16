
// TODO add contextual check principal.active in all policies
permit (
    principal is Person,
    action == Action::"readEventRequesters",
    resource is Event
) when {
    principal.username == context.requesterusr || principal in Role::"ADMIN"
};

permit (
    principal is Person,
    action == Action::"addEvent",
    resource is EventsContainer
) when {
    principal in Role::"REGULARUSER" && context.userEvents < 5 || principal in Role::"PREMIUMUSER"
};

permit (
    principal is Person,
    action == Action::"updateEvent",
    resource is Event
) when {
    principal in Role::"ADMIN" || resource.managedBy.contains(principal)
};

forbid (
    principal is Person,
    action == Action::"demoteManager",
    resource is Event
) when {
    resource.owner == context.demotedManager
};

permit (
    principal is Person,
    action == Action::"demoteManager",
    resource is Event
) when {
    principal in Role::"ADMIN" || resource.owner == principal
};

permit (
    principal is Person,
    action == Action::"promoteAttendant",
    resource is Event
) when {
    principal in Role::"ADMIN" || resource.owner == principal
};

forbid (
    principal is Person,
    action == Action::"removeAttendant",
    resource is Event
) when {
    resource.managedBy.contains(context.removedAttendant)
};

permit (
    principal is Person,
    action == Action::"removeAttendant",
    resource is Event
) when {
    principal in Role::"ADMIN" ||  resource.managedBy.contains(principal) || principal == context.removedAttendant
};

permit (
    principal is Person,
    action in [Action::"acceptRequest", Action::"rejectRequest"],
    resource is Event
) when {
    principal in Role::"ADMIN" ||  resource.managedBy.contains(principal)
};

// user can reject(retire) its own request 
permit (
    principal is Person,
    action == Action::"rejectRequest",
    resource is Event
) when {
    principal == context.rejectedRequester
};

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"analyze",
    resource is Event
);