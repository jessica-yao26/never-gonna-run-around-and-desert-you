from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# from rest_framework.validators import UniqueValidator

# class styloUser(AbstractUser):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	first_name = models.CharField(max_length=20)
# 	last_name = models.CharField(max_length=20)
# 	phone_number = models.CharField(max_length=10, validators=[UniqueValidator(queryset=User.objects.all())])
class User(models.Model):
	email = models.EmailField(unique=True)
	phone_number = models.CharField(unique=True)
	username = models.CharField(unique=True)
	password = models.CharField()
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'username'
	is_anonymous = False
	is_authenticated = True
