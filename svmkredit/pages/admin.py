from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import utils
import pickle
from sklearn.svm import SVC

def svm():
  df = pd.read_excel('db/dataPengaju.xlsx', sheet_name='data')
  df.head

  lab = preprocessing.LabelEncoder()

  df['Status'] = lab.fit_transform(df['Status'].values)

  # X = df[['Score Usia','Score Pernikahan','Score Pendidikan','Score Tempat Tinggal','Score Transportasi','Score Jabatan','Score Keahlian','Score Lama Kerja','Score Riwayat Pindah Kerja','Score Aset Pribadi','Score Hutang di Tempat Lain','Score Kelancaran Hutang','Score Umur Perusahaan', 'Score Skala Perusahaan', 'Score Jumlah Karyawan', 'Score Total']]
  X = df[['Score Usia','Score Total']]
  y = df['Status']

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

connection = connect()
cursor = connection.cursor(dictionary=True)

def Admin(request, pk):
  classifier = svm()

  if request.method == 'POST':
    namaPengaju = request.POST.get('namaPengaju')
    print(namaPengaju)
    nikPengaju = request.POST.get('nikPengaju')
    print(nikPengaju)
    usiaPengaju = int(request.POST.get('usiaPengaju'))
    print(usiaPengaju)
    pernikahanPengaju = int(request.POST.get('pernikahanPengaju'))
    print(pernikahanPengaju)
    pendidikanPengaju = int(request.POST.get('pendidikanPengaju'))
    print(pendidikanPengaju)
    tempatTinggalPengaju = int(request.POST.get('tempatTinggalPengaju'))
    print(tempatTinggalPengaju)
    # usiaPengaju = int(request.POST.get('usiaPengaju')) #Transportasi Pengaju
    jabatanPengaju = int(request.POST.get('jabatanPengaju'))
    print(jabatanPengaju)
    keahlianPengaju = int(request.POST.get('keahlianPengaju'))
    print(keahlianPengaju)
    lamaKerjaPengaju = int(request.POST.get('lamaKerjaPengaju'))
    print(lamaKerjaPengaju)
    riwayatPindahKerjaPengaju = int(request.POST.get('riwayatPindahKerjaPengaju'))
    print(riwayatPindahKerjaPengaju)
    # usiaPengaju = int(request.POST.get('usiaPengaju')) #aset pribadi pengaju
    hutangPengajudiTempatLain = int(request.POST.get('hutangPengajudiTempatLain'))
    print(hutangPengajudiTempatLain)
    kelancaranHutangPengaju = int(request.POST.get('kelancaranHutangPengaju'))
    print(kelancaranHutangPengaju)
    # usiaPengaju = int(request.POST.get('usiaPengaju')) #umur perusahaan
    # usiaPengaju = int(request.POST.get('usiaPengaju')) #skala perusahaan
    jumlahKaryawanPerusahaanPengaju = int(request.POST.get('jumlahKaryawanPerusahaanPengaju'))
    print(jumlahKaryawanPerusahaanPengaju)

  return render(request, 'admin/admin.html')