url = "http://127.0.0.1:5010"
url_data = "http://127.0.0.1:9000"

offers_data = {}
course_data = {}

function UpdateSetterOffers(setterName) {
  values = offers_data[setterName]
  if (values == null) {
    return
  }
  $('#setter').empty();
  for (let unit of Object.keys(values)) {
    const option1 = $("<option>").attr('value', unit).text(values[unit]);
    $('#setter').append(option1);
  }
  defaultValue = "Tinkoff"
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
    window.location.href = '#/bid';
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
      document.getElementById("main").innerHTML = response;
    },
    error: function (xhr) {
      console.log("Error load fiat data", xhr)
    }
  })
}

function UpdateGetterOffers() {
  $('#getter').empty();
  defaultValue = "BTC"
  for (let unit of Object.keys(offers_data)) {
    const option1 = $("<option>").attr('value', unit).text(unit);
    $('#getter').append(option1);
  }
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
  getter_value = $('#getter').val()
  setter_value = $('#setter').val()
  var price = course_data[getter_value][setter_value]
  return price
}


function GetOffers() {
  $.ajax({
    url: `${url_data}/direction`,
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
    url: `${url_data}/course`,
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
init()

setInterval(UpdateCourse, 15000)

window.addEventListener('hashchange', function() {
 route();
});

function route() {
  const hash = window.location.hash;
  if (hash === '#/bid') {
    SenderOfferData();
  }
}

function init() {
  route();
}

$(document).on('click', '#btn-bid-accept', function (event) {
  alert("Заявка в обработке");
  event.target.parentElement.style.display = 'none';
});
$(document).on('click', '#btn-bid-cancel', function (event) {
  alert("Заявка отменена");
  window.location.replace("/");
});

function updateSelectStyle() {
  $('select').each(function () {
    var $this = $(this), numberOfOptions = $(this).children('option').length;

    $this.addClass('select-hidden');
    $this.wrap('<div class="select"></div>');
    $this.after('<div class="select-styled"></div>');

    var $styledSelect = $this.next('div.select-styled');
    $styledSelect.text($this.children('option').eq(0).text());

    var $list = $('<ul />', {
      'class': 'select-options'
    }).insertAfter($styledSelect);

    for (var i = 0; i < numberOfOptions; i++) {
      $('<li />', {
        text: $this.children('option').eq(i).text(),
        rel: $this.children('option').eq(i).val()
      }).appendTo($list);
      if ($this.children('option').eq(i).is(':selected')) {
        $('li[rel="' + $this.children('option').eq(i).val() + '"]').addClass('is-selected')
      }
    }

    var $listItems = $list.children('li');

    $styledSelect.click(function (e) {
      e.stopPropagation();
      $('div.select-styled.active').not(this).each(function () {
        $(this).removeClass('active').next('ul.select-options').hide();
      });
      $(this).toggleClass('active').next('ul.select-options').toggle();
    });

    $listItems.click(function (e) {
      e.stopPropagation();
      $styledSelect.text($(this).text()).removeClass('active');
      $this.val($(this).attr('rel'));
      $list.find('li.is-selected').removeClass('is-selected');
      $list.find('li[rel="' + $(this).attr('rel') + '"]').addClass('is-selected');
      $list.hide();
    });

    $(document).click(function () {
      $styledSelect.removeClass('active');
      $list.hide();
    });
  });
}