from django import forms
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm



class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["job_preference"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Add email field manually (comes from User model)
        self.fields["email"] = forms.EmailField(
            initial=self.user.email,
            required=True
        )

        # Styling (Tailwind classes)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Save email to User model
        self.user.email = self.cleaned_data["email"]

        if commit:
            profile.save()
            self.user.save()

        return profile



class StyledPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })
