from flask import Flask, render_template, request
import subprocess
import main

app = Flask(__name__)


@app.before_request
def before_request():
    app.logger.info('Middleware triggered before request')
    main.run()  # Chame a função de main.py

@app.route("/")
def homepage():
    return render_template("Mapa - Autocarros de Lamego - PT.html")

if __name__ == "__main__":
    app.run(debug=True)
