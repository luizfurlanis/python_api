from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
app = Flask(__name__)
CORS(app)


# GET method for the website
@app.route('/quadros', methods = ['GET'])
def get_products():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM cadastros.produtos')
    produtos = cursor.fetchall()
    cursor.close()

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
    return jsonify(quadro)



# rota para adicionar produto
@app.route('/add')
def add_product_form():
    return render_template('add_product.html')


# POST method for adding new product
@app.route('/quadros', methods=['POST'])
def create_quadro():
    if request.is_json:
        newquadro = request.json
    else:
        newquadro = {
            'titulo' : request.form['titulo'],
            'preco' : float(request.form['preco']),
            'categoria' : request.form['categoria'],
            'imagem' : request.form['imagem'],
            'descricao' : request.form['descricao'],
            'cor' : request.form['cor'],
            'tamanho' : request.form['tamanho']
        }    
    
    sql = "INSERT INTO cadastros.produtos (titulo, preco, categoria, imagem, descricao, cor, tamanho) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    valores = (newquadro['titulo'], newquadro['preco'], newquadro['categoria'], newquadro['imagem'], newquadro['descricao'], newquadro['cor'], newquadro['tamanho'])

    cursor = mydb.cursor()
    cursor.execute(sql, valores)
    mydb.commit()
    cursor.close()

    return jsonify(mensagem = 'Produto cadastrado!', quadro = newquadro)

# Run the API app
app.run(debug = True, host = 0.0.0.0, port = 5000)
