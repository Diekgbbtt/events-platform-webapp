
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
    principal is Person in Role::"ADMIN",
    action == Action::"analyze",
    resource is Event
);