import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

# Configuração do banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='ROLONnl3@',
        database='cadastros'
    )

@app.route('/')
def homepage():
    return 'A API está no ar'

@app.route('/dados', methods=['GET'])
def get_dados():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM produtos")
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
