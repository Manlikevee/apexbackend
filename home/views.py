from django.shortcuts import render
import shortuuid
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from dashboard.forms import contactusForm
from dashboard.models import contactus


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('userdashboard')  # Replace with the URL name or path of the non-superuser page
    return wrapper

def not_superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('superdashboard')  # Replace with the URL name or path of the superuser page
    return wrapper



def not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'you are already logged in')
            return redirect('superdashboard')  # Replace with the URL name or path of the superuser page
    return wrapper



# Create your views here.
@login_required()
def logout_view(request):
    messages.success(request, 'you have been logged out, see u soon.')
    logout(request)
    return redirect('login')



def home(request):


    return render(request, 'home.html')





def privacy(request):


    return render(request, 'privacy.html')


def terms(request):


    return render(request, 'terms.html')




def aboutus(request):


    return render(request, 'aboutus.html')



def contactme(request):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    key = s.random(length=10)
    if request.method == 'POST':

        form = contactusForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.reference = key
            profile.save()
            messages.success(request, 'Thank You for Reaching Out!, We appreciate your feedback and will respond to your inquiry shortly. ')
            contactdata(key)
            return redirect('contactus')
    else:
        form = contactusForm(request.POST)
    context = {
        'form': form,

    }
    return render(request, 'contactus.html', context)



def contactdata(key):
    contactusdata = contactus.objects.filter(reference=key).first()
    emails = 'mails@pwbfinance.com'
    email = contactusdata.email
    name = contactusdata.name
    reason = contactusdata.reason
    phonenumber = contactusdata.phonenumber
    message = contactusdata.message
    email = email
    subject = 'PWB Finance contact form'
    html_message = render_to_string('formdatas.html',
                                    {'name': name, 'reason': reason, 'phonenumber': phonenumber,
                                     'message':message, 'email' : email
                                     })

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [emails]

    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)