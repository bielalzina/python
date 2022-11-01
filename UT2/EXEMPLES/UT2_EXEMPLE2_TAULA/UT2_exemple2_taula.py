from distutils.log import debug
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    dades = {'TOMATIGUES':[1,2,3,4,5,6],'MELONS':[3,3,3,4,4,4], 'GINJOLS':[9,9,8,8,7,7]}
    titolsColumnes = ['','2015','2016','2017','2018','2019','2020']
    titolsFiles = ['TOMATIGUES','MELONS','GINJOLS']
    return render_template('template_Taula.html', dades = dades, tFiles = titolsFiles, tColumnes = titolsColumnes)

if __name__=='__main__':
    app.run(debug=True)