// import {updateSelectStyle} from "./common/select.js";

var offers_data = {}
var course_data = {}
var commission = {}
var limmit = {}

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
  var defaultValue = Object.keys(values)[0]
  $('#setter').val(defaultValue)
  // updateSelectStyle();
}

function ChangeWalletName(){
  let coin_name = $("#getter").val()
  let names = {BTC : "Bitcoin", ETH : "Ethereum", USDT : "USDT(TRC20)"}
  let name = names[coin_name]
  let text = `${name} кошелёк*`
  $('#getter_number').attr("placeholder", text)
}

function ChangeNetworkCoin(){
  let coin_name = $("#getter").val()
  let names = {BTC : { BTC :"Bitcoin(BTC)"}, ETH : {ERC20 : "Ethereum(ERC20)"}, USDT : {TRC20 : "TRON(TRC20)"}}
  let name = names[coin_name]
  $('#coin_network').empty();
  for (let unit of Object.keys(name)) {
    const option1 = $("<option>").attr('value', unit).text(name[unit]);
    $('#coin_network').append(option1);
  }
  var defaultValue = Object.keys(name)[0]
  $('#coin_network').val(defaultValue)
}

$('#getter').on('change', function () {
  UpdateSetterOffers(this.value)
  ChangeWalletName()
  ChangeNetworkCoin()
  CalculationExchangeRate()
  updatePrewCourse()
})

$('#setter').on('change', function () {
  UpdateSetterOffers(this.value)
  ChangeWalletName()
  CalculationExchangeRate()
  updatePrewCourse()
})

$('#setter_value').on('change', function () {
  CalculationExchangeRate()
})

$('#getter_value').on('change', function () {
  CalculationCoinRate()
})

$('#commission').on('change', function () {
  CalculationExchangeRate()
})

$("#form-send-bid-data").on('submit', function (event) {
  event.preventDefault();
  if(!CheckLimmit()){alert("Не подходяшие лимиты");return}
  if (CheckAMLPolitic()) {
    SenderOfferData()
  } else {
    alert("Примите AML политику")
  }
})

function CheckAMLPolitic() {
  return $("#AML_checkbox").is(":checked")
}

function CheckLimmit(){
  var setterValue = $("#setter_value").val()
  return setterValue >= limmit['min'] && setterValue <= limmit['max']
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
  const setterEmail = $("#setter_email").val()

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
      getterNumber: getterNumber,
      setter_email: setterEmail,
    }),
    success: function (response) {
      window.location.href = '/bid'
    },
    error: function (xhr) {
      console.log("Error load fiat data", xhr)
    }
  })
}

function getCommission() {
  $.ajax({
      url: '/get_commission',
      type: "GET",
      dataType: "json",
      success: function (response) {
          commission = response
      },
      error: function (xhr) {
        console.log('Не удалось загрузить данные')
      }
    });
}

function getLimmit() {
  $.ajax({
      url: '/get_limmit',
      type: "GET",
      dataType: "json",
      success: function (response) {
          limmit = response
      },
      error: function (xhr) {
        console.log('Не удалось загрузить данные')
      }
    });
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

function ChangeCommission(){
  var coin = $("#getter").val()
  var select_commision = $("#commission").children(":selected").attr("id")
  var current_commision = parseInt(commission[coin][select_commision])
  if(coin == "BTC"){
    return 0.00000001 * 256 * current_commision
  }
  else if(coin == "ETH") {
    return 0.000000001 * 21000 * current_commision
  }
  else if(coin == "USDT") {
    return current_commision
  }
  return 0
}

function updatePrewCourse(){
  var price = ChangeCourse()
  var text = `Курс ≈ ${new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'RUB' }).format(price,)}` 
  $("#prew_course").text(text)
}

function CalculationExchangeRate() {
  var price = ChangeCourse()
  var value = parseFloat($("#setter_value").val())
  var commission = ChangeCommission()
  var count = Math.max((value / price) - commission, 0)
  $("#getter_value").val(Number((count).toFixed(5)))
}

function CalculationCoinRate() {
  var price = ChangeCourse()
  var commission = ChangeCommission()
  var value = commission + parseFloat($("#getter_value").val())
  console.log(value)
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
      setTimeout(UpdateCourse, 100)
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
      updatePrewCourse()
    },
    error: function (xhr) {
      console.log("Error load course")
    }
  });
}

GetOffers()
getCommission()
getLimmit()
setInterval(UpdateCourse, 15000)
