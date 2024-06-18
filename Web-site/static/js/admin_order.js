  $(document).on('click', '#release_order', function (event) {
    var tag = this.accessKey
    $.ajax({
      url: "/release_order",
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify({key : tag}),
      success: function (response) {
        if(response.resualt == true){window.location.reload()}
      },
      error: function (xhr) {
        alert('Не удалось войти')
      }
    });
  });

  $(document).on('click', '#cancel_order', function (event) {
    var tag = this.accessKey
    $.ajax({
      url: "/cancel_order",
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify({key : tag}),
      success: function (response) {
        if(response.resualt == true){window.location.reload()}
      },
      error: function (xhr) {
        alert('Не удалось войти')
      }
    });
  });

function checkStatus(){
  var status = $("#status").text()
  if(status == "payment"){
    document.getElementById('release_order').style.visibility = 'hidden';
  }
  if(status == "cancel"){
    document.getElementById('cancel_order').style.visibility = 'hidden';
  }
}

checkStatus()