from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/operacoes', methods=['GET'])
def operacoes():
    return jsonify({
        "operacoes_disponiveis": [
            {"nome": "soma",          "simbolo": "+"},
            {"nome": "subtracao",     "simbolo": "-"},
            {"nome": "multiplicacao", "simbolo": "×"},
            {"nome": "divisao",       "simbolo": "÷"}
        ]
    })

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        
        if not data or 'num1' not in data or 'num2' not in data or 'operacao' not in data:
            return jsonify({"erro": "Campos num1, num2 e operacao são obrigatórios"}), 400
        
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operacao = str(data['operacao']).strip().lower()

        if operacao not in ['soma', 'subtracao', 'multiplicacao', 'divisao']:
            return jsonify({"erro": "Operação inválida"}), 400
        
        if operacao == 'divisao' and num2 == 0:
            return jsonify({"erro": "Divisão por zero não é permitida"}), 422

        symbols = {'soma': '+', 'subtracao': '-', 'multiplicacao': '×', 'divisao': '÷'}
        
        if operacao == 'soma':
            resultado = num1 + num2
        elif operacao == 'subtracao':
            resultado = num1 - num2
        elif operacao == 'multiplicacao':
            resultado = num1 * num2
        else:
            resultado = num1 / num2

        expressao = f"{num1} {symbols[operacao]} {num2} = {resultado}"

        return jsonify({
            "sucesso": True,
            "operacao": operacao,
            "expressao": expressao,
            "num1": num1,
            "num2": num2,
            "resultado": resultado,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    except:
        return jsonify({"erro": "Erro ao processar a requisição"}), 400


if __name__ == '__main__':
    print("🚀 API rodando em http://localhost:5000")
    app.run(debug=True, port=5000)
