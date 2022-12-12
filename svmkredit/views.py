from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *
from django.contrib import messages

from svmkredit.pages.admin import *
from svmkredit.pages.user import *

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
import babel.numbers


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
                    return redirect('master', pk=idResult['MasterId'])
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
                return redirect('master', pk=idResult['UserId'])
        else:
            messages.info(request, 'Password Doesnt"t Match, Please Try Again')

    return render(request, 'register.html')

# class Register(TemplateView):
#     template_name = 'register.html'

Admin

User

def toPdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf)

    width, height = A4
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = []

    cursor.execute('select * from pengaju where Status = "Accepted"')
    disetujui = cursor.fetchall()

    keuanganDisetujui = []
    for d in disetujui:
        cursor.execute(f'select * from keuanganpengaju where PengajuId = {d["PengajuId"]}')
        dummy = cursor.fetchone()
        keuanganDisetujui.append(dummy)

    lines.append(("PengajuId", "Nama Pengaju", "Janga Waktu", "Nominal Ajuan", "Status"))
    disetujuizip = zip(disetujui, keuanganDisetujui)
    for d, k in disetujuizip:
        PermohonanKreditPengaju = babel.numbers.format_currency(k['PermohonanKreditPengaju'], 'IDR', locale="id")
        lines.append((str(d['PengajuId']), d['Nama'], str(k['JangkaWaktuKredit']) + " bulan", str(PermohonanKreditPengaju), d['Status']))

    # print(lines)
    table = Table(lines, colWidths=4 * cm)
    table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])

    table.wrapOn(c, width, height)
    table.drawOn(c, 5 * mm, 277 * mm)

    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='users.pdf')

def toPdf2(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf)

    width, height = A4
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = []

    cursor.execute('select * from pengaju where Status = "Declined"')
    ditolak = cursor.fetchall()

    keuanganDitolak = []
    for d in ditolak:
        cursor.execute(f'select * from keuanganpengaju where PengajuId = {d["PengajuId"]}')
        dummy = cursor.fetchone()
        keuanganDitolak.append(dummy)

    lines.append(("PengajuId", "Nama Pengaju", "Janga Waktu", "Nominal Ajuan", "Status"))
    disetujuizip = zip(ditolak, keuanganDitolak)
    for d, k in disetujuizip:
        PermohonanKreditPengaju = babel.numbers.format_currency(k['PermohonanKreditPengaju'], 'IDR', locale="id")
        lines.append((str(d['PengajuId']), d['Nama'], str(k['JangkaWaktuKredit']) + " bulan", str(PermohonanKreditPengaju), d['Status']))

    # print(lines)
    table = Table(lines, colWidths=4 * cm)
    table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])

    table.wrapOn(c, width, height)
    table.drawOn(c, 5 * mm, 277 * mm)

    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='users.pdf')
