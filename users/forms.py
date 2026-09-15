from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "Choose a username",
            }
        )
        self.fields["email"].widget.attrs.update(
            {"autocomplete": "email", "placeholder": "you@example.com"}
        )
        self.fields["password1"].widget.attrs.update(
            {"autocomplete": "new-password", "placeholder": "Create a password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"autocomplete": "new-password", "placeholder": "Confirm your password"}
        )


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "Enter your username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"autocomplete": "current-password", "placeholder": "Enter your password"}
        )
