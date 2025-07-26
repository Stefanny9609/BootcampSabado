import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)#Crear una aplicacion con flask que en algun momento se le dara nombre
CORS(app)

listaPersonas=[]
resultadosPersonas=[]

db = mysql.connector.connect(  #usando la libreria nos vamos a conectar con:
    host="localhost",           #mi equipo      
    user="root",                #usuario raiz    
    password="1053587088Nobs@",     #contraseña que cree al instalar mySQL
    database="sabadoJulio"          #nombre base de datos a conectar    
)
cursor = db.cursor(dictionary=True)    # permite ejecutar consultas, dictionary convierte el formato en json de python para poder acceder desde javascript

query = "SELECT * FROM persona"

@app.route('/mensaje',methods=['GET']) # metodo GET, yo soy quien recibe
def mensaje():
    return 'LISTA DE PERSONAS'

@app.route('/listarPersonas',methods=['GET'])
def listar():
    return jsonify(listaPersonas)

@app.route('/agregarPersona',methods=['POST'])
def agregar():
    newperson = request.json.get('persona')
    listaPersonas.append(newperson)
    return 'Se agrego una nueva persona'

@app.route('/datosBase',methods=['GET']) # metodo GET, yo soy quien recibe
def datosbase():
    cursor.execute(query)
    resultadosPersonas = cursor.fetchall()
    return jsonify(resultadosPersonas)

@app.route('/agregarPersonasBD', methods=['POST'])
def agregarBD():
    nuevaPersona = request.json.get('persona')
    resultadosPersonas.append(nuevaPersona)
    cursor.execute("INSERT INTO persona (identificacion, nombre, edad) VALUES(%s,%s,%s)",
    (nuevaPersona['identificacion'],nuevaPersona['nombre'],nuevaPersona['edad']))
    db.commit()
    return 'Se agrego una nueva persona'

@app.route('/buscarPersona/<identificacion>',methods=['GET'])
def buscar(identificacion):
    cursor.execute("SELECT *from persona WHERE identificacion = %s", (identificacion,))
    resultadoPersona=cursor.fetchall()
    return jsonify(resultadoPersona)

@app.route('/actualizarPersona/<identificacion>', methods=['PUT'])
def actualizar(identificacion):
    datos_nuevos=request.json
    cursor.execute("UPDATE persona SET nombre=%s,edad=%s WHERE identificacion=%s",
    (datos_nuevos['nombre'], datos_nuevos['edad'], datos_nuevos['identificacion']))
    db.commit()
    return "Persona actualizada"

@app.route('/eliminarPersona/<identificacion>',methods=['DELETE'])
def eliminar(identificacion):
    cursor.execute("DELETE FROM persona WHERE identificacion=%s",(identificacion,))
    db.commit()
    return "Persona eliminada"

if __name__=='__main__':  # solo va una vez
    app.run(debug=True)


#{"persona":{"Nombre":"Carlos","Edad":31,"Profesion":"Ingeniero"}}