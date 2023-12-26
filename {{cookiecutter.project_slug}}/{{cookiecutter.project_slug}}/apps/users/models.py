from django.contrib.auth.models import AbstractUser
from django.db.models import CharField{% if cookiecutter.username_type == "email" %}, EmailField{% endif %}
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
{%- if cookiecutter.username_type == "email" %}

from {{ cookiecutter.project_slug }}.apps.users.managers import UserManager
{%- endif %}


class User(AbstractUser):
    """
    Default custom user model for {{cookiecutter.project_name}}.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    {%- if cookiecutter.username_type == "email" %}
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    {%- endif %}
    REQUIRED_FIELDS = ["first_name", "last_name"]

    {%- if cookiecutter.username_type == "email" %}
    objects = UserManager()
    {%- endif %}

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        {%- if cookiecutter.username_type == "email" %}
        return reverse("users:detail", kwargs={"pk": self.pk})
        {%- else %}
        return reverse("users:detail", kwargs={"username": self.username})
        {%- endif %}
