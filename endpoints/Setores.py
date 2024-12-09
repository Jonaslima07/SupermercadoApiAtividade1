from flask import Blueprint, request, jsonify
import sqlite3
from helpers.database import getConnection
from helpers.logging import logger
from Models.Setores import Setores

Setores_BluePrint = Blueprint('setores', __name__)

@Setores_BluePrint.route("/", methods=["GET"])
def setores_get():
    try:
        logger.info("Listando setores")
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from setores")
        # 4 - retorna resultset
        resultset = cursor.fetchall()
        # Iterar e transformar dados.
        setores = []
        for item in resultset:
            id = item[0]
            nome = item[1]
            setor = Setores(id, nome)
            logger.info(setor)
            setores.append(setor.toJson())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(setores), 200


@Setores_BluePrint.route("/", methods=["POST"])
def setores_post():
    # Captar o json da requisição e adicionar na lista.
    setoresNovos = request.json

    # Manipulação do dados antiga.
    # setoresNovos['id'] = calcularProximoId()
    # setores.append(setoresNovos)
    # 1 - Conectar.
    connection = getConnection()

    # 2 - Obter cursor.
    cursor = connection.cursor()

    # 3 - Executar.
    cursor.execute(
        "insert into setores(nome) values (?)", (setoresNovos['nome'],))

    # 3.1 - Confirmar - commit.
    connection.commit()

    id = cursor.lastrowid
    setoresNovos['id'] = id

    return jsonify(setoresNovos), 200


def getSetorById(idSetores):
    try:
        # Retornar o resultset.
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from setores where id = ?", (idSetores,))
        # 4 - Retornar resultset
        resultset = cursor.fetchone()  # [] -> ()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return resultset


@Setores_BluePrint.route("/<int:idSetores>", methods=["GET"])
def produto_get(idSetores):
    try:
        
        resultset = getSetorById(idSetores)
        # Vrf se resultset n é nulo e transforma os dados.
        if resultset is not None:
            setor = {
                'id': resultset[0],
                'nome': resultset[1],
            }
        else:
            return jsonify({'mensagem': 'setor não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(setor), 200


@Setores_BluePrint.route("/<int:idSetores>", methods=["PUT"])
def setores_put(idSetores):
    try:
        # Captar o json da requisição e adicionar na lista.
        setorAtualizado = request.json
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Vrf se o setor a ser atualizado existe.
        resultset = getSetorById(idSetores)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute("update setores set nome=? where id=?",
                            (setorAtualizado['nome'], idSetores))
            # 3.1 - Confirmar - commit.
            connection.commit()
            # Adicionar id ao json.
            setorAtualizado['id'] = idSetores
            return jsonify(setorAtualizado), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'setor não encontrado'}), 404)



@Setores_BluePrint.route("/<int:idSetores>", methods=["DELETE"])
def setores_delete(idSetores):
    try:
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Vrf se a pripriedade a ser atualizada existe.
        resultset = getSetorById(idSetores)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute(
                "delete from setores where id = ?", (idSetores, ))
            # 3.1 - Confirmar - commit.
            connection.commit()
            return {'mensagem': " setor removido com sucesso"}, 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return (jsonify({'mensagem': 'setor não encontrado'}), 404)