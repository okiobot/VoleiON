document.addEventListener('DOMContentLoaded', function () {
    
    const eventos = window.dadosEventosCalendario || [];

    const calendarEl = document.getElementById('calendar');
    const painel = document.getElementById('painel-detalhes');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: eventos,

        dateClick: function(info) {
            const titulo = "Jogo";
            fetch("/registrar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: new URLSearchParams({
                    nome: titulo,
                    data_hora: info.dateStr
                })
            })
            .then(response => response.json())
            .then(data => {
                location.reload();
            })
            .catch(error => console.log(error));
        },

       eventClick: function(info) {
            const idEvento = info.event.id;

            fetch(`/jogo/${idEvento}/`)
                .then(response => response.json())
                .then(data => {

                    document.getElementById('detalhe-nome').textContent = data.nome;
                    document.getElementById('detalhe-data').textContent = data.data_hora;
                    document.getElementById('detalhe-organizador').textContent = data.organizador;
                    document.getElementById('detalhe-qtd').textContent = data.quant_participantes;

                    const ul = document.getElementById('lista-participantes');
                    ul.innerHTML = ""; // Limpa a lista antiga
                    data.participantes.forEach(nome => {
                        const li = document.createElement('li');
                        li.textContent = nome;
                        ul.appendChild(li);
                    });

                    const btnInscrever = document.getElementById('btn-inscrever');
                    const btnSair = document.getElementById('btn-sair-jogo');
                    const btnDeletar = document.getElementById('btn-deletar-jogo');

                    btnInscrever.classList.add('hidden');
                    btnSair.classList.add('hidden');
                    btnDeletar.classList.add('hidden');

                    if (data.criador) {
                        btnDeletar.classList.remove('hidden');
                    } else if (data.ja_inscrito) {
                        btnSair.classList.remove('hidden');
                    } else {
                        btnInscrever.classList.remove('hidden');
                    }

                    painel.classList.remove('hidden');

                    // Ação de se Inscrever
                    btnInscrever.onclick = function() {
                        fetch(`/jogo/${idEvento}/inscrever/`, {
                            method: "POST",
                            headers: { "X-CSRFToken": getCookie("csrftoken") }
                        })
                        .then(res => res.json())
                        .then(() => { 
                            calendar.getEventById(idEvento).setProp('title', `Jogo (${data.quant_participantes + 1} pessoas)`); 
                            info.el.click(); 
                        });
                    };

                    // Ação de Sair do Jogo
                    btnSair.onclick = function() {
                        fetch(`/jogo/${idEvento}/sair/`, {
                            method: "POST",
                            headers: { "X-CSRFToken": getCookie("csrftoken") }
                        })
                        .then(res => res.json())
                        .then(() => { info.el.click(); }); 
                    };

                    // Ação de Deletar o Jogo (Exclusiva para o criador)
                    btnDeletar.onclick = function() {
                        if (confirm("Deseja apagar este evento permanentemente?")) {
                            window.location.href = `/deletar/${idEvento}/`;
                        }
                    };
                })
                .catch(error => console.error("Erro ao buscar detalhes:", error));
        }
    });

    calendar.render();

    document.getElementById('fechar-painel').addEventListener('click', function() {
        painel.classList.add('hidden');
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}