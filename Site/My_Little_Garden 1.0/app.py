from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/sobre")
def sobre():
    return "Página Sobre"
@app.route("/mecanicas")
def mecanicas():
    return "Página Mecânicas"
@app.route("/personagens")
def personagens():
    return "Página Personagens"
@app.route("/ambiental")
def ambiental():
    return "Página Recuperação"
@app.route("/login")
def login():
    return "Página de Login"
if __name__ == "__main__":
    app.run(debug=True)