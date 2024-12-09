from flask import Blueprint, request, jsonify
import sqlite3

from helpers.database import getConnection
from helpers.logging import logger
from Models.Categorias import Categorias

Categorias_BluePrint = Blueprint('categorias', __name__)

@Categorias_BluePrint.route("/", methods=["GET"])
def get_categorias():
    try:
        logger.info("Listando categorias")
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from categorias")
        # 4 - retorna resultset
        resultset = cursor.fetchall()
        # Iterar e transformar dados.
        categorias = []
        for item in resultset:
            id = item[0]
            nome = item[1]
            categoria = Categorias(id, nome)
            logger.info(categoria)
            categorias.append(categoria.toJson())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(categorias), 200


@Categorias_BluePrint.route("/", methods=["POST"])
def categorias_post():
    # Captar o json da requisição e adicionar na lista.
    categoriasNovas = request.json

    # Manipulação do dados antiga.
    # categoriasNovas['id'] = calcularProximoId()
    # categorias.append(categoriasNovas)
    # 1 - Conectar.
    connection = getConnection()

    # 2 - Obter cursor.
    cursor = connection.cursor()

    # 3 - Executar.
    cursor.execute(
        "insert into categorias(nome) values (?)", (categoriasNovas['nome'],))

    # 3.1 - Confirmar - commit.
    connection.commit()

    id = cursor.lastrowid
    categoriasNovas['id'] = id

    return jsonify(categoriasNovas), 200


def getCategoriaById(idCategoria):
    try:
        # Retornar o resultset.
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from categorias where id = ?", (idCategoria,))
        # 4 - Retornar resultset
        resultset = cursor.fetchone()  # [] -> ()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return resultset


@Categorias_BluePrint.route("/<int:idCategoria>", methods=["GET"])
def categorias_get(idCategoria):
    try:
        
        resultset = getCategoriaById(idCategoria)
        
        if resultset is not None:
            categoria = {
                'id': resultset[0],
                'nome': resultset[1],
            }
        else:
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(categoria), 200


@Categorias_BluePrint.route("/<int:idCategoria>", methods=["PUT"])
def update_categorias(idCategoria):
    try:
        # Captar o json da requisição e adicionar na lista.
        categoriaAtualizada = request.json
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Vrf se a categoria a ser atualizada n é nula.
        resultset = getCategoriaById(idCategoria)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute("update categorias set nome=? where id=?",
                            (categoriaAtualizada['nome'], idCategoria))
            # 3.1 - Confirmar - commit.
            connection.commit()
            # Adicionar id ao json.
            categoriaAtualizada['id'] = idCategoria
            return jsonify(categoriaAtualizada), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Categoria não encontrada'}), 404)



@Categorias_BluePrint.route("/<int:idCategoria>", methods=["DELETE"])
def categorias_delete(idCategoria):
    try:
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Vrf se a categoria a ser atualizada existe "nao é nula".
        resultset = getCategoriaById(idCategoria)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute(
                "delete from categorias where id = ?", (idCategoria, ))
            # 3.1 - Confirmar - commit.
            connection.commit()
            return {'mensagem': " Categoria removida com sucesso"}, 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Categoria não encontrada'}), 404)