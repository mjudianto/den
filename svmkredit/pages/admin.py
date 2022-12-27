from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC

import random

def svm():
  df = pd.read_excel('db/dataPengaju.xlsx', sheet_name='data')
  df.head

  lab = preprocessing.LabelEncoder()

  df['Status'] = lab.fit_transform(df['Status'].values)

  X = df[['Score Usia','Score Pernikahan','Score Pendidikan','Score Tempat Tinggal','Score Transportasi','Score Jabatan','Score Keahlian','Score Lama Kerja','Score Riwayat Pindah Kerja','Score Aset Pribadi','Score Hutang di Tempat Lain','Score Kelancaran Hutang', 'Score Jumlah Karyawan', 'Score Total']]
  # X = df[['Score Usia','Score Total']]
  y = df['Status']
  # print(y.head)

  # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

  #menggunakan SVM library untuk membuat SVM classifier
  classifier = SVC(kernel = 'linear')

  #memasukkan training data kedalam classifier
  classifier.fit(X, y)

  #memasukkan testing data ke variabel y_predict
  # y_predict = classifier.predict(X_test)

  #menampilkan classification report
  # print(classification_report(y_test, y_predict))

  # print('Hasil Prediksi : ', y_predict)

  # prediksiBenar = (y_predict == y_test).sum()
  # prediksiSalah = (y_predict != y_test).sum()
  # print('Prediksi Benar : ', prediksiBenar)
  # print('Prediksi Salah : ', prediksiSalah)
  # print('Akurasi : ', prediksiBenar/(prediksiBenar+prediksiSalah)*100, '%')

  # filename = 'db/svmPengaju.sav'
  # pickle.dump(classifier, open(filename, 'wb'))

  # loaded_model = pickle.load(open(filename, 'rb'))
  # newData = pd.read_excel('/content/drive/MyDrive/google_colab/data/data copy.xlsx', sheet_name='data')
  # newX = newData[['Score Usia','Score Pernikahan','Score Pendidikan','Score Tempat Tinggal','Score Transportasi','Score Jabatan','Score Keahlian','Score Lama Kerja','Score Riwayat Pindah Kerja','Score Aset Pribadi','Score Hutang di Tempat Lain','Score Kelancaran Hutang','Score Umur Perusahaan', 'Score Skala Perusahaan', 'Score Jumlah Karyawan']]
  # X = df[['Score Usia','Score Pernikahan','Score Pendidikan','Score Tempat Tinggal','Score Transportasi','Score Jabatan','Score Keahlian','Score Lama Kerja','Score Riwayat Pindah Kerja','Score Aset Pribadi','Score Hutang di Tempat Lain','Score Kelancaran Hutang','Score Umur Perusahaan', 'Score Skala Perusahaan', 'Score Jumlah Karyawan']]


  # newData['Status'] = lab.fit_transform(newData['Status'].values)
  # newY = newData['Status']

  # test = [[9,4]]
  # print(newX)

  # result = loaded_model.score(newX, newY)
  # result = classifier.predict(test)
  # print(result)

  return classifier



def Admin(request, pk):
  connection = connect()
  cursor = connection.cursor(dictionary=True)

  classifier = svm()

  # masukin data dari excel
  # df = pd.read_excel('db/dataPengaju.xlsx', sheet_name='data')
  # dataNama = df['Nama']
  # dataScoreUsia = df['Score Usia']
  # dataScorePernikahan = df['Score Pernikahan']
  # dataScorePendidikan = df['Score Pendidikan']
  # dataScoreTempatTinggal = df['Score Tempat Tinggal']
  # dataScoreTransportasi = df['Score Transportasi']
  # dataScoreJabatan = df['Score Jabatan']
  # dataScoreKeahlian = df['Score Keahlian']
  # dataScoreLamaKerja = df['Score Lama Kerja']
  # dataScoreRiwayatPindahKerja = df['Score Riwayat Pindah Kerja']
  # dataScoreAsetPribadi = df['Score Aset Pribadi']
  # dataScoreHutangdiTempatLain = df['Score Hutang di Tempat Lain']
  # dataScoreKelancaranHutang = df['Score Kelancaran Hutang']
  # dataScoreJumlahKaryawan = df['Score Jumlah Karyawan']
  # # print(dataNama[0])

  # for i in range(759):
  #   arr1 = []
  #   arr2 = []
  #   nikPengaju = '{:0>16}'.format(i)
  #   insertToTable('pengaju', f'null, "{dataNama[i]}", "{nikPengaju}", {pk}, "Pending"', connection, cursor)

  #   totalPendapatanPengaju = random.randint(10000000,50000000)
  #   totalBiayaPengaju = random.randint(1000000,10000000)
  #   kreditPengaju = random.randint(1000000,20000000)
  #   jangkaWaktuKredit = random.randint(1,36)

  #   maksimumAngsuran = (totalPendapatanPengaju - totalBiayaPengaju)*75/100
  #   bunga = 1.58
  #   plafondMaksimum = (maksimumAngsuran*jangkaWaktuKredit)/(1+(bunga*jangkaWaktuKredit))

  #   insertToTable('keuanganpengaju', f'null, {totalPendapatanPengaju}, {totalBiayaPengaju}, {kreditPengaju}, {jangkaWaktuKredit}, {i+1}, {plafondMaksimum}, null', connection, cursor)

  #   character = 35/100*((dataScoreHutangdiTempatLain[i]+dataScoreKelancaranHutang[i]+dataScoreRiwayatPindahKerja[i]+dataScorePernikahan[i])/40*10)
  #   capacity = 25/100*((dataScoreUsia[i]+dataScorePendidikan[i]+dataScoreLamaKerja[i]+dataScoreJabatan[i]+dataScoreKeahlian[i])/50*10)
  #   capital = 20/100*((dataScoreTempatTinggal[i]+dataScoreTransportasi[i]+dataScoreAsetPribadi[i])/30*10)
  #   conditionOfEconomics = 20/100*((dataScoreJumlahKaryawan[i])/10*10)
  #   scoreTotal = character+capacity+capital+conditionOfEconomics

  #   insertToTable('scorepengaju', f'null, {dataScoreUsia[i]}, {dataScorePernikahan[i]}, {dataScorePendidikan[i]}, {dataScoreTempatTinggal[i]}, {dataScoreTransportasi[i]}, {dataScoreJabatan[i]}, {dataScoreKeahlian[i]}, {dataScoreLamaKerja[i]}, {dataScoreRiwayatPindahKerja[i]}, {dataScoreAsetPribadi[i]}, {dataScoreHutangdiTempatLain[i]}, {dataScoreKelancaranHutang[i]}, {dataScoreJumlahKaryawan[i]}, {scoreTotal}, {i+1}', connection, cursor)

  #   arr2 = [dataScoreUsia[i], dataScorePernikahan[i], dataScorePendidikan[i], dataScoreTempatTinggal[i], dataScoreTransportasi[i], dataScoreJabatan[i], dataScoreKeahlian[i], dataScoreLamaKerja[i], dataScoreRiwayatPindahKerja[i], dataScoreAsetPribadi[i], dataScoreHutangdiTempatLain[i], dataScoreKelancaranHutang[i], dataScoreJumlahKaryawan[i], scoreTotal]
  #   arr1.append(arr2)
  #   prediction = "Diterima" if classifier.predict(arr1)[0] == 0 else "Ditolak"
  #   # print("prediction : ", prediction)
  #   insertToTable('prediksisistem', f'null, "{prediction}", {i+1}', connection, cursor)




  cursor.execute(f'select * from pengaju where AdminId = {pk}')
  pengaju = cursor.fetchall()
  keuanganPengaju = []

  for p in pengaju:
    p = p['PengajuId']
    cursor.execute(f'select * from keuanganPengaju where PengajuId = {p} ')
    result = cursor.fetchone()
    keuanganPengaju.append(result)

  pengajuZip = zip(pengaju, keuanganPengaju)

  context = {
    'pengajuZip' : pengajuZip,
    'pk' : pk,
  }


  if request.method == 'POST':
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    
    button = request.POST.get('button')

    if button == 'ajuan':
      namaPengaju = request.POST.get('namaPengaju')
      nikPengaju = request.POST.get('nikPengaju')

      insertToTable('pengaju', f'null, "{namaPengaju}", "{nikPengaju}", {pk}, "Pending"', connection, cursor)
      cursor.execute(f"SELECT PengajuId FROM pengaju where NIK = '{nikPengaju}'")
      idPengaju = cursor.fetchone()

      try:
        ktp = request.FILES['ktp']
        fs = FileSystemStorage(location='static/images/ktp')
        filename = fs.save(ktp.name, ktp)
        ktp = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{ktp}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM KTP')
        return render(request, 'admin/admin.html', context)
      try:
        suratNikah = request.FILES['suratNikah']
        fs = FileSystemStorage(location='static/images/suratNikah')
        filename = fs.save(suratNikah.name, suratNikah)
        suratNikah = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{suratNikah}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM SURAT NIKAH')
        return render(request, 'admin/admin.html', context)
      try:
        ijazah = request.FILES['ijazah']
        fs = FileSystemStorage(location='static/images/ijazah')
        filename = fs.save(ijazah.name, ijazah)
        ijazah = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{ijazah}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM IJAZAH')
        return render(request, 'admin/admin.html', context)
      try:
        fotoRumah = request.FILES['fotoRumah']
        fs = FileSystemStorage(location='static/images/fotoRumah')
        filename = fs.save(fotoRumah.name, fotoRumah)
        fotoRumah = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{fotoRumah}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM FOTO RUMAH')
        return render(request, 'admin/admin.html', context)
      try:
        slikBi = request.FILES['slikBi']
        fs = FileSystemStorage(location='static/images/slikBi')
        filename = fs.save(slikBi.name, slikBi)
        slikBi = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{slikBi}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM SLIK BI')
        return render(request, 'admin/admin.html', context)
      try:
        suratKeteranganKantor = request.FILES['suratKeteranganKantor']
        fs = FileSystemStorage(location='static/images/suratKeteranganKantor')
        filename = fs.save(suratKeteranganKantor.name, suratKeteranganKantor)
        suratKeteranganKantor = fs.url(filename)
        insertToTable('gambar', f'null, "{idPengaju["PengajuId"]}", "{suratKeteranganKantor}"', connection, cursor)

      except:
        messages.info(request, 'MOHON UNTUK MENGISI KOLOM SURAT KETERANGAN KANTOR')
        return render(request, 'admin/admin.html', context)

      kreditPengaju = int(request.POST.get('kreditPengaju'))
      jangkaWaktuKredit = int(request.POST.get('jangkaWaktuKredit'))
      totalPendapatanPengaju = int(request.POST.get('totalPendapatanPengaju')) if request.POST.get('totalPendapatanPengaju') != '' and request.POST.get('totalPendapatanPengaju') != None else 0
      totalBiayaPengaju = int(request.POST.get('totalBiayaPengaju')) if request.POST.get('totalBiayaPengaju') != '' and request.POST.get('totalBiayaPengaju') != None else 0

      maksimumAngsuran = (totalPendapatanPengaju - totalBiayaPengaju)*75/100
      bunga = 1.58
      plafondMaksimum = (maksimumAngsuran*jangkaWaktuKredit)/(1+(bunga*jangkaWaktuKredit))
      
      

      insertToTable('keuanganpengaju', f'null, {totalPendapatanPengaju}, {totalBiayaPengaju}, {kreditPengaju}, {jangkaWaktuKredit}, {idPengaju["PengajuId"]}, {plafondMaksimum}, null', connection, cursor)

      arr1 = []
      arr2 = []

      usiaPengaju = int(request.POST.get('usiaPengaju'))
      arr2.append(usiaPengaju)
      pernikahanPengaju = int(request.POST.get('pernikahanPengaju'))
      arr2.append(pernikahanPengaju)
      pendidikanPengaju = int(request.POST.get('pendidikanPengaju'))
      arr2.append(pendidikanPengaju)
      tempatTinggalPengaju = int(request.POST.get('tempatTinggalPengaju'))
      arr2.append(tempatTinggalPengaju)
      transportasiPengaju = int(request.POST.get('transportasiPengaju'))
      arr2.append(transportasiPengaju)
      jabatanPengaju = int(request.POST.get('jabatanPengaju'))
      arr2.append(jabatanPengaju)
      keahlianPengaju = int(request.POST.get('keahlianPengaju'))
      arr2.append(keahlianPengaju)
      lamaKerjaPengaju = int(request.POST.get('lamaKerjaPengaju'))
      arr2.append(lamaKerjaPengaju)
      riwayatPindahKerjaPengaju = int(request.POST.get('riwayatPindahKerjaPengaju'))
      arr2.append(riwayatPindahKerjaPengaju)
      asetPribadiPengaju = int(request.POST.get('asetPribadiPengaju')) 
      arr2.append(asetPribadiPengaju)
      hutangPengajudiTempatLain = int(request.POST.get('hutangPengajudiTempatLain'))
      arr2.append(hutangPengajudiTempatLain)
      kelancaranHutangPengaju = int(request.POST.get('kelancaranHutangPengaju'))
      arr2.append(kelancaranHutangPengaju)
      jumlahKaryawanPerusahaanPengaju = int(request.POST.get('jumlahKaryawanPerusahaanPengaju'))
      arr2.append(jumlahKaryawanPerusahaanPengaju)

      character = 35/100*((hutangPengajudiTempatLain+kelancaranHutangPengaju+riwayatPindahKerjaPengaju+pernikahanPengaju)/40*10)
      capacity = 25/100*((usiaPengaju+pendidikanPengaju+lamaKerjaPengaju+jabatanPengaju+keahlianPengaju)/50*10)
      capital = 20/100*((tempatTinggalPengaju+transportasiPengaju+asetPribadiPengaju)/30*10)
      conditionOfEconomics = 20/100*((jumlahKaryawanPerusahaanPengaju)/10*10)

      scoreTotal = character+capacity+capital+conditionOfEconomics
      arr2.append(scoreTotal)

      insertToTable('scorepengaju', f'null, {usiaPengaju}, {pernikahanPengaju}, {pendidikanPengaju}, {tempatTinggalPengaju}, {transportasiPengaju}, {jabatanPengaju}, {keahlianPengaju}, {lamaKerjaPengaju}, {riwayatPindahKerjaPengaju}, {asetPribadiPengaju}, {hutangPengajudiTempatLain}, {kelancaranHutangPengaju}, {jumlahKaryawanPerusahaanPengaju}, {scoreTotal}, {idPengaju["PengajuId"]}', connection, cursor)


      arr1.append(arr2)
      prediction = "Diterima" if classifier.predict(arr1)[0] == 0 else "Ditolak"
      # print("prediction : ", prediction)
      insertToTable('prediksisistem', f'null, "{prediction}", {idPengaju["PengajuId"]}', connection, cursor)
      # print("score total : ", scoreTotal)
      messages.info(request, 'Data Anda Berhasil Disimpan')

      cursor.execute(f'select * from pengaju where AdminId = {pk}')
      pengaju = cursor.fetchall()
      keuanganPengaju = []

      for p in pengaju:
        p = p['PengajuId']
        cursor.execute(f'select * from keuanganPengaju where PengajuId = {p} ')
        result = cursor.fetchone()
        keuanganPengaju.append(result)

      pengajuZip = zip(pengaju, keuanganPengaju)

      context = {
        'pengajuZip' : pengajuZip,
        'pk' : pk,
      }
    
    if button == 'cp':
      currentPassword = request.POST.get('currentPassword')
      cursor.execute(f'select Password from admin where AdminId = {pk}')
      adminpass = cursor.fetchone()

      if currentPassword == adminpass['Password']:
        NewPassword = request.POST.get('NewPassword')
        confirmNewPassword = request.POST.get('confirmNewPassword')
        if NewPassword == confirmNewPassword:
          cursor.execute(f'update admin set Password = "{NewPassword}" where AdminId = {pk}')
          connection.commit()
          messages.info(request, 'Password Change Successfully')
        else:
          messages.info(request, 'Please Match New Password With Confirm New Password')
      else:
        messages.info(request, 'Current Password is Incorect')
      
      context = {
        'pengajuZip' : pengajuZip,
        'pk' : pk,
      }

  return render(request, 'admin/admin.html', context)