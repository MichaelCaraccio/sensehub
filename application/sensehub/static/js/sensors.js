'use strict';

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    loading: false,
    sensors: []
  }
})

window.onload = init

function init()
{
    app.loading = true;
    fetch('/api/sensors/', {
        method: "GET",
        credentials: 'same-origin', // this allows the credentials to be kept (logged in user)
    })
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.status === "ok") {
            data.message.sort((a,b)=> a.id-b.id);
            data.message.forEach(function(sensor){
                sensor.url = '/sensors/'+ sensor.id;
                app.sensors.push(sensor);
            });
            app.loading = false;
        }
    }).catch((error) => console.log("Error getting the data: "+error));
}
