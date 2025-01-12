from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField

# Custom manager to handle User creation logic
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        # Normalize email and create a user instance
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save the user
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # Set admin flags
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)  # Fixed typo ('eamil' → 'email')
    phone_number = models.CharField(max_length=12, blank=True)  # Fixed typo ('maxlength' → 'max_length')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)  # Fixed typo ('choice' → 'choices')

    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Specifies email for authentication
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Fields required for superuser creation

    objects = UserManager()  # Connect the custom manager

    def __str__(self):
        return self.email  # Fixed: Correctly return the email attribute

    def has_perm(self, perm, obj=None):  # Permissions method
        return self.is_admin

    def has_module_perms(self, app_label):  # Module-level permissions
        return True

# UserProfile model for additional user details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Fixed: Removed 'blank=True, null=True' to enforce OneToOne integrity
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)  # Fixed: Changed from CharField to FloatField for numeric values
    longitude = models.FloatField(blank=True, null=True)  # Fixed: Changed from CharField to FloatField for numeric values
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email