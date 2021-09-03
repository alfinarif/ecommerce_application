# Custom django default user model class to change permissions
# models class for fields
from django.db import models
# AbstractUser and BaseUserManager to modified default User permission
from django.contrib.auth.models import AbstractUser, BaseUserManager
# post_save signals to creating automatic user profile while user will register
from django.db.models.signals import post_save
from django.dispatch import receiver


# User registration custom manager
class CustomerManager(BaseUserManager):
    use_in_migrations = True
    #this function stand for creating user account via email and password
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Email Address is required!')
        else:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
    #this function stand for creating super user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # condition to check if is not true
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be is_superuser=True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must be is_active=True')

        # return create_user function and pass arguments to create superuser
        return self.create_user(email, password, **extra_fields)


# Custom default user model you can add some extra fields
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomerManager()


# Customer Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images')

    # return user email as a string
    def __str__(self):
        return f"{self.user.email}'s profile"
    # this function stand for if customer will never filled profile information 
    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True
    # it will work to create automatic profile instance while customer register
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    # it will work to save profile objects to database
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()