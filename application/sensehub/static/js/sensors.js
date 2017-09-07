'use strict';

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    sensors: []
  }
})

window.onload = init

function init()
{
    fetch('/api/sensors/',{
        method: "GET",
        credentials: 'same-origin', // this allows the credentials to be kept (logged in user)
})
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.status === "ok")
        {
            data.message.forEach(function(sensor){
                console.log(sensor);
                app.sensors.push(sensor);
            });
        }
    }).catch((error) => console.log("Error getting the data: "+error));
}
