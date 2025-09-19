from flask import Flask, request, render_template
from time import strptime

app = Flask(__name__)

def paragaphe():
  dico = {"18/9":"gfxdnwxstdgfwxd",
          "19/9":"kuhygfjhdrfgdrsjhyer"
         }
  
   return render_template("index.html", texte=dico(strptime(%j)+"/"+strptime(%m))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
