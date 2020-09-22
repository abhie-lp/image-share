from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Authentication using email address.
    """
    @staticmethod
    def authenticate(request, username, password):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
