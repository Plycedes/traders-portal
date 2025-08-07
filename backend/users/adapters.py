from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email

        if request.user.is_authenticated:
            return

        try:
            existing_user = User.objects.get(email=email)
            
            if not existing_user.socialaccount_set.exists():
                raise ImmediateHttpResponse(JsonResponse({
                    "error": "An account already exists with this email. Please login using your email and password."
                }, status=400))

        except User.DoesNotExist:
            pass 
