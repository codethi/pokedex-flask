from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import uri_pg

app = Flask(__name__)
app.secret_key = 'pokedex'

app.config['SQLALCHEMY_DATABASE_URI'] = uri_pg
db = SQLAlchemy(app)

class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, imagem, descricao, tipo):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.tipo = tipo

@app.route('/')
def index():
    pokedex = Pokedex.query.all()
    return render_template('index.html', pokedex=pokedex)

@app.route('/new', methods=['GET', 'POST'])
def new():
   if request.method == 'POST':
      pokemon = Pokedex(
         request.form['nome'],
         request.form['imagem'],
         request.form['descricao'],
         request.form['tipo']
      )
      db.session.add(pokemon)
      db.session.commit() 
      flash('Projeto criado com sucesso!')
      return redirect('/') 

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
   pokemon = Pokedex.query.get(id)
   pokedex = Pokedex.query.all()
   if request.method == "POST":
      pokemon.nome = request.form['nome']
      pokemon.descricao = request.form['descricao']
      pokemon.imagem = request.form['imagem']
      pokemon.tipo = request.form['tipo']
      db.session.commit() 
      return redirect('/')
   return render_template('index.html', pokemon=pokemon, pokedex=pokedex) 

@app.route('/<id>')
def get_by_id(id):
   pokemonDelete = Pokedex.query.get(id) 
   pokedex = Pokedex.query.all()
   return render_template('index.html', pokemonDelete=pokemonDelete, pokedex=pokedex)

@app.route('/delete/<id>') 
def delete(id):
   pokemon = Pokedex.query.get(id) 
   db.session.delete(pokemon) 
   db.session.commit() 
   return redirect('/')

@app.route('/filter', methods=['GET', 'POST']) 
def filter():
   pokedex = Pokedex.query.filter_by(tipo=request.form['search']).all()
   return render_template('index.html', pokedex=pokedex)

@app.route('/filter/<param>') 
def filter_by_param(param):
   pokedex = Pokedex.query.filter_by(tipo=param).all()
   return render_template('index.html', pokedex=pokedex)

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)