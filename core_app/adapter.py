from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Auto connect existing accounts by email to strictly bypass the intermediate form
        user = sociallogin.user
        if user.id:
            return
        if not user.email:
            return
        try:
            existing_user = User.objects.get(email=user.email)
            if not existing_user.is_active:
                existing_user.is_active = True
                existing_user.save()
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
