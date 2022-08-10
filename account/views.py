from django.contrib.auth import get_user_model, login as auth_login
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.views.generic import View, TemplateView
from django.contrib.auth.views import (LoginView, 
										LogoutView,
										PasswordResetView as PasswordReset,
										PasswordResetDoneView as PasswordResetDone,
										PasswordResetConfirmView as PasswordResetConfirm,
										PasswordResetCompleteView as PasswordResetComplete
										)
from braces.views import AnonymousRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm
from .utils import send_verification_mail
from .tokens import account_activation_token

class ActiveEmailView(LoginRequiredMixin, TemplateView):
	def get(self, *args, **kwargs):
		user = self.request.user
		if not user.is_verified:
			current_site = get_current_site(self.request)
			success = send_verification_mail(user, current_site, user.email)
			if success:
				message = 'email sent successfully.Open the link sent to your email.'
			else:
				message = 'email not sent.Please check your email or try again later'
		else:
			message = 'your email is already verified.'

		return render(
			request=self.request,
			template_name='account/registration/email_sent.html',
			context={'message': message}
			)

class UserLoginView(AnonymousRequiredMixin, LoginView):
	template_name = 'account/registration/login.html'
	authenticated_redirect_url = reverse_lazy("account:dashboard")
	success_url = reverse_lazy("account:dashboard") 
	
	def form_valid(self, form):
		user = form.get_user()
		if not user.is_verified:
			current_site = get_current_site(self.request)
			success = send_verification_mail(user, current_site, user.email)
			if success:
				message = 'email sent successfully.Open the link sent to your email.'
			else:
				message = 'email not sent.Please check your email or try again later'

			return render(
				request=self.request,
				template_name='account/registration/email_sent.html',
				context={'message': message}
				)
		else:
			auth_login(self.request, form.get_user())
			return redirect('account:dashboard')

class UserSignUpView(AnonymousRequiredMixin, View):
	authenticated_redirect_url = reverse_lazy("account:dashboard")

	def post(self, *args, **kwargs):
		form = SignUpForm(self.request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			user = form.save()
			current_site = get_current_site(self.request)
			success = send_verification_mail(user, current_site, email)
			if success:
				message = 'email sent successfully.Open the link sent to your email.'
			else:
				user.delete()
				message = 'email not sent.Please check your email or try again later'

			return render(
                request=self.request,
                template_name='account/registration/email_sent.html',
                context={'message': message}
                )
		else:
			return render(
                request=self.request,
                template_name='account/registration/signup.html',
                context={'form': form}
                )

	def get(self, *args, **kwargs):
		form = SignUpForm()
		return render(
            request=self.request,
            template_name='account/registration/signup.html',
            context={'form': form}
        )

class UserLogoutView(LoginRequiredMixin, LogoutView):
	next_page = 'account:login'

class VerifyEmailView(View):
    def get(self,*args, **kwargs):
        User = get_user_model()
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None 
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_verified = True 
            user.save()
            return render(request=self.request, template_name='account/registration/verified.html')
        else:
            return render(request=self.request, template_name='account/registration/invalid.html')

class UserDashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'account/profile/dashboard.html'

class PasswordResetView(PasswordReset):
	template_name = 'account/reset/reset_form.html'
	success_url = reverse_lazy('account:reset_done')
	email_template_name = 'account/email_templates/email_reset_template.html'

class PasswordResetDoneView(PasswordResetDone):
	template_name = 'account/reset/reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirm):
	template_name = 'account/reset/reset_confirm.html'
	success_url = reverse_lazy('account:reset_complete') 


class PasswordResetCompleteView(PasswordResetComplete):
	template_name = 'account/reset/reset_complete.html'
