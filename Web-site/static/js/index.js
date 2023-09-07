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
    $("#header-link-lc").show();
    $("#header-link-exit").show();
  } else {
    $("#header-link-login").show();
    $("#header-link-reg").show();
    $("#header-link-lc").hide();
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
    LogOut()
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

function LogOut(login, password, email) {
  $.ajax({
    url: "/logout",
    type: "get",
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify({login : login, password : password, email : email}),
    success: function (response) {
    },
    error: function (xhr) {
      alert('Не удалось выйти')
    },
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




$('#prime').click(function() {
  toggleFab();
});

//Toggle chat and links
function toggleFab() {
  $('.prime').toggleClass('zmdi-comment-outline');
  $('.prime').toggleClass('zmdi-close');
  $('.prime').toggleClass('is-active');
  $('.prime').toggleClass('is-visible');
  $('#prime').toggleClass('is-float');
  $('.chat').toggleClass('is-visible');
  $('.fab').toggleClass('is-visible');
  
}

function hideChat() {
  $('#chat_converse').css('display', 'none');
  $('#chat_body').css('display', 'none');
  $('#chat_form').css('display', 'none');
  $('.chat_login').css('display', 'none');
  $('.chat_fullscreen_loader').css('display', 'block');
  $('#chat_fullscreen').css('display', 'block');
}

function createElementChatsAdmin(message){
  var $template = $("#chat_panel")
  var node = $template.prop('content');
  const element = $(node).find("#admin_item")
  var clone = element.clone()
  clone.find("#element_message_admin").text(message)
  $("#chat_fullscreen").append(clone);
}

function createElementChatsClient(message){
  var $template = $("#chat_panel")
  var node = $template.prop('content');
  const element = $(node).find("#client_item")
  var clone = element.clone()
  clone.text(message)
  $("#chat_fullscreen").append(clone);
}

$(document).on('click', '#fab_send', function (event) {
  message = $("#chatSend").val()
  $("#chatSend").val("")
  socketMarketGraph.send(message)
});

url = true ? "wss://jango-exchange.com/chat" : "ws://127.0.0.1:9020/chat"

let socketMarketGraph = new WebSocket(url);

socketMarketGraph.onmessage = function(event) {
  chat_data = JSON.parse(event.data)
  construct_chats();
};

function setCookieUUID(uuid){
  var expDate = new Date();
  expDate.setTime(expDate.getTime() + (180 * 1440 * 60 * 1000));
  $.cookie("uuid_chat", uuid, {path: '/', expires: expDate})
}

function construct_chats(){
  $("#chat_fullscreen").empty()
  messages = chat_data['messages']
  setCookieUUID(chat_data["uuid_chat"])
  for (let unit of messages) {
    if(unit["owner"] == "Client"){createElementChatsClient(unit["message"])}
    else{createElementChatsAdmin(unit["message"])}
  }
}

var chat_data = {}

hideChat();
