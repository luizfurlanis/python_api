import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

#contruindo as funcionalidades
@app.route('/')
def homepage():
    return 'A API está no ar'

@app.route('/resposta')
def products():
    try:
        tabela = pd.read_csv("cancelamentos.csv")
        res = tabela.to_dict(orient='dict')
        return jsonify(res)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo nao encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#rodando a api
if __name__ == "__main__":
    app.run(debug = True)



