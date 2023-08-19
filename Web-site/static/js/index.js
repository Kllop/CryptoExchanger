const IS_LOGIN_FLAG = 'isLogin';

function assignActiveTab() {
  const path = window.location.pathname;
  if(path === '/') return;
  if(path === '/bid') {
    $("a[href='/my-bids']").addClass('nav-tab--selected');
    return
  }
  $(`a[href="${path}"]`).addClass('nav-tab--selected');
}

function hideNavByIsLogin() {
  const isLogin = JSON.parse(localStorage.getItem(IS_LOGIN_FLAG));
  if(isLogin) {
    $("#header-link-login").hide();
    $("#header-link-reg").hide();
    $("#header-link-exit").show();
  } else {
    $("#header-link-login").show();
    $("#header-link-reg").show();
    $("#header-link-exit").hide();
  }
}
function hideModal(modalElem) {
  const backdrop = document.querySelector('#modal-backdrop');
  modalElem.classList.remove('show');
  backdrop.classList.add('hidden');
  document.getElementsByTagName('body')[0].style.overflow = 'auto';
  hideNavByIsLogin()
}

$(document).ready(function () {
  assignActiveTab();
  hideNavByIsLogin();
  $("#header-link-exit").click(function () {
    localStorage.removeItem(IS_LOGIN_FLAG);
    window.location.reload();
  })
})

$("#submitLog").on("submit", function(event){
  event.preventDefault()
  const login = $("#log-login").val()
  const password = $("#log-password").val()
  LoginIn(login, password)
});

$("#submitReg").on("submit", function(event){
  event.preventDefault()
  const login = $("#reg-login").val()
  const password = $("#reg-password").val()
  const email = $("#reg-email").val()
  Registration(login, password, email)
});

function Registration(login, password, email) {
  $.ajax({
    url: "/registration",
    type: "post",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify({login : login, password : password, email : email}),
    success: function (response) {
      if(response['resualt'] == false){alert(response['message']); return}
      localStorage.setItem(IS_LOGIN_FLAG, 'true')
      hideNavByIsLogin();
    },
    error: function (xhr) {
      alert('Не удалось зарегистрироваться')
    },
    complete: function () {
      hideModal(document.getElementById('modal-registration'))
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
      if(response['resualt'] == false){alert("Логин и пароль неверный"); return}
      localStorage.setItem(IS_LOGIN_FLAG, 'true')
      hideNavByIsLogin();
    },
    error: function (xhr) {
      alert('Не удалось авторизоваться')
      console.log("Error load offers")
    },
    complete: function () {
      hideModal(document.getElementById('modal-login'))
    }
  });
}