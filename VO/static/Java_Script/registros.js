document.addEventListener('DOMContentLoaded', function () {

    const eventos = JSON.parse(
        document.getElementById('eventos-data').textContent
    );

    const calendarEl = document.getElementById('calendar');

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
    .catch(error => {
    console.log(error);
    });
    },


        eventClick: function(info) {
            const idEvento = info.event.id;
            const confirmar = confirm(
                "Deseja apagar este evento?"
            );
            if(confirmar){
                window.location.href =
                    `/deletar/${idEvento}/`;
            }
        }
    });

    calendar.render();

});



function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}