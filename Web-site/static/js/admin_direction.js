

const url = "127.0.0.1:9020/all_direction"

function createDirection() {
  const coin = $("#f-coin").val();
  const pay_method = $("#f-pay_method").val();
  const bank_ru = $("#f-bank_ru").val();
  const bank_en = $("#f-bank_en").val();
  const bank_ind = $("#f-bank_ind").val();
  const percent = $("#f-percent").val();
  const area = $("#f-area").val();
  const market = $("#f-market").val();

  const payload = {coin, pay_method, bank_ru, bank_en, bank_ind, percent, area, market}
  console.log('pay', payload);
  $.ajax({
    url: '/create_direction',
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify(payload),
    success: function (response) {
      getAllDirections()
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });

}

function removeDirection(uid) {
  console.log(uid);
  $.ajax({
    url: '/remove_direction',
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify({uid}),
    success: function (response) {
      getAllDirections()
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
}

function getAllDirections() {
  $.ajax({
    url: '/all_direction',
    type: "get",
    success: function (response) {
      // console.log(response);
      renderDirectionList(response.data)
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
}

$( document ).ready(function() {
  getAllDirections();
});

function renderDirectionList(directions) {
  $("#direction-list").empty();

  directions.forEach(item => {
    $("#direction-list").append(
      `
        <div class="direction-item">
            <div>${item[1]}</div>
            <div>${item[2]}</div>
            <div>${item[3]}</div>
            <div>${item[4]}</div>
            <div>${item[5]}</div>
            <div>${item[6]}</div>
            <div>${item[7]}</div>
            <div>${item[8]}</div>
            <div>
                <button
                  class="danger"
                  onclick="removeDirection('${item[0]}')"
                >
                    Удалить
                </button>
            </div>
        </div>
      `)
  })
}