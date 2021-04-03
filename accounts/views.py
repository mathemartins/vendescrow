from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from accounts.forms import ReactivateEmailForm
from accounts.models import Profile, EmailActivation

User = get_user_model()


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Proceed to login!")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("account-password:password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = Profile.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        context['currentTime'] = timezone.now()
        return context

    def render_to_response(self, context, **response_kwargs):
        if context:
            user_obj = str(self.get_object())
            if user_obj != self.request.user.username:
                return HttpResponseRedirect(reverse('404_'))
            if self.request.user.first_name and self.request.user.last_name:
                messages.success(self.request, 'Welcome to your profile, {}'.format(self.get_object().get_name()))
            else:
                messages.warning(self.request, '{}, Profile Update Is Required'.format(self.request.user.username))
        return super(UserProfileView, self).render_to_response(context, **response_kwargs)

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return redirect(reverse('404_'))
        except Profile.MultipleObjectsReturned:
            qs = Profile.objects.filter(slug=slug)
            instance = qs.first()
        except:
            return redirect(reverse('404_'))
        return instance
