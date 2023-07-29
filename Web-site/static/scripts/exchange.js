
url = "http://127.0.0.1:5010"
url_data = "http://127.0.0.1:9000"

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
  CalculationExchangeRate()
})

$('#setter').on('change', function () {
  UpdateSetterOffers(this.value)
  CalculationExchangeRate()
})

$('#setter_value').on('change', function () {
  CalculationExchangeRate()
})

$('#getter_value').on('change', function () {
  CalculationCoinRate()
})

$("#send_buttom").on('click', function () {
  console.log("Send data")
  if(CheckAMLPolitic()){SenderOfferData()}
  else{alert("Примите AML политику")}
})

function CheckAMLPolitic(){
  return $("#AML_checkbox").is(":checked")
}

function SenderOfferData(){
  const method = "Buy"
  const setterValue = $("#setter_value").val()
  const getterValue = $("#getter_value").val()
  const setterType = $("#setter").val()
  const getterType = $("#getter").val()
  const setterNumber = $("#setter_number").val()
  const setterFullName = $("#setter_full_name").val()
  const setterEmail = $("#setter_email").val()
  const getterNumber = $("#getter_number").val()

  $.ajax({
    url: "/bid",
    type: "post",
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({
                          method : method, 
                          setterValue : setterValue, 
                          getterValue : getterValue,
                          setterType : setterType,
                          getterType : getterType,
                          setterNumber : setterNumber,
                          setterFullName : setterFullName,
                          setterEmail : setterEmail,
                          getterNumber : getterNumber
                        }),
    success: function (response) {
      console.log(response)
    },
    error: function (xhr) {
      console.log("Error load fiat data")
    }
  })
}

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

function CalculationExchangeRate(){
  var price = ChangeCourse()
  var value = $("#setter_value").val()
  $("#getter_value").val(Number((value/price).toFixed(5)))
}

function CalculationCoinRate(){
  var price = ChangeCourse()
  var value = $("#getter_value").val()
  $("#setter_value").val(Number((price * value).toFixed(0)))
}

function ChangeCourse(){
  getter_value = $('#getter').val()
  setter_value = $('#setter').val()
  var price = course_data[getter_value][setter_value]
  return price
}


function GetOffers(){
  $.ajax({
    url: `${url_data}/direction`,
    type: "get",
    success: function (response) {
      //const data = JSON.parse(response);
      offers_data = response
      UpdateGetterOffers()
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}

function UpdateCourse(){
$.ajax({
    url: `${url_data}/course`,
    type: "get",
    success: function (response) {
      //const data = JSON.parse(response);
      course_data = response
      CalculationExchangeRate()
    },
    error: function (xhr) {
      console.log("Error load course")
    }
  });
}

GetOffers()
UpdateCourse()

setInterval(UpdateCourse, 15000)