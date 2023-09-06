var chats_data = {}
var uuid = ""

let socketMarketGraph = new WebSocket("ws://jango-exchange.com/admin_chat");

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
    outmessage = lastmesage['date'] + " : "+ lastmesage["message"].slice(0, 10) + "..."
    createElementChats(unit, outmessage)
  }
}

function createElementChats(uid, message){
  var $template = $("#chat_panel")
  var node = $template.prop('content');
  const element = $(node).find("#chat_element")
  var clone = element.clone()
  clone.find("#uuid_chat").text(uid)
  clone.find("#shortmessage").text(message)
  clone.attr("accesskey", uid);
  $("#element_chats").append(clone);
}

function openChat(tag){
  $("#message_uuid").text("client chat uuid : " + tag)
  var chat = $("#messages")
  chat.empty();
  messages = chats_data[tag]["messages"]
  for(let message of messages){
    message = $('<div>').text(message['date'] + " | " + message["owner"] + " | " + message["message"])
    chat.append(message)
  }
  uuid = tag
}

$(document).on('click', '#chat_element', function (event) {
  var tag = this.accessKey
  console.log(tag)
  openChat(tag)
});

$(document).on('click', '#send_message', function (event) {
var message = $("#text_message").val()
$("#text_message").val("")
socketMarketGraph.send(JSON.stringify({uuid : uuid, message : message}))
});

