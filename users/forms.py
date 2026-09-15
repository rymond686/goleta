from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(max_length=254, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control auth-control"
        self.fields["username"].widget.attrs.update(
            {
                "aria-describedby": "username-help username-errors",
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "Choose a username",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "aria-describedby": "email-help email-errors",
                "autocomplete": "email",
                "placeholder": "you@example.com",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "aria-describedby": "password1-help password1-errors",
                "autocomplete": "new-password",
                "data-password-input": "password",
                "placeholder": "Create a password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "aria-describedby": "password2-help password2-errors",
                "autocomplete": "new-password",
                "data-password-input": "passwordConfirmation",
                "placeholder": "Confirm your password",
            }
        )


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control auth-control"
        self.fields["username"].widget.attrs.update(
            {
                "aria-describedby": "username-errors",
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": "Enter your username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "aria-describedby": "password-errors",
                "autocomplete": "current-password",
                "data-password-input": "loginPassword",
                "placeholder": "Enter your password",
            }
        )
