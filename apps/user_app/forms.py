from django import forms
import pytz

class RegForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter your name'
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter your email'
        }
    ))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter a password (8 characters or longer)'
        }
    ))
    conf_pass = forms.CharField(max_length=50, min_length=8, widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Re-enter your password to confirm'
        }
    ))
    timezone = forms.ChoiceField(
        choices=[(t, t) for t in pytz.common_timezones],
        widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ),
        label='Time Zone',
        help_text='Please choose your time zone'
    )
    def clean(self):
        cleaned_data = super(RegForm, self).clean()
        password = cleaned_data.get("password")
        conf_pass = cleaned_data.get("conf_pass")
        if password and conf_pass:
            if not password == conf_pass:
                msg = "Passwords must match."
                self.add_error('password', msg)
                self.add_error('conf_pass', msg)

class LogForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter your email'
        }
    ))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter a password (8 characters or longer)'
        }
    ))