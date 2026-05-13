let calendar;
let calendarioCriado = false;

function abrirCalendario(){

    document.getElementById("modalCalendario").style.display = "block";

    if (!calendarioCriado){

        const eventos = JSON.parse(
            document.getElementById('eventos-data').textContent
        );

        console.log(eventos);

        const calendarEl = document.getElementById('calendar');

        calendar = new FullCalendar.Calendar(calendarEl, {

            initialView: 'dayGridMonth',

            events: eventos

        });

        calendar.render();

        calendarioCriado = true;
    }

    calendar.updateSize();
}

function fecharCalendario(){

    document.getElementById("modalCalendario").style.display = "none";
}