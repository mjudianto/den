from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *
from django.contrib import messages

from svmkredit.pages.admin import *
from svmkredit.pages.user import *

connection = connect()
cursor = connection.cursor(dictionary=True)

# Create your views here.
def Login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        account = 'admin'
        cursor.execute(f"SELECT Password FROM {account} where Email = '{email}'")
        passwordResult = cursor.fetchone()
        if passwordResult == None:
            account = 'master'
            cursor.execute(f"SELECT Password FROM {account} where Email = '{email}'")
            passwordResult = cursor.fetchone()
            if passwordResult == None:
                account = ''
                messages.info(request, 'Account Not Found')
            else:
                if password == passwordResult['Password']:
                    cursor.execute(f"SELECT MasterId FROM {account} where Email = '{email}'")
                    idResult = cursor.fetchone()
                    return redirect('user', pk=idResult['MasterId'])
                else:
                    messages.info(request, 'Email or Password is incorect')
        else:
            if password == passwordResult['Password']:
                cursor.execute(f"SELECT AdminId FROM {account} where Email = '{email}'")
                idResult = cursor.fetchone()
                return redirect('admin', pk=idResult['AdminId'])
            else:
                messages.info(request, 'Email or Password is incorect')

    return render(request, 'login.html')

# class Login(TemplateView):
#     template_name = 'login.html'

def Register(request):

    if request.method == 'POST':
        button = request.POST.get('button')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        telp = ''
        telp = request.POST.get('telp')

        if password == confirmpassword:
            if telp == None or telp == '':
                telp = 'null'
                value = 'null' + ', "' + email + '" , "' + password + '" ,' + telp
            else:
                value = 'null' + ', "' + email + '" , "' + password + '" , "' + telp + '"'
            print(value)

            if button == 'admin':
                insertToTable(button, value, connection, cursor)
                cursor.execute(f"SELECT AdminId FROM {button} where Email = '{email}'")
                idResult = cursor.fetchone()
                return redirect('admin', pk=idResult['AdminId'])    
            if button == 'user':
                insertToTable(button, value, connection, cursor)
                cursor.execute(f"SELECT UserId FROM {button} where Email = '{email}'")
                idResult = cursor.fetchone()
                return redirect('user', pk=idResult['UserId'])
        else:
            messages.info(request, 'Password Doesnt"t Match, Please Try Again')

    return render(request, 'register.html')

# class Register(TemplateView):
#     template_name = 'register.html'

Admin

User