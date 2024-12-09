from flask import Flask
from endpoints.Produtos import Produtos_BluePrint
from endpoints.Usuarios import Usuarios_BluePrint
from helpers.aplicattion import app
from endpoints.Categorias import Categorias_BluePrint
from endpoints.Setores import Setores_BluePrint

app.register_blueprint(Produtos_BluePrint, url_prefix="/produtos")
app.register_blueprint(Usuarios_BluePrint, url_prefix="/usuarios")
app.register_blueprint(Categorias_BluePrint, url_prefix="/categorias")
app.register_blueprint(Setores_BluePrint, url_prefix="/setores")


if __name__ == "__main__":
    app.run(debug=True)
