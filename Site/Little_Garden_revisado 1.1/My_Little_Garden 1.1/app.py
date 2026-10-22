from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
@app.route("/mecanicas")
def mecanicas():
    return render_template("mecanicas.html")
@app.route("/personagens")
def personagens():
    return render_template("personagens.html")
@app.route("/ambiental")
def ambiental():
    return render_template("ambiental.html")
if __name__ == "__main__":
    # Apenas para desenvolvimento local. Não usar debug=True em produção.
    app.run(debug=True)