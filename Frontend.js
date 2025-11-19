function verificar() {
    const membros = document.getElementById("membros").value;

    fetch("http://localhost:5000/verificar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ membros: membros })
    })
    .then(r => r.json())
    .then(dados => {
        document.getElementById("resposta").innerText = dados.resposta;
    })
    .catch(err => {
        document.getElementById("resposta").innerText =
            "Erro ao comunicar com o servidor.";
        console.error(err);
    });
}
