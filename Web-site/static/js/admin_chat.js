var chats_data = {}
var uuid = ""

url = true ? "wss://jango-exchange.com/admin_chat" : "ws://127.0.0.1:9020/admin_chat"
// url = "ws://127.0.0.1:9020/admin_chat"

let socketMarketGraph = new WebSocket(url);

socketMarketGraph.onopen = function(e) {
    
};

socketMarketGraph.onmessage = function(event) {
  chats_data = JSON.parse(event.data)
  construct_chats()
  if(uuid != ""){openChat(uuid)}
  play_sound()
};

function play_sound(){
  var beat = new Audio('static/mp3/signal.mp3');
  beat.play();
}

socketMarketGraph.onclose = function(event) {alert("Close market graph")};

function construct_chats(){
  $("#element_chats").empty()
  for (let unit of Object.keys(chats_data)) {
    data = chats_data[unit]
    messages = data['messages']
    lastmesage = messages.slice(-1)[0]
    createElementChats(unit, lastmesage['date'], lastmesage["message"].slice(0, 10) + "...")
  }
}

function createElementChats(uid, datetime, message){
  const [date, time] = datetime.split(' ');
  var $template = $("#chat_panel")
  var node = $template.prop('content');
  const element = $(node).find("#chat_element")
  var clone = element.clone()
  clone.find("#uuid_chat").text(uid)
  clone.find("#shortmessage").html(`
    <div style="display:flex; justify-content: space-between; width: 100%;">
        <div>${message}</div>    
        <div style="    display: flex;gap: 8px;align-items: center;">
          <div style="font-size: 13px">${time}</div>
          <div style="font-size: 11px">${date}</div>
        </div>    
    </div>`)
  clone.attr("accesskey", uid);
  $("#element_chats").append(clone);
}

function openChat(tag){
  $("#message_uuid").text("client chat uuid : " + tag)
  var chat = $("#messages")
  chat.empty();
  messages = chats_data[tag]["messages"]
  for(let message of messages){
    // message = $(`<div class="chat-messages-${message["owner"]}">`).text(message['date'] + " | " + message["owner"] + " | " + message["message"])
    message = $(`<div class="chat-message-${message["owner"]}">`).html(`
     <div class="chat-message-${message["owner"]}-wrapper">
      <div class="chat-message__text">${message['message']}</div>
      <div class="chat-message__date">
        <span>${message['date'].split(' ')[0]}</span>
        <span class="chat-message__date-time">${message['date'].split(' ')[1]}</span>
        </div>
    </div>
    `)
    chat.append(message)
  }
  uuid = tag
}

$(document).on('click', '#chat_element', function (event) {
  var tag = this.accessKey
  $("#text_message").val("")
  openChat(tag)
  $(`[accessKey]`).removeClass('chat-item--active');
  $(`[accessKey=${this.accessKey}]`).addClass('chat-item--active');
});

$(document).on('click', '#send_message', function (event) {
  sendMsg();
});

$("input#text_message").keydown(function(e){
  if (e.keyCode === 13 && !e.shiftKey)
  {
    e.preventDefault();
    sendMsg();
  }
});

function sendMsg() {
  var message = $("#text_message").val()
  $("#text_message").val("")
  socketMarketGraph.send(JSON.stringify({uuid : uuid, message : message}))
}

