$("#submit").click(function(){
    const login = $("#login").val()
    const password = $("#password").val()
    console.log(login, password)
    LoginIn(login, password)
});

function LoginIn(login, password) {
    $.ajax({
      url: "/authorization",
      type: "post",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify({login : login, password : password}),
      success: function (response) {
        console.log(response)
      },
      error: function (xhr) {
        console.log("Error load offers")
      }
    });
  }