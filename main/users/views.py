from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

# СТРАНИЦА РЕГИСТРАЦИИ
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            tomail = form.cleaned_data.get('email') 
            username = form.cleaned_data.get('username')

            email = EmailMessage(
            'Успешная регистрация на Морском Маркетплэйсе',
            'Привет '+username +'. Спасибо за регистрацию аккаунта в Морском Маркетплэйсе.' ,
            to=[tomail, 'repostwebsite@gmail.com'])
            
            email.send()
            form.save()
           
            messages.success(request, f'Аккаунт зареган {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})



# СТРАНИЦА ВХОДА
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


# НАПОМНИТЬ ПАРОЛЬ НА EMAIL
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "Ссылка для смены пароля отправлена на email, " \
                      "Если существует учетная запись с введенным вами адресом электронной почты, письмо прийдет в ближайшее время." \
                      "Если вы не получили письмо на email, " \
                      "пожалуйста, убедитесь, что вы ввели email, с которым зарегистрировались, и проверьте папку со спамом."
    success_url = reverse_lazy('home')

# СМЕНИТЬ ПАРОЛЬ
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy('users-profile')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html',
    {'user_form': user_form, 'profile_form': profile_form})




