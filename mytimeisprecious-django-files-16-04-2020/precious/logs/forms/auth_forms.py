from django import forms
from logs.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField


class SignUpForm(forms.ModelForm):

    # captcha = NoReCaptchaField(error_messages={'required': 'Please enter the CAPTCHA'})
    tos = forms.BooleanField(required=True, error_messages={'required': 'You have to agree to the Terms of Service'})

    # email = forms.EmailField(max_length=75, required=True, widget=forms.EmailInput(attrs={'required': 'true'}))

    class Meta:

        model = User
        fields = [
            'username',
            'password',
            'email'
        ]
        error_messages = {
            'username': {
                'required': "Please enter your name",
            },
            'email': {
                'required': "Please enter your e-mail",
            },
            'password': {
                'required': "Please enter your password",
            }
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SignInForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]
        error_messages = {
            'email': {
                'required': "Please enter your e-mail",
            },
            'password': {
                'required': "Please enter your password",
            }
        }
