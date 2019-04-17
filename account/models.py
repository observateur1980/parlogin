from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
	def create_user(self, username, email,  password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			username = username,
			email=self.normalize_email(email),
			
		)
		user.is_active = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			username,
			email,
			password=password,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_adult = True
		user.is_kids = True
		user.is_upload = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	username = models.CharField(
				max_length=120, 
				validators=[
				RegexValidator(
						regex= USERNAME_REGEX,
						message = 'Username must be Alphanumeric',
						code = 'invalide username'
					)], 
				unique = True, 
			)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)


	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_adult = models.BooleanField(default=False)
	is_kids = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_upload = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	