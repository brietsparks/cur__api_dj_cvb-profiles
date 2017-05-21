import graphene
from profiles.models import Profile as ProfileModel
from .project import ProjectType


class ProfileType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    name = graphene.String()
    projects = graphene.List(ProjectType)

