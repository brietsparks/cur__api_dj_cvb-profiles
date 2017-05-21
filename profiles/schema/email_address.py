import graphene
from profiles.models import EmailAddress as EmailAddressModel


# todo: design to prevent circular refs
class EmailAddressType(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    value = graphene.String(required=True)
    profile = graphene.Field('profiles.schema.profile.ProfileType')


class EmailAddressQuery(graphene.AbstractType):
    email_address = graphene.Field(EmailAddressType, value=graphene.String(required=True))

    def resolve_email_address(self, args, context, info):
        value = args.get('value')
        return EmailAddressModel.nodes.get_or_none(value=value)

