$(document).on('click', '#admin_button', function (event) {
    const login = $("#admin_login").val()
    const password = $("#admin_password").val()
    send_login(login, password)
  });

function send_login(login, password) {
    $.ajax({
      url: "/admin",
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify({login : login, password : password}),
      success: function (response) {
        if(response.resualt == true){window.location.replace("/order_panel?status=new");}
        else{alert("Неправильный логин или пароль")}
      },
      error: function (xhr) {
        alert('Не удалось войти')
      }
    });
}

$(document).on('click', '#order_prev', function (event) {
    var tag = this.accessKey
    console.log(tag)
    window.location.replace("/order_detail?id=" + tag)
  });