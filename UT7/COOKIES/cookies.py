from flask import Flask, render_template, request, url_for, make_response
app = Flask(__name__)

@app.route('/')
def index():
    color=request.cookies.get('colorH1')
    return render_template('main.html',color=color)

@app.route('/actualitza', methods=['GET', 'POST'])
def actualitza():
    color = request.args.get('estilo')
    print(color)
    resposta = make_response(render_template('main.html',color=color))
    resposta.set_cookie('colorH1',color,max_age=60)
    #max_age = vida de la cookie (60 segons)
    return resposta

if __name__ == '__main__':
    app.run()