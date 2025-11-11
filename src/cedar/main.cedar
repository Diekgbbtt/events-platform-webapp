// TODO

permit (
    principal is Person in Role::"REGULARUSER",
    action == Action::"addEvent",
    resource is EventsContainer
)

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"analyze",
    resource is Event
)