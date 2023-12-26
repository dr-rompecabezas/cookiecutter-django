from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    """Custom manager for the User model."""

    def _create_user(self, email: str, first_name: str, last_name: str, password: str | None, **extra_fields):
        """
        Create and save a user with the given email, names, and password.
        """
        if not email:
            raise ValueError("The email must be set")
        if not first_name:
            raise ValueError("The first name must be set")
        if not last_name:
            raise ValueError("The last name must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.first_name = first_name
        user.last_name = last_name
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, first_name: str, last_name: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(
        self, email: str, first_name: str, last_name: str, password: str | None = None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, first_name, last_name, password, **extra_fields)
