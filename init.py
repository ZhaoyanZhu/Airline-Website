from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

app=Flask(__name__)

conn=pymysql.connect(host="localhost",
                     user="root",
                     password="",
                     db="air_ticket",
                     charset="utf8mb4",
                     cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/search_future_trip')
def search_future_trip():
    return render_template('search_future_trip.html')

@app.route('/flight_status')
def flight_status():
    return render_template('flight_status.html')

@app.route('/cusregister')
def cusregister():
    return render_template('cusregister.html')

@app.route('/staffregister')
def staffregister():
    return render_template('staffregister.html')

@app.route('/cuslogin')
def cuslogin():
    return render_template('cuslogin.html')

@app.route('/stafflogin')
def stafflogin():
    return render_template('stafflogin.html')

@app.route('/cusviewFlight')
def cusviewFlight():
    return render_template('cusviewFlight.html')

@app.route('/cus_search_flight')
def cus_search_flight():
    return render_template('cus_search_flight.html')

@app.route('/cus_ratecomment')
def cus_ratecomment():
    return render_template('cus_ratecomment.html')


    
    

@app.route('/search_future_trip_EXCE',methods=['GET','POST'])
def search_future_trip_EXCE():
    source_city=request.form["Source City"]
    source_airport_name=request.form["Source Airport"]
    des_city=request.form["Destination City"]
    des_airport_name=request.form["Destination Airport"]
    depature_date=request.form["Depature Date"]
    return_date=request.form["Return Date"]
    cursor=conn.cursor()
    query="SELECT airline_name, flight_num, depature_date, depature_time,T.name,T.city,S.name,S.city \
FROM flight,airport as T, airport as S \
WHERE depature_airport=T.code and arrival_airport=S.code and T.city= %s and T.name= %s \
and S.city= %s and S.name= %s and depature_date= %s"
    cursor.execute(query,(source_city,source_airport_name,des_city,des_airport_name,depature_date))
    data=cursor.fetchall()
    cursor.execute(query,(des_city,des_airport_name,source_city,source_airport_name,return_date))
    data1=cursor.fetchall()
    cursor.close()
    return render_template("search_future_trip.html",posts=data,posts1=data1)

@app.route('/flight_status_EXCE',methods=['GET','POST'])
def flight_status_EXCE():
    airline_name=request.form["Airline Name"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    cursor=conn.cursor()
    query="SELECT airline_name, flight_num, depature_date, depature_time, flight_status \
FROM flight WHERE airline_name= %s and flight_num= %s and depature_date= %s"
    cursor.execute(query,(airline_name,flight_num,depature_date))
    data=cursor.fetchall()
    cursor.close()
    return render_template("flight_status.html",posts=data)

@app.route('/cusregisterAuth',methods=['GET','POST'])
def cusregisterAuth():
    username=request.form['Email']
    name=request.form["Name"]
    password=request.form['Password']
    building_num=request.form["Building Number"]
    street=request.form["Street"]
    city=request.form["City"]
    state=request.form["State"]
    phone=request.form["Phone Number"]
    passport_num=request.form["Passport Number"]
    exp=request.form["EXP Date"]
    country=request.form["Country"]
    dob=request.form["Date Of Birth"]
    cursor=conn.cursor()
    query="SELECT * FROM customer WHERE email= %s"
    cursor.execute(query,(username))
    data=cursor.fetchone()
    error=None
    if(data):
        error="This customer already exists"
        return render_template('cusregister.html',error=error)
    else:
        ins="INSERT INTO customer VALUES(%s,%s,md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(ins,(username,name,password,building_num,street,city,state,phone,passport_num,exp,country,dob))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/staffregisterAuth',methods=['GET','POST'])
def staffregisterAuth():
    username=request.form['Email']
    password=request.form['Password']
    fname=request.form["First Name"]
    lname=request.form["Last Name"]
    dob=request.form["Date Of Birth"]
    airline_name=request.form["Airline Name"]
    phone=request.form["Phone"]
    cursor=conn.cursor()
    query="SELECT * FROM airline WHERE airline_name= %s"
    cursor.execute(query,(airline_name))
    data=cursor.fetchone()
    error=None
    if(not data):
        error="This airline doesn't exist. Please check again!"
        return render_template('staffregister.html',error=error)
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data1=cursor.fetchone()
    if(data1):
        error="This staff already exists"
        return render_template('staffregister.html',error=error)
    else:
        ins="INSERT INTO staff VALUES(%s,md5(%s),%s,%s,%s,%s)"
        cursor.execute(ins,(username,password,fname,lname,dob,airline_name))
        conn.commit()
        phone_lst=phone.split(",")
        for elem in phone_lst:
            query="INSERT INTO staff_phone VALUES(%s,%s)"
            cursor.execute(query,(username,elem.strip()))
            conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/cusloginAuth',methods=['GET','POST'])
def cusloginAuth():
    username=request.form['Username']
    password=request.form['Password']
    cursor=conn.cursor()
    query="SELECT * FROM customer WHERE email=%s"
    cursor.execute(query,(username))
    data=cursor.fetchone()
    error=None
    if (not data):
        error="Invalid Username"
        cursor.close()
        return render_template('cuslogin.html',error=error)
    query="SELECT * FROM customer \
WHERE email=%s and customer_password = md5(%s)"
    cursor.execute(query,(username,password))
    data1=cursor.fetchone()
    cursor.close()
    if(data1):
         session['Username']=username
         return redirect(url_for('cushome'))
    else:
        error="Invalid Password"
        return render_template('cuslogin.html',error=error)

@app.route('/staffloginAuth', methods=['GET','POST'])
def staffloginAuth():
    username=request.form['Username']
    password=request.form['Password']
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchone()
    error=None
    if (not data):
        error="Invalid Username"
        cursor.close()
        return render_template('stafflogin.html',error=error)
    query="SELECT * FROM staff \
WHERE user_name=%s and staff_password = md5(%s)"
    cursor.execute(query,(username,password))
    data1=cursor.fetchone()
    cursor.close()
    if(data1):
         session['Username']=username
         return redirect(url_for('staffhome'))
    else:
        error="Invalid Password"
        return render_template('stafflogin.html',error=error)

@app.route('/cushome')
def cushome():
    username=session["Username"]
    cursor=conn.cursor()
    query="SELECT airline_name, flight_num, depature_date, depature_time \
from purchase NATURAL JOIN ticket \
where email=%s and (depature_date>current_date or (depature_date=current_date \
and depature_time>current_time))"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    cursor.close()
    return render_template('cushome.html',username=username,posts=data)

@app.route('/cusviewFlight_EXCE', methods=['GET','POST'])
def cusviewFlight_EXCE():
    username=session["Username"]
    date1=request.form["From Date"]
    date2=request.form["To Date"]
    source_airport=request.form["Source Airport"]
    des_airport=request.form["Destination Airport"]
    cursor=conn.cursor()
    query="SELECT airline_name, flight_num, depature_date, depature_time, T.name, T.city, \
S.name, S.city \
from purchase NATURAL JOIN ticket NATURAL JOIN flight, airport T, airport S \
WHERE depature_airport=T.code and arrival_airport=S.code and email=%s \
and (depature_date>=%s and depature_date<=%s) and T.name=%s and S.name=%s"
    cursor.execute(query,(username,date1,date2,source_airport,des_airport))
    data=cursor.fetchall()
    cursor.close()
    return render_template('cusviewFlight.html',posts=data)


@app.route('/cus_search_flight_EXCE',methods=['GET','POST'])
def cus_search_flight_EXCE():
    source_city=request.form["Source City"]
    source_airport_name=request.form["Source Airport"]
    des_city=request.form["Destination City"]
    des_airport_name=request.form["Destination Airport"]
    depature_date=request.form["Depature Date"]
    return_date=request.form["Return Date"]
    cursor=conn.cursor()
    query="SELECT airline_name, flight_num, depature_date, depature_time,T.name, T.city,S.name, S.city \
FROM flight,airport as T, airport as S \
WHERE depature_airport=T.code and arrival_airport=S.code and T.city= %s and T.name= %s \
and S.city= %s and S.name= %s and depature_date= %s"
    cursor.execute(query,(source_city,source_airport_name,des_city,des_airport_name,depature_date))
    data=cursor.fetchall()
    cursor.execute(query,(des_city,des_airport_name,source_city,source_airport_name,return_date))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('/cus_search_flight.html',posts=data,posts1=data1)


@app.route('/cus_purchase',methods=['GET','POST'])
def cus_purchase():
    airline_name=request.form["Airline Name"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date1"]
    depature_time=request.form["Depature Time"]
    cursor=conn.cursor()
    error=None
    query="SELECT count(*) as seat_taken \
FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data1=cursor.fetchall()
    seat_taken=data1[0]["seat_taken"]
    print("seat taken:",seat_taken)
    query="SELECT base_price,num_seat \
FROM flight NATURAL JOIN airplane \
WHERE airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s and \
(depature_date>current_date or (depature_date=current_date and depature_time>current_time))"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data2=cursor.fetchall()
    if (not data2):
        cursor.close()
        error="Please Enter The Correct Information"
        return render_template('/cus_search_flight.html',error=error)
    num_seat=data2[0]["num_seat"]
    print("num seat:",num_seat)
    base_price=data2[0]["base_price"]
    if seat_taken>=int(num_seat*0.75):
        sold_price=base_price*1.25
    elif seat_taken==num_seat:
        cursor.close()
        error="No Available Seat"
        return render_template('/cus_search_flight.html',error=error)
    else:
        sold_price=base_price
    session["airline_name"]=airline_name
    session["flight_num"]=flight_num
    session["depature_date"]=depature_date
    session["depature_time"]=depature_time
    session["sold_price"]=sold_price
    cursor.close()
    return redirect(url_for('cus_check_out'))


@app.route('/cus_check_out')
def cus_check_out():
    sold_price=session["sold_price"]
    return render_template('/cus_check_out.html',price=sold_price)

@app.route('/cus_proceed_payment',methods=['GET','POST'])
def cus_proceed_payment():
    airline_name=session["airline_name"]
    flight_num=session["flight_num"]
    depature_date=session["depature_date"]
    depature_time=session["depature_time"]
    sold_price=session["sold_price"]
    username=session["Username"]
    card_type=request.form["Card Type"]
    card_num=request.form["Card Number"]
    name_on=request.form["Name On"]
    exp_card=request.form["Exp"]
    cursor=conn.cursor()
    query="INSERT INTO ticket(email,airline_name,flight_num,depature_date,depature_time) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,airline_name,flight_num,depature_date,depature_time))
    conn.commit()
    query1="SELECT ticket_id \
FROM ticket \
WHERE email=%s and ticket_id not in (SELECT ticket_id FROM purchase WHERE email=%s)"
    cursor.execute(query1,(username,username))
    data=cursor.fetchall()
    query2="INSERT INTO purchase VALUES(%s,%s,%s,%s,%s,%s,current_timestamp,%s)"
    cursor.execute(query2,(data[0]["ticket_id"],username,card_type,card_num,name_on,exp_card,sold_price))
    conn.commit()
    cursor.close()
    return redirect(url_for('cus_check_out'))
    
@app.route('/cus_check_goback')
def cus_check_goback():
    session.pop("airline_name")
    session.pop("flight_num")
    session.pop("depature_date")
    session.pop("depature_time")
    session.pop("sold_price")
    return redirect('/cus_search_flight')

@app.route('/cus_ratecomment_EXCE',methods=['GET','POST'])
def cus_ratecomment_EXCE():
    username=session["Username"]
    airline_name=request.form["Airline Name"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    depature_time=request.form["Depature Time"]
    rate=float(request.form["Rate"])
    comment=request.form["Comment"]
    cursor=conn.cursor()
    error=None
    print(depature_date,depature_time,rate)
    query="SELECT * FROM comment_rate \
WHERE email=%s and airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s"
    cursor.execute(query,(username,airline_name,flight_num,depature_date,depature_time))
    data=cursor.fetchall()
    if (data):
        cursor.close()
        error="You Have Already Rated This Flight"
        return render_template('/cus_ratecomment.html',error=error)
    query="SELECT * FROM ticket \
WHERE email=%s and airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s"
    cursor.execute(query,(username,airline_name,flight_num,depature_date,depature_time))
    data1=cursor.fetchall()
    if(not data1):
        cursor.close()
        error="You Don't Purchase For This Flight"
        return render_template('/cus_ratecomment.html',error=error)
    query="SELECT * FROM ticket NATURAL JOIN flight \
WHERE email=%s and airline_name=%s and flight_num=%s and depature_date=%s \
and depature_time=%s and arrival_date<current_date"
    cursor.execute(query,(username,airline_name,flight_num,depature_date,depature_time))
    data2=cursor.fetchall()
    if(not data2):
        cursor.close()
        error="You Can Only Rate After Completing This Flight"
        return render_template('/cus_ratecomment.html',error=error)
    query="INSERT INTO comment_rate VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,airline_name,flight_num,depature_date,depature_time,rate,comment))
    conn.commit()
    cursor.close()
    return render_template('/cus_ratecomment.html',error=error)

@app.route('/cus_track_spend')
def cus_track_spend():
    username=session["Username"]
    cursor=conn.cursor()
    query="SELECT SUM(sold_price) as total_year_cost \
FROM purchase WHERE CURRENT_TIMESTAMP-INTERVAL 365 DAY<=p_datetime and p_datetime<=CURRENT_TIMESTAMP and email=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    query="CREATE VIEW cus_spending_6month(p_datetime,sold_price) as \
SELECT p_datetime, sold_price FROM purchase WHERE email=%s and p_datetime>=CURRENT_TIMESTAMP-INTERVAL 180 DAY \
and p_datetime<=CURRENT_TIMESTAMP"
    cursor.execute(query,(username))
    conn.commit()
    query="SELECT YEAR(p_datetime) as year, MONTHNAME(p_datetime) as month_name, SUM(sold_price) as spending \
FROM cus_spending_6month GROUP BY YEAR(p_datetime),MONTHNAME(p_datetime)"
    cursor.execute(query)
    data1=cursor.fetchall()
    query="DROP VIEW cus_spending_6month"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return render_template('cus_track_spend.html',posts=data,posts1=data1)

@app.route('/cus_track_spend_EXCE',methods=['GET','POST'])
def cus_track_spend_EXCE():
    username=session["Username"]
    datefrom=request.form["Date From"]
    dateto=request.form["Date To"]
    cursor=conn.cursor()
    query="SELECT SUM(sold_price) as total_range_cost \
FROM purchase WHERE p_datetime>=%s and p_datetime<=%s and email=%s"
    cursor.execute(query,(datefrom,dateto,username))
    data2=cursor.fetchall()
    query="CREATE VIEW cus_spending(p_datetime,sold_price) as \
SELECT p_datetime, sold_price FROM purchase WHERE email=%s and p_datetime>=%s \
and p_datetime<=%s"
    cursor.execute(query,(username,datefrom,dateto))
    conn.commit()
    query="SELECT YEAR(p_datetime) as year, MONTHNAME(p_datetime) as month_name, SUM(sold_price) as spending \
FROM cus_spending GROUP BY YEAR(p_datetime),MONTHNAME(p_datetime)"
    cursor.execute(query)
    data3=cursor.fetchall()
    query="DROP VIEW cus_spending"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return render_template('cus_track_spend.html',posts2=data2,posts3=data3)
    

@app.route('/staffhome')
def staffhome():
    username=session["Username"]
    cursor=conn.cursor()
    query="SELECT airline_name FROM staff \
WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchone()
    session["Airline"]=data["airline_name"]
    airline_name=session["Airline"]
    query="SELECT airline_name,flight_num,depature_date,depature_time,T.name,T.city,S.name,S.city \
FROM flight,airport T, airport S \
WHERE depature_airport=T.code and arrival_airport=S.code and depature_date<=current_date+INTERVAL 30 DAY \
and depature_date>=current_date and airline_name=%s"
    cursor.execute(query,(airline_name))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('staffhome.html',username=username,posts=data1)

@app.route('/staffviewFlight')
def staffviewFlight():
    airline_name=session["Airline"]
    return render_template('staffviewFlight.html',airline=airline_name)

@app.route('/staffviewFlight_EXCE',methods=['GET','POST'])
def staffviewFlight_EXCE():
    source_city=request.form["Source City"]
    source_airport_name=request.form["Source Airport"]
    des_city=request.form["Destination City"]
    des_airport_name=request.form["Destination Airport"]
    datefrom=request.form["Date From"]
    dateto=request.form["Date To"]
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT airline_name,flight_num,depature_date,depature_time,T.name,T.city,S.name,S.city \
FROM flight,airport T, airport S \
WHERE depature_airport=T.code and arrival_airport=S.code and airline_name=%s and T.city=%s \
and T.name=%s and S.city=%s and S.name=%s and depature_date>=%s and depature_date<=%s"
    cursor.execute(query,(airline_name,source_city,source_airport_name,des_city,des_airport_name,datefrom,dateto))
    data=cursor.fetchall()
    cursor.close()
    return render_template('staffviewFlight.html',posts=data)

@app.route('/seecustomer',methods=['GET','POST'])
def seecustomer():
    airline_name=session["Airline"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    depature_time=request.form["Depature Time"]
    cursor=conn.cursor()
    query="SELECT airline_name,flight_num,depature_date,depature_time,email FROM ticket \
WHERE airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('staffviewFlight.html',posts1=data1)

@app.route('/addAirport')
def addAirport():
    return render_template('addAirport.html')

@app.route('/addAirport_EXCE',methods=['GET','POST'])
def addAirport_EXCE():
    username=session["Username"]
    code=request.form["Code"]
    name=request.form["Name"]
    city=request.form["City"]
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    error=None
    if (not data):
        error="Unauthorized Attempt"
        cursor.close()
        return render_template('addAirport.html',error=error)
    query="SELECT * FROM airport WHERE code=%s"
    cursor.execute(query,(code))
    data=cursor.fetchall()
    if (data):
        error="Already Add This Airport"
        cursor.close()
        return render_template('addAirport.html',error=error)
    query="INSERT INTO airport VALUES(%s,%s,%s)"
    cursor.execute(query,(code,name,city))
    conn.commit()
    return render_template('addAirport.html',error=error)

@app.route('/addAirplane')
def addAirplane():
    airline_name=session["Airline"]
    return render_template('addAirplane.html',airline=airline_name)

@app.route('/addAirplane_EXCE',methods=['GET','POST'])
def addAirplane_EXCE():
    id_num=request.form["ID"]
    num_seat=request.form["Seat"]
    username=session["Username"]
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    error=None
    if (not data):
        error="Unauthorized Attempt"
        cursor.close()
        return render_template('addAirplane.html',error=error)
    query="SELECT * FROM airplane WHERE id_num=%s and airline_name=%s"
    cursor.execute(query,(id_num,airline_name))
    data=cursor.fetchall()
    if (data):
        error="Already Add This Plane"
        cursor.close()
        return render_template('addAirplane.html',error=error)
    query="INSERT INTO airplane VALUES(%s,%s,%s)"
    cursor.execute(query,(id_num,airline_name,num_seat))
    conn.commit()
    return redirect(url_for('addAirplane_confirm'))

@app.route('/addAirplane_confirm')
def addAirplane_confirm():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT * FROM airplane WHERE airline_name=%s"
    cursor.execute(query,(airline_name))
    data=cursor.fetchall()
    cursor.close()
    return render_template('addAirplane_confirm.html',posts=data)




@app.route('/createNewFlight')
def createNewFlight():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT airline_name,flight_num,depature_date,depature_time,T.name,T.city,S.name,S.city \
FROM flight,airport T, airport S \
WHERE depature_airport=T.code and arrival_airport=S.code and depature_date<=current_date+INTERVAL 30 DAY \
and depature_date>=current_date and airline_name=%s"
    cursor.execute(query,(airline_name))
    data=cursor.fetchall()
    cursor.close()
    return render_template('createNewFlight.html',airline=airline_name,posts=data)

@app.route('/createNewFlight_EXCE',methods=['GET','POST'])
def createNewFlight_EXCE():
    airline_name=session["Airline"]
    username=session["Username"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    depature_time=request.form["Depature Time"]
    depature_airport=request.form["Depature Airport"]
    arrival_date=request.form["Arrival Date"]
    arrival_time=request.form["Arrival Time"]
    arrival_airport=request.form["Arrival Airport"]
    base_price=request.form["Base Price"]
    id_num=request.form["ID"]
    flight_status=request.form["Status"]
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    error=None
    if (not data):
        error="Unauthorized Attempt"
        cursor.close()
        return render_template('createNewFlight.html',error=error)
    query="SELECT * FROM airport WHERE code=%s"
    cursor.execute(query,(depature_airport))
    data=cursor.fetchall()
    if (not data):
        error="Depature Airport Doesn't Exist"
        cursor.close()
        return render_template('createNewFlight.html',error=error)
    cursor.execute(query,(arrival_airport))
    data=cursor.fetchall()
    if (not data):
        error="Arrival Airport Doesn't Exist"
        cursor.close()
        return render_template('createNewFlight.html',error=error)
    query="SELECT * FROM airplane WHERE id_num=%s and airline_name=%s"
    cursor.execute(query,(id_num,airline_name))
    data=cursor.fetchall()
    if (not data):
        error="Airplane Doesn't Exist"
        cursor.close()
        return render_template('createNewFlight.html',error=error)
    query="INSERT INTO flight VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time,depature_airport,arrival_date,\
                          arrival_time,arrival_airport,base_price,id_num,flight_status))
    conn.commit()
    cursor.close()
    return render_template('createNewFlight.html',error=error)

@app.route('/changeStatus')
def changeStatus():
    airline_name=session["Airline"]
    return render_template('changeStatus.html',airline=airline_name)

@app.route('/changeStatus_EXCE',methods=['GET','POST'])
def changeStatus_EXCE():
    username=session["Username"]
    airline_name=session["Airline"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    depature_time=request.form["Depature Time"]
    flight_status=request.form["Status"]
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    error=None
    if (not data):
        error="Unauthorized Attempt"
        cursor.close()
        return render_template('changeStatus.html',error=error)
    query="SELECT * FROM flight WHERE airline_name=%s and flight_num=%s and depature_date=%s and depature_time=%s"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data=cursor.fetchall()
    if (not data):
        error="This Flight Doesn't Exist"
        cursor.close()
        return render_template('changeStatus.html',error=error)
    query1="UPDATE flight SET flight_status=%s WHERE airline_name=%s and flight_num=%s \
and depature_date=%s and depature_time=%s;"
    cursor.execute(query1,(flight_status,airline_name,flight_num,depature_date,depature_time))
    conn.commit()
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data=cursor.fetchall()
    cursor.close()
    return render_template('changeStatus.html',error=error,posts=data)

@app.route('/view_rating')
def view_rating():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT airline_name,flight_num,depature_date,depature_time,AVG(rate) as avg_rate \
FROM comment_rate WHERE airline_name=%s GROUP BY airline_name,flight_num,depature_date,depature_time"
    cursor.execute(query,(airline_name))
    data=cursor.fetchall()
    cursor.close()
    return render_template('view_rating.html',airline=airline_name,posts=data)

@app.route('/view_rating_EXCE',methods=['GET','POST'])
def view_rating_EXCE():
    airline_name=session["Airline"]
    username=session["Username"]
    flight_num=request.form["Flight Number"]
    depature_date=request.form["Depature Date"]
    depature_time=request.form["Depature Time"]
    cursor=conn.cursor()
    query="SELECT * FROM staff WHERE user_name=%s"
    cursor.execute(query,(username))
    data=cursor.fetchall()
    error=None
    if (not data):
        error="Unauthorized Attempt"
        cursor.close()
        return render_template('view_rating.html',error=error)
    query="SELECT * FROM comment_rate WHERE airline_name=%s and flight_num=%s and depature_date=%s \
and depature_time=%s"
    cursor.execute(query,(airline_name,flight_num,depature_date,depature_time))
    data=cursor.fetchall()
    cursor.close()
    return render_template('view_rating.html',error=error,airline=airline_name,posts1=data)

@app.route('/view_frequent_cus')
def view_frequent_cus():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="CREATE VIEW customer_frequency(email,frequency) as \
SELECT email, COUNT(email) as freqnency FROM ticket NATURAL JOIN flight \
WHERE airline_name=%s and arrival_date<=CURRENT_TIMESTAMP \
GROUP BY email;"
    cursor.execute(query,(airline_name))
    conn.commit()
    query="SELECT email, frequency as max_frequency FROM customer_frequency \
WHERE frequency=(SELECT MAX(frequency) FROM customer_frequency)"
    cursor.execute(query)
    data=cursor.fetchall()
    query="DROP VIEW customer_frequency;"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return render_template('view_frequent_cus.html',airline=airline_name,posts=data)

@app.route('/view_cus',methods=['GET','POST'])
def view_cus():
    airline_name=session["Airline"]
    email=request.form["Email"]
    cursor=conn.cursor()
    query="SELECT * FROM ticket NATURAL JOIN flight,airport T, airport S \
WHERE T.code=depature_airport and S.code=arrival_airport and \
email=%s and airline_name=%s"
    cursor.execute(query,(email,airline_name))
    data=cursor.fetchall()
    cursor.close()
    return render_template('view_frequent_cus.html',airline=airline_name,posts1=data)

@app.route('/view_reports')
def view_reports():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    day=[365,30]
    total=[]
    for elem in day:
        query="SELECT COUNT(email) as amount FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s and p_datetime>=CURRENT_TIMESTAMP-INTERVAL %s DAY \
and p_datetime<=CURRENT_TIMESTAMP"
        cursor.execute(query,(airline_name,elem))
        data=cursor.fetchall()
        total.append(data)
    query="CREATE VIEW view1(p_datetime,email) as \
SELECT p_datetime, email FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s"
    cursor.execute(query,(airline_name))
    conn.commit()
    query="SELECT YEAR(p_datetime) as year, MONTHNAME(p_datetime) as month_name, \
COUNT(email) as amount FROM view1 GROUP BY YEAR(p_datetime), MONTHNAME(p_datetime)"
    cursor.execute(query)
    data1=cursor.fetchall()
    query="DROP VIEW view1"
    cursor.execute(query)
    conn.commit()
    session["year"]=total[0]
    session["lastmonth"]=total[1]
    session["monthwise"]=data1
    cursor.close()
    return render_template('view_reports.html',airline=airline_name,total1=total[0],total2=total[1],\
                           posts1=data1)
        

@app.route('/view_reports_EXCE',methods=['GET','POST'])
def view_reports_EXCE():
    airline_name=session["Airline"]
    datefrom=request.form["Date From"]
    dateto=request.form["Date To"]
    cursor=conn.cursor()
    query="SELECT COUNT(email) as amount FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s and p_datetime>=%s \
and p_datetime<=%s"
    cursor.execute(query,(airline_name,datefrom,dateto))
    data=cursor.fetchall()
    total1=session["year"]
    total2=session["lastmonth"]
    data1=session["monthwise"]
    cursor.close()
    return render_template('view_reports.html',airline=airline_name,total1=total1,\
                           total2=total2,posts1=data1,total3=data)

@app.route('/view_reports_end')
def view_reports_end():
    session.pop("year")
    session.pop("lastmonth")
    session.pop("monthwise")
    return redirect('/staffhome')
    
    
@app.route('/view_revenue')
def view_revenue():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    query="SELECT SUM(sold_price) as revenue FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s and p_datetime<=CURRENT_TIMESTAMP and p_datetime>=CURRENT_TIMESTAMP-INTERVAL 30 DAY"
    cursor.execute(query,(airline_name))
    data=cursor.fetchall()
    query="SELECT SUM(sold_price) as revenue FROM purchase NATURAL JOIN ticket \
WHERE airline_name=%s and p_datetime<=CURRENT_TIMESTAMP and p_datetime>=CURRENT_TIMESTAMP-INTERVAL 365 DAY"
    cursor.execute(query,(airline_name))
    data1=cursor.fetchall()
    cursor.close()
    return render_template('view_revenue.html',airline=airline_name,posts=data,posts1=data1)

@app.route('/view_top_des')
def view_top_des():
    airline_name=session["Airline"]
    cursor=conn.cursor()
    day=[90,365]
    res=[]
    for elem in day:
        query="CREATE VIEW 3month_total_ticket(destination,sold_num) as \
SELECT S.city as destination, COUNT(email) as sold_num \
FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport T, airport S \
WHERE depature_airport=T.code and arrival_airport=S.code and airline_name=%s \
and p_datetime>=CURRENT_TIMESTAMP-INTERVAL %s DAY and p_datetime<=CURRENT_TIMESTAMP \
GROUP BY S.city"
        cursor.execute(query,(airline_name,elem))
        conn.commit()
        query="SELECT destination,sold_num FROM 3month_total_ticket \
WHERE sold_num=(SELECT MAX(sold_num) FROM 3month_total_ticket)"
        cursor.execute(query)
        data=cursor.fetchone()
        data=[data]
        if (data[0]):
            data[0]["rank"]=1
        query="CREATE VIEW no_most1(destination,sold_num) as \
SELECT destination, sold_num FROM 3month_total_ticket \
WHERE sold_num != (SELECT MAX(sold_num) FROM 3month_total_ticket)"
        cursor.execute(query)
        conn.commit()
        query="SELECT destination,sold_num FROM no_most1 \
WHERE sold_num=(SELECT MAX(sold_num) FROM no_most1)"
        cursor.execute(query)
        data1=cursor.fetchone()
        print(data1)
        if (data1):
            data1["rank"]=2
            data.append(data1)
        query="CREATE VIEW no_most2(destination,sold_num) as \
SELECT destination, sold_num FROM no_most1 \
WHERE sold_num != (SELECT MAX(sold_num) FROM no_most1)"
        cursor.execute(query)
        conn.commit()
        query="SELECT destination,sold_num FROM no_most2 \
WHERE sold_num=(SELECT MAX(sold_num) FROM no_most2)"
        cursor.execute(query)
        data2=cursor.fetchone()
        if (data2):
            data2["rank"]=3
            data.append(data2)
        res.append(data)
        query="DROP VIEW 3month_total_ticket"
        cursor.execute(query)
        conn.commit()
        query="DROP VIEW no_most1"
        cursor.execute(query)
        conn.commit()
        query="DROP VIEW no_most2"
        cursor.execute(query)
        conn.commit()
    cursor.close()
    return render_template('view_top_des.html',airline=airline_name,posts=res[0],posts1=res[1])
        

        
@app.route('/cuslogout')
def cuslogout():
    session.pop("Username")
    return redirect('/cuslogin')

@app.route('/stafflogout')
def stafflogout():
    session.pop("Username")
    session.pop("Airline")
    return redirect('/stafflogin')

app.secret_key="some key that you will never guess"

if __name__=="__main__":
    app.run("127.0.0.1",8888,debug=True)
