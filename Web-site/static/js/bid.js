$(document).on('click', '#btn-bid-accept', function (event) {
  alert("Заявка в обработке");
  sendNewStatus("payment")
  event.target.parentElement.style.display = 'none';
});
$(document).on('click', '#btn-bid-cancel', function (event) {
  alert("Заявка отменена");
  sendNewStatus("cancel")
  window.location.replace("/");
});

function sendNewStatus(status){
  $.ajax({
    url: "/status",
    type: "get",
    data : {status : status},
    success: function (response) {
      offers_data = response
      UpdateGetterOffers()
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}