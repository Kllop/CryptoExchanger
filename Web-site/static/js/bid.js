$(document).on('click', '#btn-bid-accept', function (event) {
  alert("Заявка в обработке");
  event.target.parentElement.style.display = 'none';
});
$(document).on('click', '#btn-bid-cancel', function (event) {
  alert("Заявка отменена");
  window.location.replace("/");
});

function sendNewStatus(){
  $.ajax({
    url: "/status",
    type: "get",
    success: function (response) {
      offers_data = response
      UpdateGetterOffers()
    },
    error: function (xhr) {
      console.log("Error load offers")
    }
  });
}