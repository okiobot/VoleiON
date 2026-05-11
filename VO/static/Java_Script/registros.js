document.addEventListener('DOMContentLoaded', function () {

    const eventos = JSON.parse(
        document.getElementById('eventos-data').textContent
    );

    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: eventos,


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