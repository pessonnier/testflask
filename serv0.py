from flask import Flask, render_template, request #, url_for

def init():
    pass

def loop():
    pass

app = Flask(__name__)

@app.route('/')
def index():
    return 'boo'

@app.route('/page1')
def page1():
    return render_template('page.html',
    title='page 1', 
    headline='Page 1',
    pages=['page2','page3'])

@app.route('/page2')
def page2():
    return render_template('page.html',
    title='page 2',
    headline='Page 2',
    pages=['page1','page3'])

@app.route('/page3')
def page3():
    return render_template('page.html',
    title='page 3',
    headline='Page 3',
    pages=['page1','page2'])

@app.route('/param/<string:str>')
def param(str):
    return f'<h1>boo {str}</h1>'

variables={
    'gauche': 5,
    'droite': 8
}

@app.route('/modif', methods=['POST'])
def modif():
    var = request.form.get('var')
    val = request.form.get('val')
    variables[var]= int(val)
    return render_template('modif.html',
    title='modif de '+var,
    headline='modification de '+var,
    var=var, val=variables[var],
    variables=variables)

@app.route('/variable/<string:var>')
def variable(var):
    if var not in variables:
        variables[var]= 0
    return render_template('variable.html',
    title='edition de '+var,
    headline='modification de '+var,
    var=var, val=variables[var])

@app.route('/t/i')
def index_t():
    return render_template('index.html',
    title='boo',
    headline='Alu',
    new_year=True,
    names=['a', 'b', 'c'])


if __name__ == '__main__':
    init()
    loop()