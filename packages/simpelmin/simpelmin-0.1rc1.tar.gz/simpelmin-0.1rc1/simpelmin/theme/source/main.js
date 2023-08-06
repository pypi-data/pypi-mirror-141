import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js';
import './images';
// import Masonry from 'masonry-layout';
import './scss/main.scss';

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
});

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  let opts = {
    animation: true,
  }
  if (popoverTriggerEl.hasAttribute('data-bs-content-id')) {
    var content_id = popoverTriggerEl.getAttribute('data-bs-content-id')
    var content_el = document.getElementById(content_id)
    if (content_el != null) {
      opts.content = content_el.innerHTML;
    } else {
      opts.content = `content element with #${content_id} not found!`;
    }
    opts.html = true;
  }
  return new bootstrap.Popover(popoverTriggerEl, opts)
})

window.bootstrap = bootstrap;
