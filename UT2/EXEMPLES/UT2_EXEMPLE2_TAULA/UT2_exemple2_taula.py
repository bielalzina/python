from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    dades={'TOMATIGUES':[1,2,3,4,5,6], 'MELONS':[7,8,9,10,11,12], 'GINJOLS':[13,14,15,16,17,18]}
    titolsCol=['','2015','2016','2017','2018','2019','2020']
    titolsFil=['TOMATIGUES', 'MELONS', 'GINJOLS']
    return render_template('template_taula.html',dades=dades, fil=titolsFil,col=titolsCol)

if __name__ == '__main__':
    app.run(debug=True)