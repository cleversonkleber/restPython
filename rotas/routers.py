


from flask import Flask,request
from cadastro import insertUser
app = Flask("APIS")

@app.route("/olamundo",methods=["GET"])
def olamundo():
    return {"ola":"mundo"}

@app.route("/cadastro/addUser",methods=["POST"])
def cadastraUser():
    body = request.get_json()
    usuario = insertUser(body["nome"],body["email"],body["senha"])
    return usuario




app.run(debug=True)




