from musicPlayer import app
import json
import sys
from werkzeug import secure_filename
import flask
import time
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from functools import wraps
import os
from bs4 import BeautifulSoup
import requests
from musicPlayer.db.connect import connection

# CUR, _ = connection()

@app.route('/register',methods=['GET','POST'])
def register():
	if flask.request.method == 'POST':
		name = flask.request.form['name']
		username = flask.request.form['username']

		print(name, username)
		result = CUR.execute("SELECT * FROM users WHERE username= %s",[username])
		print(result)
		if result>0:
			error='User name already exists !!'
			return render_template('register.html',error=error)
		else:
			flash('Success!! Your account has been created.','success')
			return redirect(url_for('index'))

	return render_template('register.html')


#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']

        password_candidate=request.form['password']

        cur=mySql.connection.cursor()

        result=cur.execute("SELECT * FROM users WHERE username= %s",[username])

        if result>0:
            data=cur.fetchone()
            incripted_password=data['password']

            if sha256_crypt.verify(password_candidate,incripted_password):
                session['logged_in']=True
                session['username']=username
                session['id']=data['id']

                flash('login successful','success')
                return redirect(url_for('dashboard'))
            else:
                error='wrong password'

        else:
            error='Username not found'
        cur.close()
        return render_template('login.html',error=error)

    return render_template('login.html')

#to prevent using of app without login
def isUserLoggedIn(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('unauthorised,please login','danger')
			return redirect(url_for('login'))
	return wrap

#logout
@app.route('/logout')
def logout():
	session.clear()
	flash('you are now logout','success')
	return redirect(url_for('login'))

#search
@app.route('/new',methods=['POST'])
def new():
    co=request.form['give']
    song=co
    song_name=co+'.mp3'
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * FROM songs_list WHERE song_name=%s",[song_name])
    albu69=cur.fetchall()
    if result>0:
        cur.close()
        return render_template('search.html',albu=albu69)
    else:
        cur.close()
        flash('Song Not Found','success')
        return render_template('dashboard.html')


@app.route('/dashboard')
@isUserLoggedIn
def dashboard():
    cur=mySql.connection.cursor()
    result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
    songs=cur.fetchall()

    if result>0:
        return render_template('dashboard.html',songs=songs)
    else:
        msg="NO PLAYLIST FOUND "

    cur.close()
    return render_template('dashboard.html',msg=msg)

class make_playlist(Form):
	title=StringField('Name',[validators.Length(min=1,max=25)])



@app.route('/create_playlist',methods=['GET','POST'])
@isUserLoggedIn
def create_playlist():
	form=make_playlist(request.form)
	if request.method=='POST' and form.validate():
		title=form.title.data

		cur=mysql.connection.cursor()

		#result=cur.execute("SELECT * FROM users WHERE username= %s",[{{session.username}}])
		username=session['username']

		row=cur.execute("SELECT * FROM users WHERE username = %s",[username])
		result=cur.fetchone()
		idd=result['id']
		cur.execute("INSERT INTO songs(title,user_id) VALUES (%s,%s)",([title],idd,))
		cur.execute("UPDATE songs SET type=1 WHERE title=%s",([title]))
		mysql.connection.commit()
		cur.close()

		flash(idd,'success')

		return redirect(url_for('dashboard'))
	return render_template('add_playlist.html',form=form)



@app.route('/create_private_playlist',methods=['GET','POST'])
@isUserLoggedIn
def create_private_playlist():
	form=make_playlist(request.form)
	if request.method=='POST' and form.validate():
		title=form.title.data

		cur=mysql.connection.cursor()

		#result=cur.execute("SELECT * FROM users WHERE username= %s",[{{session.username}}])
		username=session['username']

		row=cur.execute("SELECT * FROM users WHERE username = %s",[username])
		result=cur.fetchone()
		idd=result['id']
		cur.execute("INSERT INTO songs(title,user_id) VALUES (%s,%s)",([title],idd))
		cur.execute("UPDATE songs SET type=0 WHERE title=%s",([title]))
		mysql.connection.commit()
		cur.close()

		flash(idd,'success')

		return redirect(url_for('dashboard'))
	return render_template('add_playlist.html',form=form)


@app.route('/users')
@isUserLoggedIn
def users():
	cur=mysql.connection.cursor()
	result=cur.execute("SELECT * from users")
	songs=cur.fetchall()
	if result>0:
		return render_template('Dashboard.html',songs=songs)
	else:
		msg="NO PLAYLIST FOUND "

	return render_template('Dashboard.html',msg=msg)
	cur.close()


@app.route('/users/playlist/<string:idd>')
@isUserLoggedIn
def u_play(idd):
	cur=mysql.connection.cursor()
	result=cur.execute("SELECT * from songs WHERE user_id=%s and type=1",[idd])
	songs=cur.fetchall()
	if result>0:
		return render_template('das.html',songs=songs)
	else:
		msg="NO PLAYLIST FOUND "
	return render_template('das.html',msg=msg)
	cur.close()


@app.route('/Reputation')
@isUserLoggedIn
def play():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'rep%'")
	albu=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('home.html',songs=songs,albu=albu)
	else:
		songs=0
		return render_template('home.html',albu=albu,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('home.html',albu=albu)


@app.route('/Camila')
@isUserLoggedIn
def cam():
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM songs_list WHERE album LIKE 'Cam%'")
		albu1=cur.fetchall()
		result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
		songs=cur.fetchall()
		if result>0:
			return render_template('camila.html',songs=songs,albu=albu1)
		else:
			songs=0
			return render_template('camila.html',albu=albu1,song=songs)
		cur.close()
		#    app.logger.info(albu[11]["path"]
		return render_template('camila.html',albu=albu1)


@app.route('/CTRL')
@isUserLoggedIn
def sza():
		cur=mysql.connection.cursor()
		cur.execute("SELECT * FROM songs_list WHERE album LIKE 'SZA%'")
		albu2=cur.fetchall()
		result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
		songs=cur.fetchall()
		if result>0:
			return render_template('ctrl.html',songs=songs,albu=albu2)
		else:
			songs=0
			return render_template('ctrl.html',albu=albu2,song=songs)
		cur.close()
		#    app.logger.info(albu[11]["path"]
		return render_template('ctrl.html',albu=albu2)

@app.route('/BlackPanther')
@isUserLoggedIn
def panther():
			cur=mysql.connection.cursor()
			cur.execute("SELECT * FROM songs_list WHERE album LIKE 'bla%'")
			albu3=cur.fetchall()
			result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
			songs=cur.fetchall()
			if result>0:
				return render_template('blackpanther.html',songs=songs,albu=albu3)
			else:
				songs=0
				return render_template('blackpanther.html',albu=albu3,song=songs)
			cur.close()
			#    app.logger.info(albu[11]["path"]
			return render_template('blackpanther.html',albu=albu3)


@app.route('/Damn')
@isUserLoggedIn
def damn():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'Ken%'")
	albu4=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('damn.html',songs=songs,albu=albu4)
	else:
		songs=0
		return render_template('damn.html',albu=albu4,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('damn.html',albu=albu4)


@app.route('/SGFG')
@isUserLoggedIn
def sgfg():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE '5 S%'")
	albu5=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('sgfg.html',songs=songs,albu=albu5)
	else:
		songs=0
		return render_template('sgfg.html',albu=albu5,song=songs)
	cur.close()


@app.route('/revival')
@isUserLoggedIn
def revival():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'Emi%'")
	albu6=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('revival.html',songs=songs,albu=albu6)
	else:
		songs=0
		return render_template('revival.html',albu=albu6,song=songs)
	cur.close()
#	app.logger.info(albu5[14]["path"])

@app.route('/ManOfWoods')
@isUserLoggedIn
def manof():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'Jus%'")
	albu7=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('manofwoods.html',songs=songs,albu=albu7)
	else:
		songs=0
		return render_template('manofwoods.html',albu=albu7,song=songs)
	cur.close()


@app.route('/save_playlist/<string:name>/<string:ide>')
@isUserLoggedIn
def save(name,ide):
	res=""
	playl=[]
	flag=0
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs WHERE title = %s and user_id=%s",([name],[session['id']]))
	result=cur.fetchone()
	print(name)
	if result['_songs'] is None:
		cur.execute("UPDATE songs SET _songs=%s WHERE title=%s and user_id=%s",(ide,name,session['id']))
		mysql.connection.commit()

	else:
		res=result['_songs']
		playl=res.split("'")

		for i in playl:
			if i==ide:
				flag=1
		if flag==1:
			flash("songs already exist",'danger')
			return redirect(url_for('dashboard'))
		else:
			cur.execute("UPDATE songs SET _songs=CONCAT(%s'',_songs) WHERE title=%s and user_id=%s",(ide,name,session['id']))

		mysql.connection.commit()

	cur.close()
	flash("Song is added to playlist",'success')
	return redirect(url_for('dashboard'))


@app.route('/delete_playlist/<string:idd>')
@isUserLoggedIn
def delete_playlist(idd):
	cur=mysql.connection.cursor()
	cur.execute("delete  FROM songs WHERE id =%s",[idd])
	mysql.connection.commit()
	cur.close()
	flash("Playlist successfully deleted",'success')
	return redirect(url_for('dashboard'))

@app.route('/connect')
def connect():
	return render_template('connect.html')

@app.route('/play_playlist/<string:idd>')
@isUserLoggedIn
def play_playlist(idd):
	res=""
	playl=[]
	data=[]
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs WHERE id =%s",[idd])
	result=cur.fetchone()
	res=result['_songs']
	if res is None:
		flash("no song in playlist",'danger')
		return redirect(url_for('dashboard'))
	else:
		playl=res.split("'")
		length=len(playl)
		for i in playl:
				cur.execute("SELECT * FROM songs_list WHERE id=%s",[i])
				data.append(cur.fetchone())
		cur.execute("SELECT * FROM songs WHERE id=%s",[idd])
		name=cur.fetchone()
		Name=name['title']
		return render_template('playlist.html',albu=data,Name=Name,len=length)
