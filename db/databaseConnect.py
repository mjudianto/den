import mysql.connector
from mysql.connector import Error
import csv
from random import randint

def connect():
  try:
      connection = mysql.connector.connect(
          host= "127.0.0.1",
          port= '3306',
          user= "root",
          password= "PkmOba_2022",
          database= "svmkredit",
          auth_plugin='mysql_native_password')
      if connection.is_connected():
        return connection

  except Error as e:
      print("Error while connecting to MySQL", e)

def selectAll(tableName, cursor):
  cursor.execute(f"SELECT * FROM {tableName}")
  result = cursor.fetchall()
  return result

def insertToTable(tableName, value, connection, cursor):
  # value = 'null, ' + value
  print(value)
  cursor.execute(f"INSERT INTO {tableName} VALUES ({value})")
  connection.commit()

def tableSeed(dataFile, tableName, connection, cursor):
  file = open(dataFile)
  csvreader = csv.reader(file)
  next(csvreader)
  for row in csvreader:
    valueString = 'null'
    counter = 0
    for r in row:
      if counter == 0:
        valueString += ', "' + r + '"'
      else:
        valueString += ',' + r 
      counter+=1
    price = randint(10000,100000)
    valueString += ',' + str(price)
    insertToTable(tableName, valueString, connection, cursor)