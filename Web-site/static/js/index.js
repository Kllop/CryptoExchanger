$(document).ready(function () {
  const path = window.location.pathname;
  if(path === '/') return;
  if(path === '/bid') {
    $("a[href='/my-bids']").addClass('nav-tab--selected');
    return
  }
  $(`a[href="${path}"]`).addClass('nav-tab--selected');
})