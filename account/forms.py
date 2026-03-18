import re
from django import forms
from .models import User,Citizen,AreaOfficer,Contact


class UserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
        })
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "role"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),
            "email": forms.EmailInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),
            "role": forms.Select(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ):
            raise forms.ValidationError(
                "Password must contain uppercase, lowercase, number, and special character."
            )

        return password


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not (email.endswith(".com") or email.endswith(".in")):
            raise forms.ValidationError("Email must end with .com or .in")

        return email


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data
    
class CitizenForm(forms.ModelForm):

    class Meta:
        model = Citizen
        fields = ["aadhar"]

        widgets = {
            "aadhar": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            })
        }

    def clean_aadhar(self):
        aadhar = self.cleaned_data.get("aadhar")

        if not aadhar.isdigit():
            raise forms.ValidationError("Aadhar must contain only digits")

        if len(aadhar) != 12:
            raise forms.ValidationError("Aadhar number must be exactly 12 digits")

        return aadhar


class AreaOfficerForm(forms.ModelForm):

    class Meta:
        model = AreaOfficer
        fields = ["badge_number"]

        widgets = {
            "badge_number": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ["phone", "address", "city", "state"]

        widgets = {

            "phone": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),

            "address": forms.Textarea(attrs={
                "rows":2,
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),

            "city": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),

            "state": forms.TextInput(attrs={
                "class":"w-full border border-gray-300 rounded-lg p-2 shadow-sm focus:ring-2 focus:ring-indigo-400 focus:outline-none"
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")

        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")

        if not phone.startswith(("6","7","8","9")):
            raise forms.ValidationError("Enter a valid Indian phone number")

        return phone