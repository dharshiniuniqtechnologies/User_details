from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows":4, "maxlength": 2000}),
        }

    def clean_message(self):
        msg = self.cleaned_data.get("message", "")
        # Example validation: length & simple sanitization
        if len(msg) < 5:
            raise forms.ValidationError("Message too short.")
        return msg.strip()
