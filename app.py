from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'bdtarefas'

mysql = MySQL(app)


#Rota principal

@app.route('/', methods=['GET','POST'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT idTarefas, tarefa_titulo, tarefa_descricao, tarefa_horario FROM tarefas")
    data = cur.fetchall()

    tarefas = []

    for row in data:
        horario_tarefa = datetime.strptime(str(row[3]), '%H:%M:%S').time()

        now = datetime.now().time()

        if now > horario_tarefa:
            statuscor = 'atrasada'
            status = 'Atrasada'
        else:
            statuscor = 'noprazo'
            status = 'No prazo'

        tarefa = {
            'id': row[0],
            'titulo': row[1],
            'descricao': row[2],
            'horario': row[3],
            'status': status,
            'statuscor': statuscor
        }

        tarefas.append(tarefa)

    cur.close()

    return render_template('index.html', tarefas=tarefas)
    
#Rota usada para editar tarefa

@app.route('/editar', methods=['GET','POST'])
def atualizar():
    idTarefas = request.form['idTarefas']
    tarefa_titulo = request.form['tarefa_titulo']
    tarefa_horario = request.form['tarefa_horario']
    tarefa_descricao =  request.form['tarefa_descricao']

    
    cur = mysql.connection.cursor()
    cur.execute(f'UPDATE tarefas SET tarefa_descricao = "{tarefa_descricao}", tarefa_horario = "{tarefa_horario}", tarefa_titulo = "{tarefa_titulo}" WHERE idTarefas = {idTarefas}')
    mysql.connection.commit()
    cur.close()
    
    return redirect('/')

#rota usada para criar tarefa

@app.route('/criar', methods=['GET','POST'])
def criar():
    tarefa_titulo = request.form['titulo']
    tarefa_horario = request.form['horario']
    tarefa_descricao = request.form['descricao']


    cur = mysql.connection.cursor()
    cur.execute(f'INSERT INTO tarefas (tarefa_titulo, tarefa_descricao, tarefa_horario) VALUES ("{tarefa_titulo}","{tarefa_descricao}","{tarefa_horario}")')
    mysql.connection.commit()
    cur.close()
    
    return redirect('/')

# rota usada para deletar tarefa

@app.route('/deletar', methods=['GET','POST'])
def deletar_item():
    idTarefas = request.form['idTarefas']

    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM tarefas WHERE idTarefas = {idTarefas}')
    mysql.connection.commit()
    cur.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


