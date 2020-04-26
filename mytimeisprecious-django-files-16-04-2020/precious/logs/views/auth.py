from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect
from logs.models import User
from logs.forms.auth_forms import SignUpForm, SignInForm
import datetime
import json
from django.conf import settings

def sign_up(request):
    """ 
    Signs user up
    """
    form = SignUpForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # record_and_send_contact_us_email(form)
        # TODO sign up and redirect
        User.objects.create_user(form.cleaned_data.get('email'),
                                 form.cleaned_data.get('username'),
                                 form.cleaned_data.get('password')
                                 )
        # return redirect(reverse('default'))

    return render(request, 'auth/sign_up.html', {
        'form': form
    })
