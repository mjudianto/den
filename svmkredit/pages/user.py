from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *

connection = connect()
cursor = connection.cursor(dictionary=True)

def User(request, pk):
  cursor.execute(f'select * from pengaju where Status = "Pending"')
  pengaju = cursor.fetchall()

  text = 'select PengajuId from pengaju where Status = "Pending"'

  cursor.execute(f'select * from keuanganpengaju where PengajuId = ({text})')
  keuanganPengaju = cursor.fetchall()

  cursor.execute(f'select * from scorepengaju where PengajuId = ({text})')
  scorePengaju = cursor.fetchall()

  cursor.execute(f'select * from prediksisistem where PengajuId = ({text})')
  prediksiSistem = cursor.fetchall()
  
  pengajuZip = zip(pengaju, keuanganPengaju, scorePengaju, prediksiSistem)

  cursor.execute(f'select * from pengaju where Status = "Accepted"')
  pengajuDisetujui = cursor.fetchall()

  cursor.execute(f'select * from pengaju where Status = "Declined"')
  pengajuDitolak = cursor.fetchall()

  context = {
    'pengajuZip' : pengajuZip,
    'pengajuDisetujui' : pengajuDisetujui,
    'pengajuDitolak' : pengajuDitolak,
  }

  if request.method == 'POST':
    button = request.POST.get('button')
    button = button.split('-')

    cursor.execute(f'update pengaju set Status = "{button[0]}" where PengajuId = {button[1]}')
    connection.commit()

    cursor.execute(f'select PlafondMaksimum, PermohonanKreditPengaju from keuanganpengaju where PengajuId = {button[1]}')
    result = cursor.fetchone()
    plafondmaksimum = result['PlafondMaksimum']
    permohonankreditpengaju = result['PermohonanKreditPengaju']
    # print(plafondmaksimum)

    cursor.execute(f'select ScoreTotal from scorepengaju where PengajuId = {button[1]}')
    scoretotal = cursor.fetchone()
    scoretotal = scoretotal['ScoreTotal']
    # print(scoretotal)

    if button[0] == 'Accepted':
      plafondditerima = scoretotal/10*plafondmaksimum
      if permohonankreditpengaju < plafondditerima:
        cursor.execute(f'update keuanganpengaju set PlafondDisetujui = {permohonankreditpengaju} where PengajuId = {button[1]}')
        connection.commit()
      else:
        cursor.execute(f'update keuanganpengaju set PlafondDisetujui = {plafondditerima} where PengajuId = {button[1]}')
        connection.commit()
    if button == 'Declined':
      cursor.execute(f'update keuanganpengaju set PlafondDisetujui = 0 where PengajuId = {button[1]}')
      connection.commit()
    
    context = {
      'pengajuZip' : pengajuZip,
      'pengajuDisetujui' : pengajuDisetujui,
      'pengajuDitolak' : pengajuDitolak,
    }

  return render(request, 'user/user.html', context)