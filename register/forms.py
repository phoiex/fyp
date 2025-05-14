from django import forms
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from register.models import Company as Comp, UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    company = forms.ModelChoiceField(queryset=Comp.objects.all())

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'company',
            'password1',
            'password2',
        ]
        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'company': 'Company',
        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            company = self.cleaned_data['company']
            # Get Company object from the database in a safe way
            company_obj = Comp.objects.filter(name=company.name).first()

            UserProfile.objects.create(user=user, company=company_obj)

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password1': 'Password',
            'password2': 'Retype Password',
        }
        for field, text in placeholders.items():
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': text
            })
        self.fields['company'].widget.attrs['class'] = 'form-control'


class CompanyRegistrationForm(forms.Form):
    social_name = forms.CharField(max_length=80)
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    city = forms.CharField(max_length=50)
    found_date = forms.DateField()

    class Meta:
        model = Comp

    def save(self, commit=True):
        company = Comp()
        company.social_name = self.cleaned_data['social_name']
        company.name = self.cleaned_data['name']
        company.email = self.cleaned_data['email']
        company.city = self.cleaned_data['city']
        company.found_date = self.cleaned_data['found_date']

        if commit:
            company.save()
        return company

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'social_name': 'Social Name',
            'name': 'Name',
            'email': 'Email',
            'city': 'City',
            'found_date': 'Found date',
        }
        for field, text in placeholders.items():
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': text
            })


class ProfilePictureForm(forms.Form):
    img = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ['img']

    def save(self, request, commit=True):
        user_profile = request.user.userprofile
        user_profile.img = self.cleaned_data['img']

        if commit:
            user_profile.save()
        return user_profile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update({
            'class': 'custom-file-input',
            'id': 'validatedCustomFile'
        })
