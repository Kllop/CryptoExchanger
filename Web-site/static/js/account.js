import {updateSelectStyle} from "./utils/select.js";

$("li[data-url]").on('click', function (event) {
  const url = event.target.dataset.url;
  if (url) getSubPage(url);
})

function getSubPage(url, idElementContainer = '#account-content') {
  $.ajax({
    url: url,
    type: "post",
    success: function (response) {
      $(idElementContainer).html(response);
      if (url === 'account-referral') updateSelectStyle();
    },
    error: function (xhr) {
      alert('Не удалось загрузить страницу')
    },
    complete: function () {
      $(`li[data-url]`).removeClass("nav-list__item--active");
      $(`li[data-url=${url}]`).attr("class", "nav-list__item nav-list__item--active");
    }
  });
}

updateSelectStyle()