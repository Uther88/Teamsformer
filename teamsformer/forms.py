from django import forms
from .models import User, Team, Message
from django.forms import ModelForm
from select_multiple_field.forms import SelectMultipleFormField
from select_multiple_field.widgets import SelectMultipleField
from .models import ROLES


# Form for editing user profile
class UserForm(ModelForm):
    username = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(max_length=40, required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'skills', 'about',
                  'avatar',
                  )

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = 'true'

    def __str__(self):
        return 'UserForm'

# Form for editing and creating teams
class TeamForm(ModelForm):
    needs = SelectMultipleFormField(widget=forms.CheckboxSelectMultiple,
                                    choices=ROLES, required=False
                                      )

    class Meta:
        model = Team
        fields = ('title', 'subjects', 'description',
                  'image', 'developer',
                  'investor', 'sales_person', 'needs'
                  )

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['needs'].widget.attrs['class'] = 'choices'


# Form for creating new messages
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control hresize'