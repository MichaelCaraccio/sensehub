'use strict';

Vue.use(VueEventCalendar.default, {locale: 'en', color: '#4fc08d'}) //hack here (.default)

Vue.component('video-component', {
  template: '#my-video-component',
  props: ['src']
})

Vue.component('image-component', {
  template: '#my-image-component',
  props: ['src']
})

var app = new Vue({
  el: '#calendar',
  delimiters: ['[[', ']]'],
  data: function(){
      return {
        demoEvents : [],
        currentLink: "#",
        current: "video-component",
        seen: false,
        type: "video"
    };
  },
  methods: {
      setCurrent: function(source, type){
          this.seen = true;
          this.currentLink = source;

          if(type == "video"){
            this.current = 'video-component';
          } else if (type == "image") {
            this.current = 'image-component';
          }
      }
  }
});

window.onload = getValues;

function getValues()
{
  // TODO Dynamic date
  fetch('/api/sensor/' + sensor_id + "?from=2017-01-01&to=2017-10-01", {
      method: "GET",
      credentials: 'same-origin', // this allows the credentials to be kept (logged in user)
    })
  .then((resp) => resp.json())
  .then(function(data) {
    if (data.status === "ok") {
        data.message.forEach(function(value){
          console.log(value)

            var newEvent =
                {
                  date: value.timestamp.replace(/-/g, '/'),
                  data: value,
                  title: "Title"
              };
            console.log(newEvent);
            app.demoEvents.push(newEvent);
        });
    }
  }).catch((error) => console.log("Error getting the data: "+error));
}
