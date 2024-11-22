from django import forms
from datetime import date
from .models import Member, Claim, Beneficiary, CustomUser, Trustee, Setting

class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super(MemberForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create the associated member profile
            Member.objects.create(user=user, membership_date = date.today())
        return user


class AccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        
    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)
        #user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class MemberDetailForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number', 'gender', 'date_of_birth', 'id_number', 'hit_ec_number', 'residential_address', 'employment_position', 'extension', 'fax', 'department', 'employment_duration', 'office_number']
        widgets = {
            'residential_address': forms.Textarea(attrs={'rows': 2}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female')]),
        }

class TrusteeForm(forms.ModelForm):
    class Meta:
        model = Trustee
        fields = ['position', 'role', 'description']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = []


class ClaimForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.qset = kwargs.pop("qset", None)
        super(ClaimForm, self).__init__(*args, **kwargs)
        if self.qset:
            self.fields['beneficiary'].queryset = self.qset

    class Meta:
        model = Claim
        fields = ['beneficiary', 'description', 'proof_of_claim']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['full_name', 'relationship_type', 'id_number', 'proof_of_relationship']
        widgets = {
            'relationship_type': forms.Select(choices=[('spouse', 'Spouse'), ('child', 'Child'), ('parent', 'Parent'), ('principal', 'Principal'), ('nominee', 'Nominee')]),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=False)
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)

