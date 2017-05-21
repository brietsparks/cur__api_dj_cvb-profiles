from django_neomodel import DjangoNode
from neomodel import (
    StringProperty, UniqueIdProperty, IntegerProperty, EmailProperty,
    StructuredRel, RelationshipFrom, RelationshipTo,
    One
)


class BelongsToProfile(StructuredRel):
    rel_name = 'BELONGS_TO_PROFILE'


class HasEmailAddress(StructuredRel):
    rel_name = 'HAS_EMAIL_ADDRESS'


class HasChildProject(StructuredRel):
    rel_name = 'HAS_CHILD_PROJECT'


class HasContribution(StructuredRel):
    rel_name = 'HAS_CONTRIBUTION'


PROFILE_MODEL = 'profiles.models.Profile'
EMAIL_ADDRESS_MODEL = 'profiles.models.EmailAddress'
PROJECT_MODEL = 'profiles.models.Project'
CONTRIBUTION_MODEL = 'profiles.models.Contribution'


class Profile(DjangoNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    userId = IntegerProperty()

    projects = RelationshipFrom(PROJECT_MODEL, BelongsToProfile.rel_name, model=BelongsToProfile)

    contributions = RelationshipFrom(CONTRIBUTION_MODEL, BelongsToProfile.rel_name, model=BelongsToProfile)

    class Meta:
        app_label = 'profiles'


class EmailAddress(DjangoNode):
    uuid = UniqueIdProperty()
    value = EmailProperty()

    profile = RelationshipFrom(PROFILE_MODEL, HasEmailAddress.rel_name, model=HasEmailAddress)


class Project(DjangoNode):
    uuid = UniqueIdProperty()
    title = StringProperty(required=True)
    summary = StringProperty()

    profile = RelationshipTo(PROFILE_MODEL, BelongsToProfile.rel_name, model=BelongsToProfile, cardinality=One)

    parent_project = RelationshipFrom(PROJECT_MODEL, HasChildProject.rel_name, model=HasChildProject, cardinality=One)
    child_projects = RelationshipTo(PROJECT_MODEL, HasChildProject.rel_name, model=HasChildProject)
    contributions = RelationshipTo(CONTRIBUTION_MODEL, HasContribution.rel_name, model=HasContribution)

    class Meta:
        app_label = 'profiles'


class Contribution(DjangoNode):
    uuid = UniqueIdProperty()
    title = StringProperty(required=True)
    summary = StringProperty()

    profile = RelationshipTo(PROFILE_MODEL, BelongsToProfile.rel_name, model=BelongsToProfile, cardinality=One)
    parent_project = RelationshipFrom(PROJECT_MODEL, HasContribution.rel_name, model=HasContribution, cardinality=One)

    class Meta:
        app_label = 'profiles'
