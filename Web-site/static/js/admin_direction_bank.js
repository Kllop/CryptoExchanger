function createDirection() {
  const bank_ind = $("#bank_ind").val();
  const bank_ru = $("#bank_ru").val();
  const bank_en = $("#bank_en").val();
  const bank_number = $("#bank_number").val();
  const bank_owner = $("#bank_owner").val();


  const payload = {bank_ind, bank_ru, bank_en, bank_number, bank_owner}
  console.log('pay', payload);
  $.ajax({
    url: '/create_direction_banks',
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify(payload),
    success: function (response) {
      getAllBankDirections()
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
}

function removeBankDirection(uid) {
  $.ajax({
    url: '/remove_direction_banks',
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify({uid}),
    success: function (response) {
      getAllBankDirections()
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
}

function getAllBankDirections() {
  $.ajax({
    url: '/all_direction_banks',
    type: "get",
    success: function (response) {
      renderDirectionBankList(response.data)
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
}

function renderDirectionBankList(directions) {
    $("#direction-list").empty();
  
    for (let item of Object.values(directions)) {
      console.log(item)
      $("#direction-list").append(
        `
          <div class="direction-item">
              <div>${item["bank_ind"]}</div>
              <div>${item["bank_ru"]}</div>
              <div>${item["bank_en"]}</div>
              <div>${item["bank_number"]}</div>
              <div>${item["bank_owner"]}</div>
              <div>
                  <button
                    class="danger"
                    onclick="removeBankDirection('${item["bank_ind"]}')"
                  >
                      Удалить
                  </button>
              </div>
          </div>
        `)
    }
  }

  $( document ).ready(function() {
    getAllBankDirections();
  });

renderDirectionBankList([['Hello1', 'Hello2', 'Hello3', 'Hello4', 'Hello5', 'Hello6']])