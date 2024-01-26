import shortuuid
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import mail
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from dashboard.forms import RegistrationForm, BeneficairyForm, supportForm
from dashboard.models import Transaction, Support, contactus, Userstatus, latestupdate, Beneficiary
from home.views import superuser_required, not_superuser_required


@login_required()
@superuser_required
def userspage(request):
    incoming = User.objects.filter(is_superuser=False).count()
    allusers = Userstatus.objects.all().order_by('-id')
    context = {
        'incoming': incoming,
        'allusers': allusers,

    }

    return render(request, 'allusers.html', context)


@login_required()
def transactions(request):
    if not request.user.is_superuser:
        transactions = Transaction.objects.filter(requestuser=request.user).filter(
            status='confirmed').order_by('-updated_at')
        outgoing = Transaction.objects.filter(type='debit').filter(status='confirmed').filter(
            requestuser=request.user).filter(type='debit').aggregate(
            Sum('amount'))
        incoming = Transaction.objects.filter(status='confirmed').filter(requestuser=request.user).filter(
            type='credit').aggregate(
            Sum('amount'))

        outgoingcount = Transaction.objects.filter(type='debit').filter(status='confirmed').filter(
            requestuser=request.user).filter(type='debit').count()
        incomingcount = Transaction.objects.filter(status='confirmed').filter(requestuser=request.user).filter(
            type='credit').count()
    else:
        transactions = Transaction.objects.filter(
            status='confirmed').order_by('-updated_at')
        outgoing = Transaction.objects.filter(type='debit').filter(status='confirmed').filter(type='debit').aggregate(
            Sum('amount'))
        incoming = Transaction.objects.filter(status='confirmed').filter(
            type='credit').aggregate(
            Sum('amount'))

        outgoingcount = Transaction.objects.filter(type='debit').filter(status='confirmed').filter(type='debit').count()
        incomingcount = Transaction.objects.filter(status='confirmed').filter(
            type='credit').count()

    return render(request, 'transactions.html',
                  {'outgoingcount': outgoingcount, 'incomingcount': incomingcount, 'transactions': transactions,
                   'outgoing': outgoing, 'incoming': incoming}
                  )


@login_required()
@superuser_required
def superdashboard(request):
    latestupdates = latestupdate.objects.all()[:5]
    transfers = Transaction.objects.all().filter(type='debit').order_by('-updated_at')[:10]
    incoming = User.objects.filter(is_superuser=False).count()
    outgoing = Transaction.objects.filter(type='debit').filter(status='confirmed').count()
    support = Support.objects.all().order_by('-posteddate')[:10]
    contact = contactus.objects.all().order_by('-posteddate')[:10]
    dollarinvestments = Transaction.objects.filter(status='confirmed').filter(type='debit').aggregate(
        Sum('amount'))

    context = {
        'transfers': transfers,
        'incoming': incoming,
        'outgoing': outgoing,
        'dollarinvestments': dollarinvestments,
        'support': support,
        'contact': contact,
        'latestupdates': latestupdates

    }

    return render(request, 'admindashboard.html', context)


@login_required()
@not_superuser_required
def userdashboard(request):
    if request.user:
        if not request.user.is_superuser:
            user = request.user
            Userstatus.objects.update_or_create(
                user=user,
                defaults={
                    'user': user,
                }
            )

        user_obj = User.objects.get(pk=request.user.pk)
        user_group = Group.objects.get_or_create(name='regular_user')

        group = Group.objects.get(name='regular_user')
        user_obj.groups.add(group)

        transfers = Transaction.objects.filter(requestuser=request.user).all().order_by('-updated_at')[:4]
        transfers2 = Transaction.objects.filter(requestuser=request.user).all().order_by('updated_at')[:4]
        incoming = Transaction.objects.filter(type='credit').filter(status='confirmed').filter(
            requestuser=request.user).count()
        outgoing = Transaction.objects.filter(type='debit').filter(status='confirmed').filter(
            requestuser=request.user).count()
        dollarinvestments = Transaction.objects.filter(requestuser=request.user).filter(status='confirmed').aggregate(
            Sum('amount'))
        vee = 12000.2
        manlikevee = dollarinvestments['amount__sum']

        if manlikevee == 'None':
            manlikevees = dollarinvestments['amount__sum'] + vee
        else:
            manlikevees = vee
        print(manlikevees)

        context = {
            'transfers': transfers,
            'incoming': incoming,
            'outgoing': outgoing,
            'dollarinvestments': dollarinvestments,
            'transfers2': transfers2
        }




    return render(request, 'dashboard.html', context)

def trans(request):

    return render(request, 'withdraw.html')
def accountopen(username, email, firstname, password):
    email = email
    subject = 'PWB Finance  Account Information'
    html_message = render_to_string('userdata.html',
                                    {'accountnum': username, 'password': password, 'firstname': firstname
                                     })

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)


@login_required()
@superuser_required
def register(request):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    today = date.today()
    random_reference = shortuuid.uuid()[0:15]
    key = s.random(length=9)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            checked = form.cleaned_data['checkboxed']
            credit_amount = form.cleaned_data['credit_amount']
            narration = form.cleaned_data['narration']
            frommoney = form.cleaned_data['frommoney']
            mypaymentdata = {
                "data": {
                    "id": f'{key}',
                    "log": {
                        "input": [

                        ],
                        "errors": 0,
                        "mobile": 'true',
                        "history": [
                            {
                                "time": 1,
                                "type": "action",
                                "message": "Connecting With Merchant Bank"
                            },
                            {
                                "time": 2,
                                "type": "action",
                                "message": "Verifying Source Destination"
                            },
                            {
                                "time": 3,
                                "type": "action",
                                "message": "Attempted to receive Funds"
                            },
                            {
                                "time": 4,
                                "type": "success",
                                "message": "Successfully received"
                            },
                            {
                                "time": 5,
                                "type": "success",
                                "message": "Updating Users Balance"
                            }
                        ],
                        "success": 'true',
                        "attempts": 1,
                        "start_time": 1670318568,
                        "time_spent": 4
                    },
                    "fees": 300,
                    "plan": 'null',
                    "split": {

                    },
                    "amount": f'{credit_amount}',
                    "domain": "cellafinance.com",
                    "paidAt": "2022-12-06T09:22:50.000Z",
                    "source": 'null',
                    "status": "success",
                    "channel": "card",
                    "message": 'null',
                    "paid_at": f'{today}',
                    "currency": "USD",
                    "customer": {
                        "id": 53845337,
                        "email": "mails@cellafinance.com",
                        "phone": "+23408165201384",
                        "metadata": 'null',
                        "last_name": f'',
                        "first_name": f'',
                        "risk_action": "default",
                        "customer_code": "CUS_egqj2lfmbk4cmzf",
                        "international_format_phone": "+738828"
                    },
                    "metadata": "",
                    "order_id": 'null',
                    "createdAt": "2022-12-06T09:22:35.000Z",
                    "reference": "0uraa6qxnk",
                    "created_at": "2022-12-06T09:22:35.000Z",
                    "fees_split": 'null',
                    "ip_address": "102.67.1.32",
                    "subaccount": {

                    },
                    "plan_object": {

                    },
                    "authorization": {
                        "bin": "408408",
                        "bank": "Cella Finance",
                        "brand": "visa",
                        "last4": "4081",
                        "channel": "card",
                        "exp_year": "2030",
                        "reusable": 'true',
                        "card_type": "visa ",
                        "exp_month": "12",
                        "signature": f'{random_reference}',
                        "account_name": 'null',
                        "country_code": "NG",
                        "authorization_code": "AUTH_rv782ib5mt"
                    },
                    "fees_breakdown": 'null',
                    "gateway_response": "Successful",
                    "requested_amount": '3500000',
                    "transaction_date": "2022-12-06T09:22:35.000Z",
                    "pos_transaction_data": 'null'
                },
                "status": 'true',
                "message": "Payment successful"
            }

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Account Number already exists.')
            else:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                                last_name=lastname)
                group = Group.objects.get(name='regular_user')  # Replace with your group name
                user.groups.add(group)
                user.save()
                Transaction.objects.update_or_create(requestuser=user,
                                                     defaults={'requestuser': user,
                                                               'type': 'credit', 'status': 'confirmed',
                                                               'witholdingtax': f'{credit_amount}',
                                                               'amount': f'{credit_amount}',
                                                               'narration': f'{narration}',
                                                               'payment_data': mypaymentdata,
                                                               'reference': key, 'paymentto': f'{frommoney}'
                                                               })
                Userstatus.objects.update_or_create(
                    user=user,
                    defaults={
                        'user': user,
                    }
                )
                latestupdate.objects.create(user=user, data='Deposit', text=f'credit alert of {credit_amount}', ref=key)

                messages.success(request, 'User Successfully Created.')

                if checked == True:
                    accountopen(username, email, firstname, password)
                    return redirect('register')
                else:
                    return redirect('register')  # Redirect to a success page
        else:
            messages.error(request, 'An Error Occured')
            return redirect('register')  # Redirect to a success page

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


@login_required()
def withdrawal(request):
    beneficary = Beneficiary.objects.filter(user=request.user).all()
    print(beneficary)
    if not request.user.is_superuser:
        user = request.user
        Userstatus.objects.update_or_create(
            user=user,
            defaults={
                'user': user,
            }
        )

    pending = False
    dollarinvestments = Transaction.objects.filter(requestuser=request.user).filter(
        status='confirmed').aggregate(
        Sum('amount'))
    successtransfer = Transaction.objects.filter(status='confirmed').filter(type='debit').filter(
        requestuser=request.user)

    if successtransfer:
        pending = False
    else:
        pending = True
    return render(request, 'withdrawal.html',
                  {'dollarinvestments': dollarinvestments, 'pending': pending, 'beneficiary': beneficary})


@login_required()
def completetransaction(request, id):
    pending = False

    successtransfer = Transaction.objects.filter(status='confirmed').filter(type='debit').filter(
        requestuser=request.user).all()
    j = get_object_or_404(Transaction, reference=id)
    search_result = j.payment_data

    if successtransfer.exists():
        first_object_id = j.id
        target_object_id = successtransfer[0].id
        print(target_object_id)
        print(first_object_id)

        if first_object_id == target_object_id:
            pending = True
        else:
            pending = False

    context = {
        'search_result': search_result,
        'j': j,
        'pending': pending

    }

    return render(request, 'transactiondetail.html', context)


@login_required()
def supportdetail(request, id):
    support = Support.objects.filter(reference=id).all().first()

    context = {
        'support': support,

    }

    return render(request, 'supportdetail.html', context)


@login_required()
def contactdetail(request, id):
    contact = contactus.objects.filter(reference=id).all().first()

    context = {
        'contact': contact,

    }

    return render(request, 'contactdetail.html', context)


@login_required()
def supportpage(request):
    if not request.user.is_superuser:
        supportticket = Support.objects.filter(user=request.user).all()
        supportticketopen = Support.objects.filter(user=request.user).filter(status='pending').all().count()
        supportticketclosed = Support.objects.filter(user=request.user).filter(status='resolved').all().count()
    else:
        supportticket = Support.objects.all()
        supportticketopen = Support.objects.filter(status='pending').all().count()
        supportticketclosed = Support.objects.filter(status='resolved').all().count()

    myuser = User.objects.get(pk=request.user.pk)
    s = shortuuid.ShortUUID(alphabet="0123456789")
    key = s.random(length=9)
    if request.method == 'POST':

        form = supportForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = myuser
            profile.reference = key
            profile.save()
            messages.success(request, 'Your Support Ticket Has Been Booked')
            latestupdate.objects.create(user=request.user, data='Support', text=f'New Support ticket', ref=key)

            return redirect('supportpage')

    else:
        form = supportForm(request.POST)

        context = {
            'form': form,
            'supportticket': supportticket,
            'supportticketopen': supportticketopen,
            'supportticketclosed': supportticketclosed

        }

    return render(request, 'support.html', context)


@login_required()
@superuser_required
def contactpage(request):
    if request.user.is_superuser:
        supportticket = contactus.objects.all()
        supportticketopen = contactus.objects.all().count()
    else:
        return redirect('userdashboard')

    context = {
        'supportticket': supportticket,
        'supportticketopen': supportticketopen,

    }

    return render(request, 'contactdata.html', context)


def beneficiary(request):
    myuser = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = BeneficairyForm(request.POST)
        if form.is_valid:
            profile = form.save(commit=False)
            profile.user = myuser
            profile.save()

        messages.success(request, f'Your Beneficiary Details Has Been Added Successfully!')
        return redirect('userdashboard')


@csrf_exempt
def your_view(request):
    successtransfer = Transaction.objects.filter(status='confirmed').filter(type='debit').filter(
        requestuser=request.user)
    if successtransfer:
        pending = 'pending'
    else:
        pending = 'successful'

    if request.method == 'POST':
        value = request.POST.get('value')
        accountname = request.POST.get('accountname')
        accountnumber = request.POST.get('accountnumber')
        narration = request.POST.get('narration')
        bank = request.POST.get('bank')

        s = shortuuid.ShortUUID(alphabet="0123456789")
        key = s.random(length=9)
        key2 = s.random(length=10)
        random_reference = shortuuid.uuid()[0:15]
        random_reference2 = shortuuid.uuid()[0:15]
        today = date.today()
        dollarinvestments = Transaction.objects.filter(requestuser=request.user).filter(
            status='confirmed').aggregate(
            Sum('amount'))
        print(dollarinvestments['amount__sum'])
        result = -1 * (float(value) * 1)
        manlikevee2 = dollarinvestments['amount__sum']

        if manlikevee2 is None:
            addedbalance2 = result
        else:
            addedbalance2 = float(manlikevee2) + result
        beneficiarydata = {
            "data": {
                "accountname": f'{accountname}',
                "accountnumber": f'{accountnumber}',
                "bank": f'{bank}',
            }
        }
        processingdata = {
            "data": {
                "id": f'{key2}',
                "log": {
                    "input": [

                    ],
                    "errors": 0,
                    "mobile": 'true',
                    "history": [
                        {
                            "time": 1,
                            "type": "action",
                            "message": "Retrieve the user's account information"
                        },
                        {
                            "time": 2,
                            "type": "action",
                            "message": "Determining the amount to be debited from the user's account"
                        },
                        {
                            "time": 3,
                            "type": "action",
                            "message": "Verifying if the user has sufficient funds to complete the debit."
                        },
                        {
                            "time": 4,
                            "type": "action",
                            "message": "Createing a new transaction record to document the debit"
                        },

                        {
                            "time": 6,
                            "type": "action",
                            "message": "Saving the transaction record in the database."
                        },
                        {
                            "time": 7,
                            "type": "success",
                            "message": "debited to users account"
                        },
                        {
                            "time": 8,
                            "type": "success",
                            "message": "Updating Users Balance"
                        },
                        {
                            "time": 7,
                            "type": "error",
                            "message": "payment still pending"
                        },
                        {
                            "time": 7,
                            "type": "error",
                            "message": "error connecting with users bank"
                        },
                        {
                            "time": 7,
                            "type": "error",
                            "message": "wait a few hours or contact support"
                        },
                    ],
                    "success": 'true',
                    "attempts": 1,
                    "start_time": 1670318568,
                    "time_spent": 4
                },
                "fees": 300,
                "plan": 'null',
                "split": {

                },
                "amount": f'{value}',
                "domain": "cellafinance.com",
                "paidAt": "2022-12-06T09:22:50.000Z",
                "source": 'null',
                "status": "success",
                "channel": "card",
                "message": 'null',
                "paid_at": f'{today}',
                "currency": "USD",
                "customer": {
                    "id": f'{key2}',
                    "email": "odahviktor@gmail.com",
                    "phone": "+23408165201384",
                    "metadata": 'null',
                    "last_name": f'{request.user.last_name}',
                    "first_name": f'{request.user.first_name}',
                    "risk_action": "default",
                    "customer_code": "CUS_egqj2lfmbk4cmzf",
                    "international_format_phone": "+2348165201384"
                },
                "metadata": "",
                "order_id": 'null',
                "createdAt": "2022-12-06T09:22:35.000Z",
                "reference": f'{random_reference2}',
                "created_at": "2022-12-06T09:22:35.000Z",
                "fees_split": 'null',
                "ip_address": "102.67.1.32",
                "subaccount": {

                },
                "plan_object": {

                },
                "authorization": {
                    "bin": "408408",
                    "bank": "Cella Finance",
                    "brand": "visa",
                    "last4": "4081",
                    "channel": "Transfer",
                    "exp_year": "2030",
                    "reusable": 'true',
                    "card_type": "visa ",
                    "exp_month": "12",
                    "signature": f'{random_reference2}',
                    "account_name": 'null',
                    "country_code": "NG",
                    "authorization_code": "AUTH_rv782ib5mt"
                },
                "fees_breakdown": 'null',
                "gateway_response": "Successful",
                "requested_amount": '20000',
                "transaction_date": "2022-12-06T09:22:35.000Z",
                "pos_transaction_data": 'null'
            },
            "status": 'true',
            "message": f'{pending}'
        }

        print(value)

        my_model_obj2 = Transaction(reference=key2, type='debit', narration=narration,
                                    status='confirmed', amount=result, payment_data=processingdata,
                                    witholdingtax=addedbalance2, bankdetails=beneficiarydata,
                                    paymentto=accountname
                                    )

        my_model_obj2.requestuser = request.user
        my_model_obj2.save()
        latestupdate.objects.create(user=request.user, data='Withdrawal', text=f'withdrawal  of {result}', ref=key2)

        email = request.user.email
        trxamt = value
        trxtyp = 'debit'
        dates = today
        sender = request.user.get_full_name
        destination = f'{accountname} {accountnumber} '
        trxref = random_reference2
        trxstatus = f'{pending}'
        jobreferralemail(trxamt, trxtyp, dates, sender, trxref, trxstatus, email, destination)

        return HttpResponse('Value received')
    else:
        return HttpResponse('Invalid request method')


def jobreferralemail(trxamt, trxtyp, dates, sender, trxref, trxstatus, email, destination):
    email = email
    usersname = 'odahviktor@gmail.com'
    usersname2 = 'odahviktor@gmail.com'
    key = 'odahviktor@gmail.com'

    trxamt = trxamt
    trxtyp = trxtyp
    date = dates
    sender = sender
    destination = destination
    trxref = trxref
    trxstatus = trxstatus
    jb = 'ddd'

    context = {
        'trxamt': trxamt,
        'trxtyp': trxtyp,
        'date': date,
        'sender': sender,
        'trxref': trxref,
        'trxstatus': trxstatus
    }
    subject = 'Transaction Report'
    html_message = render_to_string('refferal.html',
                                    {'usersname': usersname, 'usersname2': usersname2, 'jb': jb, 'trxamt': trxamt,
                                     'trxtyp': trxtyp,
                                     'date': dates,
                                     'sender': sender,
                                     'trxref': trxref,
                                     'trxstatus': trxstatus,
                                     'destination': destination
                                     })

    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)


from django.core.mail import send_mail


def send_email(request):
    from_email = settings.EMAIL_HOST_USER
    to = 'ennyvix@gmail.com'

    subject = 'Hello, this is the subject'
    message = 'test'
    from_email = from_email
    recipient_list = [to]

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Email sent successfully!')


from django.shortcuts import render

# Create your views here.
