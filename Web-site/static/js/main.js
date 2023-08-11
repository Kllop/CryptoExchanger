import {updateSelectStyle} from "./utils/select.js";


var isDev = false
var url = isDev ? "https://jango-exchange.com" : "http://127.0.0.1:5010"
var url_data = isDev ? "https://jango-exchange.com" : "http://127.0.0.1:9000"

var offers_data = {}
var course_data = {}

function UpdateSetterOffers(setterName) {
  var values = offers_data[setterName]
  if (values == null) {
    return
  }
  $('#setter').empty();
  for (let unit of Object.keys(values)) {
    const option1 = $("<option>").attr('value', unit).text(values[unit]);
    $('#setter').append(option1);
  }
  var defaultValue = "Tinkoff"
  $('#setter').val(defaultValue)
  updateSelectStyle();
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

$("#form-send-bid-data").on('submit', function (event) {
  event.preventDefault();
  if (CheckAMLPolitic()) {
    SenderOfferData()
  } else {
    alert("Примите AML политику")
  }
})

function CheckAMLPolitic() {
  return $("#AML_checkbox").is(":checked")
}

function SenderOfferData() {
  const method = "Buy"
  const setterValue = $("#setter_value").val()
  const getterValue = $("#getter_value").val()
  const setterType = $("#setter").val()
  const getterType = $("#getter").val()
  const setterNumber = $("#setter_number").val()
  const setterTelegram = $("#setter_telegram").val()
  const getterNumber = $("#getter_number").val()

  $.ajax({
    url: "/bid",
    type: "post",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({
      method: method,
      setterValue: setterValue,
      getterValue: getterValue,
      setterType: setterType,
      getterType: getterType,
      setterNumber: setterNumber,
      setterTelegram: setterTelegram,
      getterNumber: getterNumber
    }),
    success: function (response) {
      window.location.href = '/bid'
    },
    error: function (xhr) {
      console.log("Error load fiat data", xhr)
    }
  })
}

function UpdateGetterOffers() {
  $('#getter').empty();
  for (let unit of Object.keys(offers_data)) {
    const option1 = $("<option>").attr('value', unit).text(unit);
    $('#getter').append(option1);
  }
  var defaultValue = "BTC"
  $('#getter').val(defaultValue)
  UpdateSetterOffers(defaultValue)
}

function CalculationExchangeRate() {
  var price = ChangeCourse()
  var value = $("#setter_value").val()
  $("#getter_value").val(Number((value / price).toFixed(5)))
}

function CalculationCoinRate() {
  var price = ChangeCourse()
  var value = $("#getter_value").val()
  $("#setter_value").val(Number((price * value).toFixed(0)))
}

function ChangeCourse() {
  var getter_value = $('#getter').val()
  var setter_value = $('#setter').val()
  var price = course_data[getter_value][setter_value]
  return price
}

function GetOffers() {
  $.ajax({
    url: "/direction",
    type: "get",
    success: function (response) {
      offers_data = response
      UpdateGetterOffers()
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}

function UpdateCourse() {
  const hash = window.location.hash;
  if (hash === '#/bid') return;

  $.ajax({
    url: "/course",
    type: "get",
    success: function (response) {
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
