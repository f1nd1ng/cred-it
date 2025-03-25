from django.contrib.auth.backends import ModelBackend
from backend.models import User

class MultiAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        user = None

        if email:
            user = User.objects.filter(email=email).first()
        elif username:
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user
        return None
