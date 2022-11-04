from django import forms
from scottyseats.models import PlayerModel, CommentModel, Profile

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EntryForm(forms.Form):
    last_name     = forms.CharField(max_length=20)
    first_name    = forms.CharField(max_length=20)
    birthday      = forms.DateField(required=False)
    children      = forms.IntegerField(required=False, label='# of children')
    address       = forms.CharField(required=False, max_length=200)
    city          = forms.CharField(required=False, max_length=30)
    state         = forms.CharField(required=False, max_length=20)
    zip_code      = forms.CharField(required=False, max_length=10)
    country       = forms.CharField(required=False, max_length=30)
    email         = forms.CharField(required=False, max_length=32)
    phone_number  = forms.CharField(required=False, max_length=16, label='Phone #')

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class NewUser(forms.ModelForm):
    class Meta:
        model = PlayerModel
        fields = ('username',)
        labels = {
            'username': 'Create A Nickname:'
        }
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
'''
class UpdateProfile(forms.Form):
    bio_input_text = forms.CharField(max_length = 100)
    profile_picture = forms.ImageField()
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        post_input_text = cleaned_data.get('post_0')
        # We must return the cleaned data we got from our parent.
        return cleaned_data'''

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'bio')
        widgets = {
            'bio':forms.Textarea(attrs={'id':'id_bio_input_text','rows':'3'}),
            'picture':forms.FileInput(attrs={'id':'id_profile_picture'})
        }

class NewComment(forms.Form):
    class Meta:
        model = CommentModel
        exclude = ('post_by', 'update_time', 'commented_post_id')
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.


class RegisterForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm',  
                                 widget = forms.PasswordInput())
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
