from flask import Flask, make_response, jsonify
from bd import Quadros

app = Flask(__name__)

@app.route('/quadros', methods = ['GET'])
def get_products():
    return make_response(
        jsonify(Quadros)
    )

app.run()
