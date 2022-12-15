from django.shortcuts import render
from db.databaseConnect import *
from django.contrib import messages
import json
import pandas as pd
from sklearn import preprocessing


def User(request, pk):
  connection = connect()
  cursor = connection.cursor(dictionary=True)
  
  df = pd.read_excel('db/dataPengaju.xlsx', sheet_name='data')
  dataStatus = df['Status']
  dataNama = df['Nama']
  dataScoreUsia = df['Score Usia']
  dataScorePernikahan = df['Score Pernikahan']
  dataScorePendidikan = df['Score Pendidikan']
  dataScoreTempatTinggal = df['Score Tempat Tinggal']
  dataScoreTransportasi = df['Score Transportasi']
  dataScoreJabatan = df['Score Jabatan']
  dataScoreKeahlian = df['Score Keahlian']
  dataScoreLamaKerja = df['Score Lama Kerja']
  dataScoreRiwayatPindahKerja = df['Score Riwayat Pindah Kerja']
  dataScoreAsetPribadi = df['Score Aset Pribadi']
  dataScoreHutangdiTempatLain = df['Score Hutang di Tempat Lain']
  dataScoreKelancaranHutang = df['Score Kelancaran Hutang']
  dataScoreJumlahKaryawan = df['Score Jumlah Karyawan']
  dataScoreTotal = df['Score Total']

  datazip = zip(dataStatus, dataNama, dataScoreUsia, dataScorePernikahan, dataScorePendidikan, dataScoreTempatTinggal, dataScoreTransportasi, dataScoreJabatan, dataScoreKeahlian, dataScoreLamaKerja, dataScoreRiwayatPindahKerja, dataScoreAsetPribadi, dataScoreHutangdiTempatLain, dataScoreKelancaranHutang, dataScoreJumlahKaryawan, dataScoreTotal)

  cursor.execute(f'select * from pengaju where Status = "Pending"')
  pengaju = cursor.fetchall()
  # print(pengaju)

  text = 'select PengajuId from pengaju where Status = "Pending"'
  cursor.execute('select PengajuId from pengaju where Status = "Pending"')
  pengajuId = cursor.fetchall()

  keuanganPengaju = []
  scorePengaju = []
  prediksiSistem = []

  for p in pengajuId:
    id = p['PengajuId']

    cursor.execute(f'select * from keuanganpengaju where PengajuId = {id}')
    data = cursor.fetchone()
    keuanganPengaju.append(data)

    cursor.execute(f'select * from scorepengaju where PengajuId = {id}')
    data = cursor.fetchone()
    scorePengaju.append(data)

    cursor.execute(f'select * from prediksisistem where PengajuId = {id}')
    data = cursor.fetchone()
    prediksiSistem.append(data)
  
  pengajuZip = zip(pengaju, keuanganPengaju, scorePengaju, prediksiSistem)

  cursor.execute(f'select * from pengaju where Status = "Accepted"')
  pengajuDisetujui = cursor.fetchall()
  
  keuanganPengajuDisetujui = []
  for pdisetujui in pengajuDisetujui:
    cursor.execute(f'select * from keuanganpengaju where PengajuId = {pdisetujui["PengajuId"]}')
    dummy = cursor.fetchone()
    keuanganPengajuDisetujui.append(dummy)

  cursor.execute(f'select * from pengaju where Status = "Declined"')
  pengajuDitolak = cursor.fetchall()

  keuanganPengajuDitolak = []
  for pditolak in pengajuDitolak:
    cursor.execute(f'select * from keuanganpengaju where PengajuId = {pditolak["PengajuId"]}')
    dummy = cursor.fetchone()
    keuanganPengajuDitolak.append(dummy)
  
  pengajuDitolakjs = json.dumps(pengajuDitolak)
  pengajuDisetujuijs = json.dumps(pengajuDisetujui)
  pengajuDisetujui = zip(pengajuDisetujui, keuanganPengajuDisetujui)
  pengajuDitolak = zip(pengajuDitolak, keuanganPengajuDitolak)

  admin = selectAll('admin', cursor)

  adminjs = json.dumps(admin)
  scorejs = json.dumps(scorePengaju)
  keuanganpengaju = json.dumps(keuanganPengaju)
  
  
  context = {
    'pengajuZip' : pengajuZip,
    'pengajuDisetujui' : pengajuDisetujui,
    'pengajuDitolak' : pengajuDitolak,
    'admin' : admin,
    'adminjs' : adminjs,
    'scorejs' : scorejs,
    'df' : df,
    'keuanganpengaju' :keuanganpengaju,
    'datazip' : datazip,
    'pengajuDitolakjs' : pengajuDitolakjs,
    'pengajuDisetujuijs' : pengajuDisetujuijs,
  }

  if request.method == 'POST':
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    
    button = request.POST.get('button')
    button = button.split('-')
    # print(button[0])

    if button[0] == 'Accepted' or button[0] == 'Declined':
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

    if button[0] == 'admin':
      email = request.POST.get('email')
      password = email
      telp = ''
      telp = request.POST.get('telp')
      if telp == None or telp == '':
          telp = 'null'
          value = 'null' + ', "' + email + '" , "' + password + '" ,' + telp
      else:
          value = 'null' + ', "' + email + '" , "' + password + '" , "' + telp + '"'
      # print(value)
      insertToTable(button[0], value, connection, cursor)
    
    if button[0] == 'delete':
      cursor.execute(f'delete from admin where AdminId = {button[1]}')
      connection.commit()
    
    # if button[0] == 'updateAdmin':
    #   updateAdminId = request.POST.get('updateAdminId')
    #   email = request.POST.get('updateEmail')
    #   password = request.POST.get('updatePassword')
    #   confirmpassword = request.POST.get('updateConfirmpassword')
    #   telp = ''
    #   telp = request.POST.get('updateTelp')

    #   # print(updateAdminId)
    #   if password == confirmpassword:
    #       if telp == None or telp == '':
    #         telp = 'null'
    #         cursor.execute(f'update admin set Email = "{email}", Password = "{password}", NoTelp = {telp} where AdminId = {updateAdminId}')
    #         connection.commit()
    #       else:
    #         cursor.execute(f'update admin set Email = "{email}", Password = "{password}", NoTelp = "{telp}" where AdminId = {updateAdminId}')
    #         connection.commit()
    
    if button[0] == 'reset':
      cursor.execute(f'select Email from admin where AdminId = {button[1]}')
      defaultpass = cursor.fetchone() 
      defaultpass = defaultpass['Email']
      cursor.execute(f'update admin set Password = "{defaultpass}" where AdminId = {button[1]}')
      connection.commit()

    cursor.execute(f'select * from pengaju where Status = "Pending"')
    pengaju = cursor.fetchall()
    # print(pengaju)

    text = 'select PengajuId from pengaju where Status = "Pending"'
    cursor.execute('select PengajuId from pengaju where Status = "Pending"')
    pengajuId = cursor.fetchall()

    keuanganPengaju = []
    scorePengaju = []
    prediksiSistem = []

    for p in pengajuId:
      id = p['PengajuId']

      cursor.execute(f'select * from keuanganpengaju where PengajuId = {id}')
      data = cursor.fetchone()
      keuanganPengaju.append(data)

      cursor.execute(f'select * from scorepengaju where PengajuId = {id}')
      data = cursor.fetchone()
      scorePengaju.append(data)

      cursor.execute(f'select * from prediksisistem where PengajuId = {id}')
      data = cursor.fetchone()
      prediksiSistem.append(data)
    
    pengajuZip = zip(pengaju, keuanganPengaju, scorePengaju, prediksiSistem)

    cursor.execute(f'select * from pengaju where Status = "Accepted"')
    pengajuDisetujui = cursor.fetchall()
    keuanganPengajuDisetujui = []
    for pdisetujui in pengajuDisetujui:
      cursor.execute(f'select * from keuanganpengaju where PengajuId = {pdisetujui["PengajuId"]}')
      dummy = cursor.fetchone()
      keuanganPengajuDisetujui.append(dummy)

    cursor.execute(f'select * from pengaju where Status = "Declined"')
    pengajuDitolak = cursor.fetchall()

    keuanganPengajuDitolak = []
    for pditolak in pengajuDitolak:
      cursor.execute(f'select * from keuanganpengaju where PengajuId = {pditolak["PengajuId"]}')
      dummy = cursor.fetchone()
      keuanganPengajuDitolak.append(dummy)

    
    pengajuDitolakjs = json.dumps(pengajuDitolak)
    pengajuDisetujuijs = json.dumps(pengajuDisetujui)
    
    pengajuDisetujui = zip(pengajuDisetujui, keuanganPengajuDisetujui)
    pengajuDitolak = zip(pengajuDitolak, keuanganPengajuDitolak)
    
    admin = selectAll('admin', cursor)

    adminjs = json.dumps(admin)
    scorejs = json.dumps(scorePengaju)
    keuanganpengaju = json.dumps(keuanganPengaju)
    

    context = {
      'pengajuZip' : pengajuZip,
      'pengajuDisetujui' : pengajuDisetujui,
      'pengajuDitolak' : pengajuDitolak,
      'admin' : admin,
      'adminjs' : adminjs,
      'scorejs' : scorejs,
      'df' : df,
      'keuanganpengaju' : keuanganpengaju,
      'datazip' : datazip,
      'pengajuDitolakjs' : pengajuDitolakjs,
      'pengajuDisetujuijs' : pengajuDisetujuijs,
    }

  return render(request, 'master/master.html', context)