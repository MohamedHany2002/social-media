
from django.contrib.auth.models import User
class EmailAuthBackend:

    def authenticate(self,request,email=None,password=None):
        try:
            user=User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            user=User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
            


