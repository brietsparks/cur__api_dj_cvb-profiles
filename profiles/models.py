from django_neomodel import DjangoNode
from neomodel import (
    StringProperty, UniqueIdProperty, IntegerProperty,
    StructuredRel, RelationshipFrom, RelationshipTo,
    One
)


class BelongsToProfile(StructuredRel):
    rel_name = 'BELONGS_TO_PROFILE'
    pass


class HasChildProject(StructuredRel):
    rel_name = 'HAS_CHILD_PROJECT'
    pass


class HasContribution(StructuredRel):
    rel_name = 'HAS_CONTRIBUTION'
    pass

PROFILE_MODEL = 'profiles.models.Profile'
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
