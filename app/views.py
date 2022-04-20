""" view file """
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin

from .models import CustomerInquiry, OTP
from .forms import CustomerInquiryForm, OTPForm, OTPVerifyForm
from .custom_method import generate_otp


class Home(SuccessMessageMixin, CreateView):
    """home page"""

    form_class = CustomerInquiryForm
    model = CustomerInquiry
    template_name = "app/form.html"
    success_message = "Inquiry sent successfully"
    success_url = reverse_lazy("otp_send")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "something went incorrect")
        return self.render_to_response(self.get_context_data(form=form))


class OTPView(FormView):
    """otp view"""

    form_class = OTPForm
    template_name = "app/otp_form.html"

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if CustomerInquiry.objects.filter(
            phone_no=form.cleaned_data.get("mobile_no")
        ).exists():

            otp = generate_otp(6)
            print("otp ", otp)
            otp = OTP(
                otp=otp,
                expire_time=datetime.now() + timedelta(minutes=5),
                mobile_no=form.cleaned_data.get("mobile_no"),
            )
            otp.save()
            messages.success(self.request, "otp sent successfully")
            return redirect(reverse("otp_verify", kwargs={"id": otp.id}))
        messages.error(self.request, "mobile no dose not exist")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs.update({"header": "User Mobile No", "otp_view": True})
        return super().get_context_data(**kwargs)


class OTPVerify(FormView):
    """otp verify"""

    success_url = reverse_lazy("home")
    form_class = OTPVerifyForm
    template_name = "app/otp_form.html"

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        otp_obj = OTP.objects.get(id=self.kwargs.get("id"))
        if "re_send" in self.request.POST:
            otp_obj.otp = generate_otp(6)
            otp_obj.expire_time = datetime.now() + timedelta(minutes=5)
            otp_obj.save()
            return redirect(reverse("otp_verify", kwargs={"id": self.kwargs.get("id")}))
        if datetime.now().replace(tzinfo=None) > otp_obj.expire_time.replace(
            tzinfo=None
        ) or otp_obj.otp != form.cleaned_data.get("otp", None):
            OTP.objects.exclude(id=self.kwargs.get("id")).delete()
            return super().form_invalid(form)
        OTP.objects.filter(mobile_no=otp_obj.otp).delete()
        messages.success(self.request, "mobile no verify successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs.update({"header": "OTP Verify", "otp_view": False})
        return super().get_context_data(**kwargs)
