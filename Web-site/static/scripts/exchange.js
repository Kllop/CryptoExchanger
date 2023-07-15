
url = "http://127.0.0.1:5010"

offers_data = {}
course_data = {}


function UpdateSetterOffers(setterName){
  values = offers_data[setterName]
  if(values == null){return}
  $('#setter').empty();
  for (let unit of values) {
    const option1 = $("<option>").attr('value', unit.key).text(unit.name);
    $('#setter').append(option1);
  }
  defaultValue = values[0].key
  $('#setter').val(defaultValue)
}

$('#getter').on('change', function () {
  UpdateSetterOffers(this.value)
})

function UpdateGetterOffers(){
    $('#getter').empty();
    defaultValue = "BTC"
    for (let unit of Object.keys(offers_data)) {
      const option1 = $("<option>").attr('value', unit).text(unit);
      $('#getter').append(option1);
    }
    $('#getter').val(defaultValue)
    UpdateSetterOffers(defaultValue)
}

function ChangeCourse(){
  getter_value = $('#getter').value
  setter_value = $('#setter').value
}


function GetOffers(){
  $.ajax({
    url: `${url}/offers`,
    type: "get",
    success: function (response) {
      const data = JSON.parse(response);
      offers_data = data
      UpdateGetterOffers()
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}

function UpdateCourse(){
$.ajax({
    url: `${url}/course`,
    type: "get",
    success: function (response) {
      const data = JSON.parse(response);
      course_data = data
    },
    error: function (xhr) {
      console.log("Error load course")
    }
  });
}

GetOffers()
setInterval(UpdateCourse, 15000)