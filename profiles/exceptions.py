class ProfilesException(Exception):
    pass


class DoesNotExistError(ProfilesException):
    pass


class RelationshipConstraintError(ProfilesException):
    pass
