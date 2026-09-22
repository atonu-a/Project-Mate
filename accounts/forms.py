from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Jordan'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Lee'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # সব ইনপুট ফিল্ডে 'form-input' CSS class অটোমেটিক যোগ হবে
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{current_class} form-input".strip()

        # Placeholders সেট করা
        self.fields['username'].widget.attrs.update({'placeholder': 'jordan_lee'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Jordan'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Lee'})
        self.fields['email'].widget.attrs.update({'placeholder': 'you@example.com'})
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'At least 8 characters'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Re-enter password'})