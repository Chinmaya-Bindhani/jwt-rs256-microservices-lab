from django.db import models
from django.contrib.auth.models import PermissionsMixin,BaseUserManager,AbstractBaseUser
#CustomUserManager for CustomUserModel
class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password,**extra):
        if not email:
            raise ValueError("email is not there !")
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra)

# creating a custom user model to keep authentication with email
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.CharField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=100)
    Date_joined = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]


    def __str__(self):
        return  self.username