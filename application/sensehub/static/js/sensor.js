'use strict';

Vue.use(VueEventCalendar.default, {locale: 'en', color: '#4fc08d'}) //hack here (.default)

Vue.component('video-component', {
  template: `<div class="card text-center">
              <div class="card-body">
                <video width="100%" autoplay controls>
                    <source :src="src" type="video/mp4" />
                </video>
              </div>
              <div class="card-footer text-muted">
                {{data.timestamp}}
              </div>
            </div>`,
  props: ['src', 'data']
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
        currentData : [],
        currentLink: "#",
        current: "video-component",
        seen: false,
        type: "video"
    };
  },
  methods: {
      setCurrent: function(index){
          var data = app.demoEvents[index].data;
          console.log(data);
          this.seen = true;
          this.currentLink = data.value;
          this.currentData = data;

          if(data.type == "video"){
            this.current = 'video-component';
          } else if (data.type == "image") {
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
        data.message.values.forEach(function(value){
          console.log(value)

            var newEvent = {
                  date: value.timestamp.replace(/-/g, '/'),
                  data: value,
                  title: "Title"
            };
            app.demoEvents.push(newEvent);

            // Load last media
            app.setCurrent(0);
        });
    }
  }).catch((error) => console.log("Error getting the data: "+error));
}
