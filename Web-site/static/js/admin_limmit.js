function sendLimmit() {
    const min_lim = $("#min_lim").val();
    const max_lim = $("#max_lim").val();
  
    const limmit = {min_lim, max_lim}
    $.ajax({
      url: '/send_limmit',
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(limmit),
      success: function (response) {
      },
      error: function (xhr) {
        console.log('Не удалось загрузить данные')
      }
    });
}
