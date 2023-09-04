var chats_data = {}

let socketMarketGraph = new WebSocket("ws://127.0.0.1:9020/admin_chat");

socketMarketGraph.onopen = function(e) {
    
};

socketMarketGraph.onmessage = function(event) {
  data = JSON.parse(event.data)
};

socketMarketGraph.onclose = function(event) {alert("Close market graph")};

function createElementChats(uid, message){
    var tbody = document.querySelector("#place_chats")
    var tableElement = document.querySelector("#chat_panel");
    var clone = tableElement.content.cloneNode(true);
    clone.accessKey = uid;
    var uuid = clone.getElementById("uuid_chat");
    var short_message = clone.getElementById("shortmessage");
    uuid.textContent = uid;
    short_message.textContent = message;
      
    tbody.appendChild(clone)
}

createElementChats("Hello", "123")

$(document).on('click', '#chat_element', function (event) {
    var tag = this.accessKey
    console.log(tag)
  });