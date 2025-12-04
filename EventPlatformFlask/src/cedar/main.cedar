permit (
    principal is Person,
    action == Action::"readPerson",
    resource is Person
) when {
    principal in Role::"ADMIN" || principal == resource
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
    action == Action::"addAd",
    resource is AdContainer
);

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"addCategory",
    resource is CategoriesContainer
);

permit (
    principal is Person,
    action == Action::"updateEvent",
    resource is Event
) when {
    principal in Role::"ADMIN" || resource.managedBy.contains(principal) || resource.owner == principal
};

permit (
    principal is Person,
    action == Action::"updateUser",
    resource is Person
) when {
    principal in Role::"ADMIN" || principal == resource
};

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"updateUserRole",
    resource is Person
);

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
    principal in Role::"ADMIN" || resource.managedBy.contains(principal) || resource.owner == principal || principal == context.removedAttendant
};

permit (
    principal is Person,
    action == Action::"readEventRequesters",
    resource is Event
) when {
    principal.username == context.requesterusr || principal in Role::"ADMIN"
};

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"readAllLogs",
    resource is LogContainer
);

permit (
    principal is Person,
    action == Action::"readLog",
    resource is Log
) when {
    principal in Role::"ADMIN" || resource.user == principal
};

permit (
    principal is Person,
    action == Action::"readCategorySubscribers",
    resource is Category
) when {
    principal in Role::"ADMIN" || resource.moderators.contains(principal)
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

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"removeAd",
    resource is Ad
);

permit (
    principal is Person,
    action == Action::"removeCategoryModerator",
    resource is Category
) when {
    principal in Role::"ADMIN" || context.removedModerator == principal
};

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"addCategoryModerator",
    resource is Category
);

permit (
    principal is Person,
    action == Action::"removeCategoryEvent",
    resource is Category
) when {
    principal in Role::"ADMIN" || resource has moderators && resource.moderators.contains(principal) || context.eventmanagers.contains(principal)
};

permit (
    principal is Person,
    action == Action::"addCategoryEvent",
    resource is Category
) when {
    principal in Role::"ADMIN" || context.eventmanagers.contains(principal)
};

permit (
    principal is Person,
    action in [Action::"acceptRequest", Action::"rejectRequest"],
    resource is Event
) when {
    principal in Role::"ADMIN" ||  resource.managedBy.contains(principal) || resource.owner == principal
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

permit (
    principal is Person in Role::"ADMIN",
    action == Action::"updateCategory",
    resource is Category
);

permit (
    principal is Person in Role::"MODERATOR",
    action == Action::"moderatorReadEmail",
    resource is Person
) when {
    resource.subscriptions.containsAny(principal.moderates)
};

permit (
    principal is Person in Role::"REGULARUSER",
    action == Action::"createInvite",
    resource is InvitesContainer
);

permit (
    principal is Person,
    action == Action::"setInviteEvent",
    resource is Event
) when {
    resource.owner == principal || resource.managedBy.contains(principal)
};

permit (
    principal is Person,
    action in [Action::"setInviteInvitedBy", Action::"setInviteInvitee"],
    resource is Invite
) when {
    resource has event && (resource.event.owner == principal || resource.event.managedBy.contains(principal))
};

permit (
    principal is Person,
    action == Action::"readEventInvitations",
    resource is Event
) when {
    resource.owner == principal || resource.managedBy.contains(principal)
};

permit (
    principal is Person,
    action == Action::"readPersonInvitations",
    resource is Person
) when {
    principal == resource
};

permit (
    principal is Person,
    action == Action::"readPersonInvites",
    resource is Person
) when {
    principal in Role::"ADMIN" || principal == resource
};

permit (
    principal is Person,
    action == Action::"readInvite",
    resource is Invite
) when {
    resource.invitedBy == principal || resource.invitee == principal || resource has event && (resource.event.owner == principal || resource.event.managedBy.contains(principal))
};

permit (
    principal is Person,
    action == Action::"deleteInvite",
    resource is Invite
) when {
    resource.invitedBy == principal || resource.invitee == principal || resource has event && (resource.event.owner == principal || resource.event.managedBy.contains(principal))
};

permit (
    principal is Person,
    action == Action::"acceptInvite",
    resource is Invite
) when {
    resource.invitee == principal
};

permit (
    principal is Person,
    action == Action::"viewPersonalizedStats",
    resource is Person
) when {
    principal == resource
};
