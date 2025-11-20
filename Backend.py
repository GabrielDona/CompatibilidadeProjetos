from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pyswip import Prolog
import os
import threading

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 🔧 Ajuste o caminho do SWI se for diferente
os.environ["SWI_HOME_DIR"] = r"C:\Program Files\swipl"
os.environ["PATH"] += r";C:\Program Files\swipl\bin"

# 🔧 Inicializa Prolog UMA vez só
prolog = Prolog()
prolog.consult("Regras.pl")

# 🔒 Lock para evitar chamadas concorrentes ao Prolog
prolog_lock = threading.Lock()


@app.route("/")
def home():
    # Se seu arquivo chama Interface.html
    return send_from_directory(".", "Interface.html")


@app.route("/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    membros_str = dados.get("membros", "")

    membros = [m.strip().lower() for m in membros_str.split(",") if m.strip()]

    if not membros:
        return jsonify({"resposta": "Informe pelo menos um membro."}), 400

    # monta [ana,bruno,...]
    membros_lista_prolog = "[" + ",".join(membros) + "]"

    # 👇 AQUI protegemos o acesso ao Prolog
    with prolog_lock:
        consulta = list(
            prolog.query(
                f"verificar_adequacao(sistema_web, {membros_lista_prolog}, R)"
            )
        )

    if not consulta:
        return jsonify({
            "resposta": "Não foi possível verificar o time. Confira os nomes."
        })

    resultado = consulta[0]["R"]

    if str(resultado) == "adequado":
        msg = "✅ O grupo atende às necessidades do projeto."
    else:
        msg = "❌ O grupo NÃO atende às necessidades do projeto."

    return jsonify({"resposta": msg})


if __name__ == "__main__":
    # 🚫 Nada de debug/reloader/multithread com Prolog
    app.run(debug=False, threaded=False)
    # Se quiser debug visual mas sem reloader:
    # app.run(debug=True, use_reloader=False, threaded=False)
