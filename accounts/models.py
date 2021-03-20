from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountsManager(BaseUserManager):
    def create_user(self, username, fullname, email, phone_no, date_of_birth, gender, password=None):
        if not username:
            raise ValueError("User must have an username")
        if not email:
            raise ValueError("User must have an email")
        if not fullname:
            raise ValueError("User must have an fullname")
        if not phone_no:
            raise ValueError("User must have an phone number")
        if not date_of_birth:
            raise ValueError("User must have an date of birth")
        if not gender:
            raise ValueError("User must have an gender")

        user = self.model(
            username=username,
            fullname=fullname,
            email=self.normalize_email(email),
            phone_no=phone_no,
            date_of_birth=date_of_birth,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, email, phone_no, date_of_birth, gender, password):
        user = self.create_user(
            username=username,
            fullname=fullname,
            email=self.normalize_email(email),
            phone_no=phone_no,
            date_of_birth=date_of_birth,
            gender=gender,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Accounts(AbstractBaseUser):

    # all fields in accounts table
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="data joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fullname = models.CharField(max_length=60)
    phone_no = models.CharField(max_length=15)
    date_of_birth = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname',
                       'phone_no', 'date_of_birth', 'gender', ]

    objects = MyAccountsManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class OTP(models.Model):
    username = models.CharField(max_length=60, unique=True)
    otp_code = models.CharField(max_length=5)

    def __str__(self):
        return str(self.username)
