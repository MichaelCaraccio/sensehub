// VueJS
var app = new Vue({
  el: '#form-container',
  delimiters: ['[[', ']]'],
  data: function(){
      return {
        state : "form", // sent, received
        key:"",
        id:"",
    };
  },
  methods: {
      setCurrent: function(index){

      }
  }
});



// Listener

var form = document.getElementById("needs-validation");
form.addEventListener("submit", function(event) {

  if (form.checkValidity() == false) {
    event.preventDefault();
    event.stopPropagation();
  }
  form.classList.add("was-validated");

  if (form.checkValidity() == true)
  {
    event.preventDefault();

    var data = {};
    data["name"] = form.elements.name.value;
    data["hardware_type"] = form.elements.hardware_type.value;
    data["public"]= form.elements.public.checked;
    data["type"]= form.elements.type.value;
    app.state='sent';
    $.ajax({
      type: 'PUT', // Use POST with X-HTTP-Method-Override or a straight PUT if appropriate.
      contentType: 'application/json', // Set datatype - affects Accept header
      url: "/api/sensor/add/", // A valid URL
      data: JSON.stringify(data) // Some data e.g. Valid JSON as a string
    }).done(function(data) {
      if (data.status === "ok") {
        var response = data.message;
        app.key = response.key;
        app.id = response.sensor_id;
        app.state = 'received';
      }
      else {
        app.state='form';
      }
    });
  }
}, false);
