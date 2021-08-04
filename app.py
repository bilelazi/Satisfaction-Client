from flask import Flask,request, render_template, jsonify, redirect, url_for, session, flash
from passlib.hash import sha256_crypt

import json
import sqlite3
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

import numpy as np
import pickle


app = Flask(__name__)
app.secret_key = "Secret Key"

mdl = pickle.load(open('model.pkl','rb'))


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("classif.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/home')
def cnx():
   
      return render_template('login.html')
   
    
@app.route('/login', methods=['POST'])
def do_admin_login():
  

  conn = db_connection()
  cursor = conn.cursor()
  login= request.form.get
  username = login('username')
  password = login('password')
  data = cursor.execute('SELECT username,password FROM Admin')

  if (username=='admin' and password=='admin') :
    return redirect(url_for('statistiques'))
 

  else:
    flash("Please check your information !")
    return cnx()

    
@app.route('/')
def home():
    
    return render_template("form.html")    
    

    
    
@app.route('/client', methods=['POST'])
def add():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        new_class = request.form.get("classe", False)
        new_travel = request.form.get("travel", False)
        new_age = request.form.get("age", False)
        new_sexe = request.form.get("sexe", False)
        new_baggage = request.form.get("i", False)
        new_time = request.form.get("a", False)
        new_gate = request.form.get("f", False)
        new_seat = request.form.get("h", False)
        new_enter = request.form.get("d", False)
        new_food = request.form.get("g", False)
        new_wifi = request.form.get("b", False)
        new_booking = request.form.get("c", False)
        new_service = request.form.get("e", False) 
        new_comm = request.form.get("comm", False)
      
        pred = mdl.predict([new_time, new_gate, new_baggage, new_seat, new_enter, new_food,  new_wifi, new_booking, new_service])
  
   
        sql = """INSERT INTO client (classe, travel, age, sexe, baggage, time, gate, seat, intertainment, food, wifi, booking, service, commentaire, satisfaction)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        val = (new_class, new_travel, new_age, new_sexe, new_baggage, new_time, new_gate, new_seat, new_enter, new_food, new_wifi, new_booking, new_service, new_comm, pred)
        cursor.execute(sql, val)
        conn.commit()
        flash("Insert successfully ")

      
        return render_template('form.html', data=pred)
  


@app.route('/dec')
def decideur():
    
    return render_template("admin.html")
  
@app.route('/admin', methods=['GET'])
def getAll():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":

        cursor.execute('SELECT * FROM client')
        data = cursor.fetchall()
       
       # clients = [
        #    dict(id=row[0], classe=row[1], travel=row[2], age=row[3], sexe=row[4], baggage=row[5], time=row[6], gate=row[7], seat=row[8], intertainment=row[9], food=row[10], wifi=row[11], booking=row[12], service=row[13], commentaire=row[14], satisfaction=row[15])
         #   for row in cursor.fetchall()
       # ]
        #if clients is not None:
          # return jsonify(clients)
    return render_template('admin.html', clients=data)
    
@app.route("/client/<int:id>", methods=["GET"])
def getOne(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM client where id=?",id)
        client = cursor.fetchone()
        print(client)
      
    
        return redirect(url_for('getOne(id'), client = client)

    
    

@app.route('/chart')
def statistiques(): 
     conn = db_connection()
     cursor = conn.cursor()
     cursor.execute('SELECT  classe,  count(satisfaction) FROM client where satisfaction="satisfied" group by classe')
     data=cursor.fetchall()
     labels = [row[0] for row in data]
     values = [row[1] for row in data]
     
     cursor.execute('SELECT  classe,  count(satisfaction) FROM client where satisfaction="neutral or dissatisfied" group by classe')
     data1=cursor.fetchall()
     label = [row[0] for row in data1]
     value = [row[1] for row in data1]
     
     cursor.execute(' SELECT  sexe,  count(satisfaction) FROM client where satisfaction="neutral or dissatisfied" group by sexe')
     data2=cursor.fetchall()
     label1 = [row[0] for row in data2]
     value1 = [row[1] for row in data2]
     
     cursor.execute(' SELECT   count(satisfaction) FROM client group by satisfaction')
     data3 = cursor.fetchall()
     label2 = [row[0] for row in data3]
     return render_template("chart.html", labels=labels, values=values, x=label,y=value,x1=label1, y1=value1, x2=label2) 
     

  
   

    


    
    


    
  

 
    
   
    
if __name__ == '__main__':
    app.run(debug=True)