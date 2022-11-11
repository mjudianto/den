from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView
from db.databaseConnect import *

connection = connect()
cursor = connection.cursor(dictionary=True)

def User(request, pk):
  return render(request, 'user/user.html')