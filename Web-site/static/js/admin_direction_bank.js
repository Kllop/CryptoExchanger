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

function saveChangeBankDirection(bank_ind){
  var element = $("#" + bank_ind)
  const bank_ru = element.find("#change_bank_ru").val();
  const bank_en = element.find("#change_bank_en").val();
  const bank_number = element.find("#change_bank_number").val();
  const bank_owner = element.find("#change_bank_owner").val();
  const payload = {bank_ind, bank_ru, bank_en, bank_number, bank_owner}
  console.log(payload)
  $.ajax({
    url: '/change_direction_banks',
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify(payload),
    success: function (response) {
      window.location.reload()
    },
    error: function (xhr) {
      console.log('Не удалось загрузить данные')
    }
  });
  
}

function changeBankDirection(ind) {
  var element = $("#" + ind)
  var text_ru = element.find("#name_ru").text()
  element.find("#name_ru").replaceWith(`<input id = "change_bank_ru" value = "${text_ru}">`)
  var text_en = element.find("#name_en").text()
  element.find("#name_en").replaceWith(`<input id = "change_bank_en" value = "${text_en}">`)
  var text_number = element.find("#number").text()
  element.find("#number").replaceWith(`<input id = "change_bank_number" value = "${text_number}">`)
  var text_owner = element.find("#owner").text()
  element.find("#owner").replaceWith(`<input id = "change_bank_owner" value = "${text_owner}">`)
  element.find("#change").replaceWith(`<button class="save" onclick="saveChangeBankDirection('${ind}')">C</button>`)
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
          <div class="direction-item" id = ${item["bank_ind"]}>
              <div>${item["bank_ind"]}</div>
              <div id = "name_ru">${item["bank_ru"]}</div>
              <div id = "name_en">${item["bank_en"]}</div>
              <div id = "number">${item["bank_number"]}</div>
              <div id = "owner">${item["bank_owner"]}</div>
              <div>
                  <button
                    class="change"
                    id = "change"
                    onclick="changeBankDirection('${item["bank_ind"]}')"
                  >
                      Р
                  </button>
                  <button
                    class="danger"
                    onclick="removeBankDirection('${item["bank_ind"]}')"
                  >
                      У
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