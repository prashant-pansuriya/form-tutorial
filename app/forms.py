""" form """
from django.forms.widgets import TextInput, DateInput, Textarea
from django import forms

from .models import CustomerInquiry


class CustomerInquiryForm(forms.ModelForm):
    """customer inquiry form"""

    def __init__(self, *args, **kwargs):
        """remove label suffix"""
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        pattern = "[789][0-9]{9}"  # add mobile no pattern

    def clean(self):
        """date validation"""
        cleaned_data = super().clean()
        if cleaned_data.get("start_date") > cleaned_data.get("end_date"):
            raise forms.ValidationError(
                {"start_date": "Please select valid start date"}
            )
        return cleaned_data

    class Meta:
        """model meta info"""

        model = CustomerInquiry
        fields = "__all__"
        widgets = {
            "phone_no": TextInput(attrs={"pattern": "[789][0-9]{9}"}),
            "start_date": DateInput(attrs={"type": "date"}),
            "end_date": DateInput(attrs={"type": "date"}),
            "complaint_msg": Textarea(attrs={"rows": 5}),
        }


class OTPForm(forms.Form):
    """otp form"""

    mobile_no = forms.CharField(label="Mobile No", max_length=10, min_length=10)

    def __init__(self, *args, **kwargs):
        """remove label suffix"""
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        """meta info"""

        fields = ("mobile_no",)
        widgets = {
            "mobile_no": TextInput(attrs={"pattern": "[789][0-9]{9}"}),
        }


class OTPVerifyForm(forms.Form):
    """otp verify form"""

    otp = forms.CharField(label="OTP", help_text="OTP valid only 5 mins")

    def __init__(self, *args, **kwargs):
        """remove label suffix & add class"""
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        """class meta info"""

        fields = ("otp",)
