from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import datetime
import urllib.request, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


@app.route('/')
def index():
	session['aeroportCode']="PMI"
	session['pantalla']="arribades"
	return redirect(url_for('arribades'))

@app.route('/sortides')
def sortides():
	session['pantalla']="sortides"	
	return render_template('aeroport.html')

# This page will have the sign up form
@app.route('/arribades')
def arribades():
	session['pantalla']="arribades"
	url="http://127.0.0.1:5001/vols/arribades/"+session['aeroportCode']+"/2022-05-01_00:00"
	response = urllib.request.urlopen(url)
	data = response.read()
	jsonVols = json.loads(data)
	print(jsonVols)
	return render_template('aeroport.html',vols=jsonVols)

@app.route('/aeroport') #la utilitzam per canviar d'aeroport
def aeroport():
	nouAeroport= request.args.get('codi')
	session['aeroportCode']=nouAeroport
	if session['pantalla']=="arribades":
		return redirect(url_for('arribades'))
	else:
		return redirect(url_for('sortides'))

if __name__ == '__main__':
	app.run(debug=True)
