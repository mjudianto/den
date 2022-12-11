from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *
from django.contrib import messages

import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC

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
    button = request.POST.get('button')

    if button == 'ajuan':
      namaPengaju = request.POST.get('namaPengaju')
      nikPengaju = request.POST.get('nikPengaju')

      insertToTable('pengaju', f'null, "{namaPengaju}", "{nikPengaju}", {pk}, "Pending"', connection, cursor)

      kreditPengaju = int(request.POST.get('kreditPengaju'))
      jangkaWaktuKredit = int(request.POST.get('jangkaWaktuKredit'))
      totalPendapatanPengaju = int(request.POST.get('totalPendapatanPengaju')) if request.POST.get('totalPendapatanPengaju') != '' and request.POST.get('totalPendapatanPengaju') != None else 0
      totalBiayaPengaju = int(request.POST.get('totalBiayaPengaju')) if request.POST.get('totalBiayaPengaju') != '' and request.POST.get('totalBiayaPengaju') != None else 0

      maksimumAngsuran = (totalPendapatanPengaju - totalBiayaPengaju)*75/100
      print(maksimumAngsuran)
      bunga = 1.58
      plafondMaksimum = (maksimumAngsuran*jangkaWaktuKredit)/(1+(bunga*jangkaWaktuKredit))
      
      cursor.execute(f"SELECT PengajuId FROM pengaju where NIK = '{nikPengaju}'")
      idPengaju = cursor.fetchone()

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