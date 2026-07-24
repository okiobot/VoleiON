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

            if (info.event.extendedProps.tipo === "aniversario") {
                alert(`Hoje é aniversário de ${info.event.title.replace('Aniversário: ', '')}! Deixe seus parabéns!`);
                return;
            }

            const idBruto = info.event.id
            const idEvento = idBruto.replace('jogo_', '');

            fetch(`/jogo/${idEvento}/`)
                .then(response => response.json())
                .then(data => {

                    document.getElementById('detalhe-nome').textContent = data.nome;
                    document.getElementById('detalhe-data').textContent = data.data_hora;
                    document.getElementById('detalhe-organizador').textContent = data.organizador;
                    document.getElementById('detalhe-qtd').textContent = data.quant_participantes;

                    function atualizarPainel() {
                        fetch(`/jogo/${idEvento}/`)
                        .then(res => res.json())
                        .then(dataAtualizada => {
                            document.getElementById('detalhe-qtd').textContent = dataAtualizada.quant_participantes;

                            const ul = document.getElementById('lista-participantes');
                            ul.innerHTML = "";
                            dataAtualizada.participantes.forEach(nome => {
                                const li = document.createElement('li');
                                li.textContent = nome;
                                ul.append(li);
                            });

                            btnDeletar.classList.add('hidden');
                            btnInscrever.classList.add('hidden');
                            btnIniciar.classList.add('hidden');
                            btnSair.classList.add('hidden');

                            if (dataAtualizada.criador || dataAtualizada.criador) {
                                btnDeletar.classList.remove('hidden');
                                if (dataAtualizada.quant_participantes >= 2) {
                                    btnIniciar.classList.remove('hidden');
                                }
                            } else if (dataAtualizada.ja_inscrito) {
                                btnSair.classList.remove('hidden');
                            } else {
                                btnInscrever.classList.remove('hidden');
                            }
                        });
                    }

                    const ul = document.getElementById('lista-participantes');
                    ul.innerHTML = "";
                    data.participantes.forEach(nome => {
                        const li = document.createElement('li');
                        li.textContent = nome;
                        ul.appendChild(li);
                    });

                    const btnInscrever = document.getElementById('btn-inscrever');
                    const btnSair = document.getElementById('btn-sair-jogo');
                    const btnDeletar = document.getElementById('btn-deletar-jogo');
                    const btnIniciar = document.getElementById('btn-iniciar-jogo');

                    btnIniciar.classList.add('hidden');
                    btnInscrever.classList.add('hidden');
                    btnSair.classList.add('hidden');
                    btnDeletar.classList.add('hidden');

                    const Criador = data.criador || data.criador;
                    if (Criador) {
                        btnDeletar.classList.remove('hidden');
                        if (data.quant_participantes >= 2) {
                            btnIniciar.classList.remove('hidden');
                            btnIniciar.onclick = function() {
                                window.location.href = `/jogo/${idEvento}/partida/`;
                            };
                        }
                    }   else if (data.ja_inscrito) {
                        btnSair.classList.remove('hidden');
                    } else {
                        btnInscrever.classList.remove('hidden');
                    }

                    painel.classList.remove('hidden');

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
                        .then(resData => { 
                            if (resData.sucesso !== false) {
                                atualizarPainel();
                            } 
                        })
                        .catch(err => console.error("Erro ao se inscrever: ", err))
                    };

                    // Sair do jogo
                    btnSair.onclick = function() {
                        fetch(`/jogo/${idEvento}/sair/`, {
                            method: "POST",
                            headers: { "X-CSRFToken": getCookie("csrftoken")}
                        })
                        .then(res => res.json())
                        .then(resData => {
                            if (resData.sucesso !== false) {
                                atualizarPainel();
                            }
                        })
                        .catch(err => console.error("Erro ao sair: ", err))
                    }

                    if (data.criador) {
                        btnDeletar.classList.remove('hidden')

                        if (data.quant_participantes >= 2) {
                            btnIniciar.classList.remove('hidden');
                            btnIniciar.onclick = function() {
                                const confimar = confirm("Deseja realmente iniciar a partida?\n\nApós o início, não será mais possível alterar os participantes.");

                                if (confimar) {
                                    window.location.href = `/jogo/${idEvento}/partida/`;
                                }
                            };
                        }
                    } else if (data.ja_inscrito) {
                        btnSair.classList.remove('hidden');
                    } else {
                        btnInscrever.classList.remove('hidden');
                    }

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
    calendar.refetchEvents();

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