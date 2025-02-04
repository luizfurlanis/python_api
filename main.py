from flask import Flask, make_response, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS


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

    return jsonify(quadro)


# GET method for the user UI
@app.route('/add', methods=['GET'])
def add_product_form():
    return render_template('add_products.html')


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

    mycursor = mydb.cursor()
    mycursor.execute(sql, valores)
    mydb.commit()

    return jsonify(mensagem = 'Produto cadastrado!', quadro = newquadro)

# Run the API app
app.run(debug=True)
