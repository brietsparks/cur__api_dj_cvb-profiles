from profiles.models import Profile
from profiles.models import EmailAddress


class ProfileManager:
    @staticmethod
    def create_new_profile(email):
        email_address = EmailAddress.nodes.get_or_none(value=email)

        if email_address is None:
            email_address = EmailAddress(value=email).save()

        new_profile = Profile().save()

        new_profile.email_addresses.connect(email_address)

        return new_profile.uuid
