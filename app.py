from flask import Flask, request, render_template
from time import strptime

app = Flask(__name__)

def paragaphe():
  
   return render_template("index.html", texte="test"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
