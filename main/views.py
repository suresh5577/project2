from django.shortcuts import render,redirect,HttpResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import base64
import urllib
from django.conf import settings
from django.urls import reverse_lazy,reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from main.utils import *

# Create your views here.
def home(request):
    count = User.objects.count()
    return render(request,'home.html',
    {'count':count})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request,'registration/signup.html',{ 'form' : form })

def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username',None)
        try:
            User.objects.get(username = username)
            enc_username = encrypt(username)

            mail_subject = 'reset your password'
            to_mail_ids = [username]
            mail_body = '<h2> If have you requested for password reset? then click below link</h2>'
            mail_body += '<a href = "%s%s">Reset Password</a>' %(settings.BASE_DOMAIN,reverse('reset_password',kwargs={'enc_username':enc_username}))

            response = sendEmail(mail_subject,to_mail_ids,mail_body)
            if response:
                return HttpResponse("reset password link send to your mail")
            else:
                return HttpResponse("something went wrong please try again")
        except ObjectDoesNotExist:
            return HttpResponse('user not found<br/><a href="%s"> Goback  </a>'%reverse('forgot_password'))


    return render(request,'registration/forgotpassword.html')


def resetPassword(request,enc_username):
    username = decrypt(enc_username)
    try:
        userObj = User.objects.get(username = username)
    except ObjectDoesNotExist:
        raise Http404

    if request.method =='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("password and conform password not matching!!!")
        userObj.set_password(password1)
        userObj.save()
        return HttpResponse("your password reset successfully <a href ='%s'>Go to Login</a>"%reverse('login'))

    return render(request,'registration/resetPassword.html',{'username':username})