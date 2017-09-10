'use strict';

Vue.use(VueEventCalendar.default, {locale: 'en', color: '#4fc08d'}) //hack here (.default)

Vue.component('video-slide', {
  template: '<video autoplay controls>
              <source :src="src" type="video/mp4">
            </video>'
          ,
  props: ['src']
})

var app = new Vue({
  el: '#example',
  delimiters: ['[[', ']]'],
  data: {
    demoEvents : [],
    current: 'video-slide',
    currentSlide: 0,
    slides:[
    	{
      	id: 0,
      	src: 'http://www.808.dk/vstreamer.asp?video=gizmo.mp4',
        time: 10,
        type: 3
      },
      {
      	id: 1,
      	src: 'http://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4',
        time: 150,
        type: 3
      },
      {
      	id: 2,
      	src: 'http://placehold.it/350x350',
        time: 150,
        type: 2
      }
    ]
  },
  mounted: function(){
  this.currentSlide = this.slides[0];
},
  methods: {
  	setCurrent: function(index){
      if (index == -1) {
        return;
      }

    	this.currentSlide = this.slides[index];

      switch(this.slides[index].type) {
      	case "photo":
        	this.current = 'image-slide';
          break;

        case "video":
        	this.current = 'video-slide';
          break;

        default:
        break;
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
        data.message.forEach(function(sensor){

            // TODO less data
            console.log(sensor);
            app.demoEvents.push({
              date: sensor.timestamp.replace(/-/g, '/'),
              data: sensor,
              type: sensor.type,
              title: 'test',
              src: sensor.value,
              desc: sensor.timestamp
            });
        });
    }
  }).catch((error) => console.log("Error getting the data: "+error));
}
