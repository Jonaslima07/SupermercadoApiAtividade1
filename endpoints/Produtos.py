from flask import Blueprint, request, jsonify
import sqlite3
from helpers.database import getConnection
from helpers.logging import logger
from Models.Produtos import Produtos

Produtos_BluePrint = Blueprint('produtos', __name__)

@Produtos_BluePrint.route("/", methods=["GET"])
def produtos_get():
    try:
        logger.info("Listando produtos")
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from produtos")
        # 4 - retorna resultset
        resultset = cursor.fetchall()
        # Iterar e transformar dados.
        produtos = []
        for item in resultset:
            id = item[0]
            nome = item[1]
            produto = Produtos(id, nome)
            logger.info(produto)
            produtos.append(produto.toJson())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(produtos), 200


@Produtos_BluePrint.route("/", methods=["POST"])
def produtos_post():
    # Captar o json da requisição e adicionar na lista.
    produtosNovos = request.json

    # Manipulação do dados antiga.
    # produtosNovos['id'] = calcularProximoId()
    # produtos.append(produtosNovos)
    # 1 - Conectar.
    connection = getConnection()

    # 2 - Obter cursor.
    cursor = connection.cursor()

    # 3 - Executar.
    cursor.execute(
        "insert into produtos(nome) values (?)", (produtosNovos['nome'],))

    # 3.1 - Confirmar - commit.
    connection.commit()

    id = cursor.lastrowid
    produtosNovos['id'] = id

    return jsonify(produtosNovos), 200


def getProdutoById(idProduto):
    try:
        # Retornar o resultset.
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from produtos where id = ?", (idProduto,))
        # 4 - Retornar resultset
        resultset = cursor.fetchone()  # [] -> ()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return resultset


@Produtos_BluePrint.route("/<int:idProduto>", methods=["GET"])
def produto_get(idProduto):
    try:
        
        resultset = getProdutoById(idProduto)
        # Vrf se resultset n é nulo e transforma os dados.
        if resultset is not None:
            produto = {
                'id': resultset[0],
                'nome': resultset[1],
            }
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(produto), 200


@Produtos_BluePrint.route("/<int:idProduto>", methods=["PUT"])
def produtos_put(idProduto):
    try:
        # Captar o json da requisição e adicionar na lista.
        produtoAtualizado = request.json
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Verificar se o produto a ser atualizado existe.
        resultset = getProdutoById(idProduto)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute("update produtos set nome=? where id=?",
                            (produtoAtualizado['nome'], idProduto))
            # 3.1 - Confirmar - commit.
            connection.commit()
            # Adicionar id ao json.
            produtoAtualizado['id'] = idProduto
            return jsonify(produtoAtualizado), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Produto não encontrado'}), 404)



@Produtos_BluePrint.route("/<int:idProduto>", methods=["DELETE"])
def produtos_delete(idProduto):
    try:
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Verificar se o produto a ser atualizado existe.
        resultset = getProdutoById(idProduto)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute(
                "delete from produtos where id = ?", (idProduto, ))
            # 3.1 - Confirmar - commit.
            connection.commit()
            return {'mensagem': " Produto removido com sucesso"}, 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Produto não encontrado'}), 404)
