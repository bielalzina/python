from flask import Flask, render_template, request, session
app=Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'

@app.route('/')
def index():
    session['varInterna']=1
    return render_template('Home.html')

@app.route('/actualitzar')
def actualitzar():
    bot=request.args.get('operacion')
    if bot=="mas1":
        session['varInterna']=session['varInterna']+1
    if bot=="mas5":
        session['varInterna']=session['varInterna']+5
    if bot=="menos2":
        session['varInterna']=session['varInterna']-2
    print(session['varInterna'])
    return render_template('Boton.html', boton=bot)
    
if __name__ == '__main__':
    app.run(debug=True)