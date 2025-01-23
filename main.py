from flask import Flask, make_response, jsonify, request
import mysql.connector
from flask_cors import CORS
from bd import Quadros

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ROLONnl3@',
    database='cadastros'
)

app = Flask(__name__)
CORS(app)

@app.route('/quadros', methods = ['GET'])
def get_products():

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM cadastros.produtos')
    produtos = mycursor.fetchall()

    quadro = list()
    for i in produtos:
        quadro.append(
            {
                'id': i[0],
                'titulo': i[1],
                'preco': i[2],
                'categoria': i[3],
                'imagem': i[4],
                'descricao': i[5],
                'cor': i[6],
                'tamanho': i[7]
            }
        )

    return make_response(
        jsonify(quadro)
    )

@app.route('/quadros', methods=['POST'])
def create_quadro():
    newquadro = request.json

    sql = f"INSERT INTO cadastros.produtos (id, titulo, preco, categoria, imagem, descricao, cor, tamanho) VALUES ('{newquadro['titulo']}', '{newquadro['preco']}', '{newquadro['categoria']}', '{newquadro['imagem']}', '{newquadro['descricao']}', '{newquadro['cor']}', '{newquadro['tamanho']}')"
    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem = 'Novo produto cadastrado com sucesso.',
            quadro = newquadro
        )
    )


app.run()
