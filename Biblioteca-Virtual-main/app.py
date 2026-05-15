from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# CONEXÃO

def conectar():
    conexao = sqlite3.connect('biblioteca.db')
    conexao.row_factory = sqlite3.Row
    return conexao


# CRIAR TABELA

def criar_tabela():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        senha TEXT NOT NULL,

        data_cadastro DATE DEFAULT CURRENT_DATE
    )
    ''')

    conexao.commit()
    conexao.close()


# HOME

@app.route('/')
def home():
    return render_template('index.html')


# LIVROS

@app.route('/livros')
def livros():
    return render_template('biblioteca.html')


# CADASTRO

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar()
        cursor = conexao.cursor()

        try:

            cursor.execute('''
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
            ''', (nome, email, senha))

            conexao.commit()

        except sqlite3.IntegrityError:

            return 'Email já cadastrado!'

        finally:
            conexao.close()

        return redirect('/login')

    return render_template('cadastro.html')

# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute('''
        SELECT * FROM usuarios
        WHERE email = ? AND senha = ?
        ''', (email, senha))

        usuario = cursor.fetchone()

        conexao.close()

        if usuario:
            return redirect('/')

        else:
            return 'Email ou senha incorretos!'

    return render_template('login.html')


# LISTA DE USUÁRIOS

@app.route('/usuarios')
def usuarios():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM usuarios')

    usuarios = cursor.fetchall()

    conexao.close()

    return render_template(
        'usuarios.html',
        usuarios=usuarios
    )


# INICIAR

if __name__ == '__main__':

    criar_tabela()

    app.run(debug=True)