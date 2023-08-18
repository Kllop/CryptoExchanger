$("#submitLog").on("submit", function(event){
    event.preventDefault()
    const login = $("#log-login").val()
    const password = $("#log-password").val()
    console.log(login, password)
    LoginIn(login, password)
});

$("#submitReg").on("submit", function(event){
  event.preventDefault()
  const login = $("#reg-login").val()
  const password = $("#reg-password").val()
  const email = $("#reg-email").val()
  console.log(login, password, email)
  Registration(login, password, email)
});

function Registration(login, password, email) {
  $.ajax({
    url: "/registration",
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify({login : login, password : password, email : email}),
    success: function (response) {
      console.log(response)
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}

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