# from django.shortcuts import render
import pandas as pd
from authentication.excelToJson import convertJson
from authentication.paymentInvoice import PaypalPayment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render


# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        file = request.FILES['excel_file']
        data = convertJson(file)
        missing_mail = []
        payment = PaypalPayment()
        for i in data:
            client_mail = i['email']
            cc_mail = i['cc']
            item_name = i['product']
            amount = i['amount']
            note = i['note']
            address = i['address']
            city = i['city']
            state = i['state']
            postal_code = i['zip']
            if amount is not None:
                invoice_status = payment.getInvoice(client_mail, cc_mail, item_name, amount, note, address, city, state, postal_code)
                if type(invoice_status) != bool:
                    missing_mail.append(invoice_status)
        count_missing_mail = int(len(missing_mail))
        return render(request, "authentication/success.html", {'count': count_missing_mail, 'mails': missing_mail})
    return render(request, "authentication/index.html")
            

    return render(request, "authentication/index.html")

def signUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been successfully created !")
        return redirect('login')
    return render(request, "authentication/signup.html")

def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            error_message = 'Invalid login credentials'
            render(request, 'authentication/login.html', {'error_message': error_message})
    return render(request, 'authentication/login.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('login')