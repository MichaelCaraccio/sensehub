'use strict';

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    sensor: []
  }
})

window.onload = init

function init()
{
    app.loading = true;
    fetch('/api/sensor/' + sensor_id, {
        method: "GET",
        credentials: 'same-origin', // this allows the credentials to be kept (logged in user)
    })
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.status === "ok") {
            data.message.forEach(function(sensor){
                app.sensor = sensor;
            });
            app.loading = false;
        }
    }).catch((error) => console.log("Error getting the data: "+error));
}
