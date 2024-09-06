from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

# Dados iniciais de exemplo
estoque = [
    {"id": 1, "nome": "Bomba A", "quantidade": 10},
    {"id": 2, "nome": "Bomba B", "quantidade": 5}
]

@app.route('/')
def index():
    return render_template('index.html', estoque=estoque)

@app.route('/buscar')
def buscar():
    query = request.args.get('query')
    if query:
        query = query.lower()
        filtrado = [item for item in estoque if str(item['id']) == query or query in item['nome'].lower()]
        return render_template('resultados.html', estoque=filtrado)
    return redirect(url_for('index'))

@app.route('/adicionar', methods=['POST'])
def adicionar():
    item_id = int(request.form['id'])
    quantidade = int(request.form['quantidade'])
    nome = request.form.get('nome', '')

    for item in estoque:
        if item['id'] == item_id:
            item['quantidade'] += quantidade
            return redirect(url_for('index'))

    novo_item = {"id": item_id, "nome": nome, "quantidade": quantidade}
    estoque.append(novo_item)
    return redirect(url_for('index'))

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])

    for item in estoque:
        if item['id'] == id:
            item['nome'] = nome
            item['quantidade'] = quantidade
            return redirect(url_for('index'))

    return "Item não encontrado", 404

@app.route('/deletar/<int:id>')
def deletar(id):
    global estoque
    estoque = [item for item in estoque if item['id'] != id]
    return redirect(url_for('index'))

@app.route('/vender', methods=['POST'])
def vender():
    item_id = int(request.form['id'])
    quantidade = int(request.form['quantidade'])

    for item in estoque:
        if item['id'] == item_id:
            if item['quantidade'] >= quantidade:
                item['quantidade'] -= quantidade
                return redirect(url_for('index'))
            else:
                return "Quantidade insuficiente", 400

    return "Item não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
