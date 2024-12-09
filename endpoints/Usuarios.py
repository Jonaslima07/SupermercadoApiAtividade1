from flask import Blueprint, request, jsonify
import sqlite3
from helpers.database import getConnection
from helpers.logging import logger
from Models.Usuarios import Usuarios

Usuarios_BluePrint = Blueprint('usuarios', __name__)

@Usuarios_BluePrint.route("/", methods=["GET"])
def usuarios_get():
    try:
        logger.info("Listando usuarios")
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from usuarios")
        # 4 - retorna resultset
        resultset = cursor.fetchall()
        # Iterar e transformar dados.
        usuarios = []
        for item in resultset:
            id = item[0]
            nome = item[1]
            usuario = Usuarios(id, nome)
            logger.info(usuario)
            usuarios.append(usuario.toJson())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(usuarios), 200


@Usuarios_BluePrint.route("/", methods=["POST"])
def usuarios_post():
    # Captar o json da requisição e adicionar na lista.
    usuariosNovos = request.json

    # Manipulação do dados antiga.
    # usuariosNovos['id'] = calcularProximoId()
    # usuarios.append(usuariosNovos)
    # 1 - Conectar.
    connection = getConnection()

    # 2 - Obter cursor.
    cursor = connection.cursor()

    # 3 - Executar.
    cursor.execute(
        "insert into usuarios(nome) values (?)", (usuariosNovos['nome'],))

    # 3.1 - Confirmar - commit.
    connection.commit()

    id = cursor.lastrowid
    usuariosNovos['id'] = id

    return jsonify(usuariosNovos), 200


def getUsuariosById(idUsuarios):
    try:
        # Retornar o resultset.
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from usuarios where id = ?", (idUsuarios,))
        # 4 - Retornar resultset
        resultset = cursor.fetchone()  # [] -> ()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return resultset


@Usuarios_BluePrint.route("/<int:idUsuarios>", methods=["GET"])
def produto_get(idUsuarios):
    try:
        
        resultset = getUsuariosById(idUsuarios)
        # Vrf se resultset n é nulo e transforma os dados.
        if resultset is not None:
            usuario = {
                'id': resultset[0],
                'nome': resultset[1],
            }
        else:
            return jsonify({'mensagem': 'Usuarios não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(usuario), 200


@Usuarios_BluePrint.route("/<int:idUsuarios>", methods=["PUT"])
def usuarios_put(idUsuarios):
    try:
        # Captar o json da requisição e adicionar na lista.
        produtoAtualizado = request.json
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # vrf se o usuario a ser atualizado existe.
        resultset = getUsuariosById(idUsuarios)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute("update usuarios set nome=? where id=?",
                            (produtoAtualizado['nome'], idUsuarios))
            # 3.1 - Confirmar - commit.
            connection.commit()
            # Adicionar id ao json.
            produtoAtualizado['id'] = idUsuarios
            return jsonify(produtoAtualizado), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Usuarios não encontrado'}), 404)



@Usuarios_BluePrint.route("/<int:idUsuarios>", methods=["DELETE"])
def usuarios_delete(idUsuarios):
    try:
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Vrf se o usuario a ser atualizado existe.
        resultset = getUsuariosById(idUsuarios)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute(
                "delete from usuarios where id = ?", (idUsuarios, ))
            # 3.1 - Confirmar - commit.
            connection.commit()
            return {'mensagem': " Usuario removido com sucesso"}, 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'Usuario não encontrado'}), 404)