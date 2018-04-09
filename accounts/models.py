from django.db import models
# from django.contrib.auth.models import UserManager
# from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# from rest_framework.validators import UniqueValidator

# class styloUser(AbstractUser):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	first_name = models.CharField(max_length=20)
# 	last_name = models.CharField(max_length=20)
# 	phone_number = models.CharField(max_length=10, validators=[UniqueValidator(queryset=User.objects.all())])
class UserManager(BaseUserManager):
    def create_user(self, email, username, password, first_name, last_name):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
	email = models.EmailField(unique=True, max_length=255)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	username = models.CharField(unique=True, max_length=20)
	password = models.CharField(max_length=255)
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'username'
	is_anonymous = False
	is_authenticated = True
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	# user = User.objects.create_user(username=form.cleaned_data['username'],
 #                                password=form.cleaned_data['password'], 
 #                                email=form.cleaned_data['email'],
 #                                first_name=form.cleaned_data['first_name'],
 #                                last_name=form.cleaned_data['last_name'])
	# user.save()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin