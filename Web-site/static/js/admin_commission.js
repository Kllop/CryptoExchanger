var commission = {}

function sendCommission() {
    const min_com = $("#min_com").val();
    const middle_com = $("#middle_com").val();
    const max_com = $("#max_com").val();
  
    const commission = {min_com, middle_com, max_com}
    $.ajax({
      url: '/send_commission',
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(commission),
      success: function (response) {
      },
      error: function (xhr) {
        console.log('Не удалось загрузить данные')
      }
    });
}

function getCommission() {
    $.ajax({
        url: '/get_commission',
        type: "get",
        success: function (response) {
            commission = response.data
        },
        error: function (xhr) {
          console.log('Не удалось загрузить данные')
        }
      });
}

getCommission()
console.log(commission)