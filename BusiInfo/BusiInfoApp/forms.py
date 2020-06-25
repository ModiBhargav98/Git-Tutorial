from django import forms

class UserSignInSignUp(forms.Form):
    EnrollNum = forms.CharField(max_length=20)
    Password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class SellerSignInSignUp(forms.Form):
    # Just Signup
    RFID = forms.CharField(max_length=20)
    Password = forms.CharField(max_length=20,widget=forms.PasswordInput)