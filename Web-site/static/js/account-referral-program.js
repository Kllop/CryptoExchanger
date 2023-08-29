$("li[data-referral-url]").on('click', function (event) {
  const url = event.target.dataset.referralUrl;
  if (url) getSubPage(url);
})

function getSubPage(url) {
  $.ajax({
    url: url,
    type: "post",
    success: function (response) {
      $('#account-referral-content').html(response);
    },
    error: function (xhr) {
      alert('Не удалось загрузить страницу')
    },
    complete: function () {
      $(`li[data-referral-url]`).removeClass("nav-list__item--active");
      $(`li[data-referral-url=${url}]`).attr("class", "nav-list__item nav-list__item--active");
    }
  });
}