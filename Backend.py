from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)
CORS(app)  #libera acesso do frontend (HTML/JS)

#Configuração Prolog
prolog = Prolog()
prolog.consult("Regras.pl")


@app.route("/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    membros_str = dados.get("membros", "")

    # transforma "ana, bruno" -> ['ana', 'bruno']
    membros = [m.strip().lower() for m in membros_str.split(",") if m.strip()]

    if not membros:
        return jsonify({"resposta": "Por favor, informe pelo menos um membro no time."}), 400

    # monta a lista no formato Prolog: [ana,bruno]
    membros_lista_prolog = "[" + ",".join(membros) + "]"

    # consulta Prolog: verificar_adequacao(sistema_web, [ana,bruno], R).
    consulta = list(
        prolog.query(
            f"verificar_adequacao(sistema_web, {membros_lista_prolog}, R)"
        )
    )

    if not consulta:
        return jsonify({
            "resposta": "Não foi possível verificar o time. Verifique se os nomes dos membros estão corretos."
        })

    resultado = consulta[0]["R"]  # resultado deve ser 'adequado' ou 'nao_adequado'

    if str(resultado) == "adequado":
        msg = "✅ O grupo atende às necessidades do projeto (adequado)."
    else:
        msg = "❌ O grupo NÃO atende às necessidades do projeto (não adequado)."

    return jsonify({
        "resposta": msg,
    })


if __name__ == "__main__":
    app.run(debug=True)
