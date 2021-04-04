import os  
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, Usuarios, Roles, Pruebas, Preguntas, Alternativas, Distraccion
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from functions import allowed_file
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS_IMAGES = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG '] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'jerosantamariai@gmail.com' #La cuenta de correo electronico de donde saldran los correos
app.config['MAIL_PASSWORD'] = ''
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static')
jwt = JWTManager(app)

db.init_app(app)

Migrate(app, db)
CORS(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route("/")
def root():
    return render_template('index.html')

@app.route('/pruebas', methods=['GET', 'POST'])
@app.route('/pruebas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required
def pruebas(id = None):
    if request.method == 'GET':
        if id is not None:
            prueba = Pruebas.query.get(id)
            if prueba:
                return jsonify(prueba.serialize()), 200
            else:
                return jsonify({"msg": "Prueba no existe"}), 404
        else:
            pruebas = Pruebas.query.all()
            print("aqui!!")
            pruebas = list(map(lambda prueba: prueba.serialize(), pruebas))
            return jsonify(pruebas), 200

    if request.method == 'POST':
        tipo = request.json.get('tipo', None)
        descripcion = request.json.get('descripcion', None)
        
        pruebas = Pruebas()
        
        pruebas.tipo = tipo 
        pruebas.descripcion = descripcion 
        
        db.session.add(pruebas) 
        db.session.commit()  

        return jsonify(pruebas.serialize()), 201
    
    if request.method == 'PUT':
        tipo = request.json.get('tipo', None)
        descripcion = request.json.get('descripcion', None)

        if not tipo or tipo == "":
            return jsonify({"msg":"Ingresar tipo de prueba"}), 400
        if not descripcion or descripcion == "":
            return jsonify({"msg":"Ingresar descripción de la prueba"}), 400

        pruebas = Pruebas.query.get(id)
        if not users:
            return jsonify({"msg": "Prueba no encontrada"}), 404
         
        pruebas.tipo = tipo 
        pruebas.descripcion = descripcion 
        
        db.session.commit()  

        return jsonify(pruebas.serialize()), 201

    if request.method == 'DELETE':
        pruebas = Pruebas.query.get(id)
        if not pruebas:
            return jsonify({"msg": "Prueba no encontrada"}), 404
        db.session.delete(pruebas)
        db.session.commit()
        return jsonify({"msg":"Prueba eliminada"}), 200

@app.route('/preguntas', methods=['GET', 'POST'])
@app.route('/preguntas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required
def preguntas(id = None):
    if request.method == 'GET':
        if id is not None:
            pregunta = Preguntas.query.get(id)
            if pregunta:
                return jsonify(pregunta.serialize()), 200
            else:
                return jsonify({"msg": "Pregunta no existe"}), 404
        else:
            preguntas = Preguntas.query.all()
            print("aqui!!")
            preguntas = list(map(lambda pregunta: pregunta.serialize(), preguntas))
            return jsonify(preguntas), 200

    if request.method == 'POST':
        enunciado = request.json.get('enunciado', None)
        prueba_id = request.json.get('prueba_id', None)
        
        preguntas = Pruebas()
        
        preguntas.enunciado = enunciado 
        preguntas.prueba_id = prueba_id 
        
        db.session.add(preguntas) 
        db.session.commit()  

        return jsonify(preguntas.serialize()), 201
    
    if request.method == 'PUT':
        enunciado = request.json.get('enunciado', None)
        prueba_id = request.json.get('prueba_id', None)

        if not enunciado or enunciado == "":
            return jsonify({"msg":"Ingresar enunciado de prueba"}), 400
        if not prueba_id or prueba_id == "":
            return jsonify({"msg":"Ingresar a que prueba pertenece"}), 400

        preguntas = Preguntas.query.get(id)
        if not preguntas:
            return jsonify({"msg": "Pregunta no encontrada"}), 404
         
        preguntas.enunciado = enunciado 
        preguntas.prueba_id = prueba_id 
        
        db.session.commit()  

        return jsonify(preguntas.serialize()), 201

    if request.method == 'DELETE':
        preguntas = Preguntas.query.get(id)
        if not preguntas:
            return jsonify({"msg": "Pregunta no encontrada"}), 404
        db.session.delete(preguntas)
        db.session.commit()
        return jsonify({"msg":"Pregunta eliminada"}), 200

@app.route('/alternativas', methods=['GET', 'POST'])
@app.route('/alternativas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required
def alternativas(id = None):
    if request.method == 'GET':
        if id is not None:
            alternativa = Alternativas.query.get(id)
            if alternativa:
                return jsonify(alternativa.serialize()), 200
            else:
                return jsonify({"msg": "Alternativa no existe"}), 404
        else:
            alternativas = Alternativas.query.all()
            print("aqui!!")
            alternativas = list(map(lambda alternativa: alternativa.serialize(), alternativas))
            return jsonify(alternativas), 200

    if request.method == 'POST':
        enunciado = request.json.get('enunciado', None)
        prueba_id = request.json.get('prueba_id', None)
        
        preguntas = Pruebas()
        
        preguntas.enunciado = enunciado 
        preguntas.prueba_id = prueba_id 
        
        db.session.add(preguntas) 
        db.session.commit()  

        return jsonify(preguntas.serialize()), 201
    
    if request.method == 'PUT':
        enunciado = request.json.get('enunciado', None)
        prueba_id = request.json.get('prueba_id', None)

        if not enunciado or enunciado == "":
            return jsonify({"msg":"Ingresar enunciado de prueba"}), 400
        if not prueba_id or prueba_id == "":
            return jsonify({"msg":"Ingresar a que prueba pertenece"}), 400

        preguntas = Preguntas.query.get(id)
        if not preguntas:
            return jsonify({"msg": "Pregunta no encontrada"}), 404
         
        preguntas.enunciado = enunciado 
        preguntas.prueba_id = prueba_id 
        
        db.session.commit()  

        return jsonify(preguntas.serialize()), 201

    if request.method == 'DELETE':
        preguntas = Preguntas.query.get(id)
        if not preguntas:
            return jsonify({"msg": "Pregunta no encontrada"}), 404
        db.session.delete(preguntas)
        db.session.commit()
        return jsonify({"msg":"Pregunta eliminada"}), 200





@manager.command
def cargarprueba():
    prueba = Pruebas()
    prueba.tipo = "Prueba 1"
    prueba.descripcion = "Descripción prueba 1"

    db.session.add(prueba)
    db.session.commit()

    prueba = Pruebas()
    prueba.tipo = "Prueba 2"
    prueba.descripcion = "Descripción prueba 2"

    db.session.add(prueba)
    db.session.commit()

    print("Pruebas Creadas")

@manager.command
def cargarpregunta():
    pregunta = Preguntas()
    pregunta.enunciado = "Pregunta 1 Prueba 1"
    pregunta.prueba_id = "1"

    db.session.add(pregunta)
    db.session.commit()

    pregunta = Preguntas()
    pregunta.enunciado = "Pregunta 2 Prueba 1"
    pregunta.prueba_id = "1"

    db.session.add(pregunta)
    db.session.commit()

    pregunta = Preguntas()
    pregunta.enunciado = "Pregunta 3 Prueba 1"
    pregunta.prueba_id = "1"

    db.session.add(pregunta)
    db.session.commit()

    pregunta = Preguntas()
    pregunta.enunciado = "Pregunta 1 Prueba 2"
    pregunta.prueba_id = "2"

    db.session.add(pregunta)
    db.session.commit()

    pregunta = Preguntas()
    pregunta.enunciado = "Pregunta 2 Prueba 2"
    pregunta.prueba_id = "2"

    db.session.add(pregunta)
    db.session.commit()

    print("Preguntas Creadas")

@manager.command
def cargaralternativas():
    alternativa = Alternativas()
    alternativa.correcta = "Respuesta correcta a Pregunta 1 Prueba 1"
    alternativa.pregunta_id = "1"

    db.session.add(alternativa)
    db.session.commit()

    alternativa = Alternativa()
    alternativa.correcta = "Respuesta correcta a Pregunta 2 Prueba 1"
    alternativa.pregunta_id = "2"

    db.session.add(alternativa)
    db.session.commit()

    alternativa = Alternativas()
    alternativa.correcta = "Respuesta correcta a Pregunta 3 Prueba 1"
    alternativa.pregunta_id = "3"

    db.session.add(alternativa)
    db.session.commit()

    alternativa = Alternativas()
    alternativa.correcta = "Respuesta correcta a Pregunta 1 Prueba 2"
    alternativa.pregunta_id = "4"

    db.session.add(alternativa)
    db.session.commit()

    alternativa = Alternativas()
    alternativa.correcta = "Respuesta correcta a Pregunta 2 Prueba 2"
    alternativa.pregunta_id = "5"

    db.session.add(alternativa)
    db.session.commit()

    print("Respuestas Correctas Creadas")

@manager.command
def cargardistraccion():
    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 1 a Pregunta 1 Prueba 1"
    distrae.alternativa_id = "1"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 2 a Pregunta 1 Prueba 1"
    distrae.alternativa_id = "1"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 3 a Pregunta 1 Prueba 1"
    distrae.alternativa_id = "1"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 4 a Pregunta 1 Prueba 1"
    distrae.alternativa_id = "1"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 5 a Pregunta 1 Prueba 1"
    distrae.alternativa_id = "1"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 1 a Pregunta 2 Prueba 1"
    distrae.alternativa_id = "2"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 2 a Pregunta 2 Prueba 1"
    distrae.alternativa_id = "2"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 3 a Pregunta 2 Prueba 1"
    distrae.alternativa_id = "2"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 4 a Pregunta 2 Prueba 1"
    distrae.alternativa_id = "2"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 5 a Pregunta 2 Prueba 1"
    distrae.alternativa_id = "2"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 1 a Pregunta 3 Prueba 1"
    distrae.alternativa_id = "3"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 2 a Pregunta 3 Prueba 1"
    distrae.alternativa_id = "3"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 3 a Pregunta 3 Prueba 1"
    distrae.alternativa_id = "3"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 4 a Pregunta 3 Prueba 1"
    distrae.alternativa_id = "3"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 5 a Pregunta 3 Prueba 1"
    distrae.alternativa_id = "3"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 1 a Pregunta 1 Prueba 2"
    distrae.alternativa_id = "4"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 2 a Pregunta 1 Prueba 2"
    distrae.alternativa_id = "4"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 3 a Pregunta 1 Prueba 2"
    distrae.alternativa_id = "4"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 4 a Pregunta 1 Prueba 2"
    distrae.alternativa_id = "4"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 5 a Pregunta 1 Prueba 2"
    distrae.alternativa_id = "4"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 1 a Pregunta 2 Prueba 2"
    distrae.alternativa_id = "5"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 2 a Pregunta 2 Prueba 2"
    distrae.alternativa_id = "5"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 3 a Pregunta 2 Prueba 2"
    distrae.alternativa_id = "5"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 4 a Pregunta 2 Prueba 2"
    distrae.alternativa_id = "5"

    db.session.add(distrae)
    db.session.commit()

    distrae = Distraccion()
    distrae.incorrecta = "Respuesta incorrecta 5 a Pregunta 2 Prueba 2"
    distrae.alternativa_id = "5"

    db.session.add(distrae)
    db.session.commit()

    print("Distracciones Creadas")

aun no
    # @manager.command
    # def loadroles():
    #     role = Roles()
    #     role.rolename = "admin"

    #     db.session.add(role)
    #     db.session.commit()

    #     role = Roles()
    #     role.rolename = "customer"

    #     db.session.add(role)
    #     db.session.commit()

    #     print("Roles Creados")

    # @manager.command
    # def loadadmin():
    #     users = Users()
    #     users.email = "admin@gmail.com"
    #     users.password = bcrypt.generate_password_hash("123456")
    #     users.role_id = "1"

    #     db.session.add(users)
    #     db.session.commit()

    #     print("Administrador Creado! Buena Suerte!")

if __name__ == '__main__':
    manager.run()