/* Walamort: progressive enhancement for responsive navigation. No tracking. */
(function(){
  "use strict";
  var toggle=document.querySelector(".wm-menu-toggle");
  var menu=document.getElementById("wm-nav-links");
  if(!toggle||!menu)return;
  function close(){menu.classList.remove("is-open");toggle.setAttribute("aria-expanded","false");toggle.setAttribute("aria-label","Abrir menú");}
  toggle.addEventListener("click",function(){var open=menu.classList.toggle("is-open");toggle.setAttribute("aria-expanded",String(open));toggle.setAttribute("aria-label",open?"Cerrar menú":"Abrir menú");});
  menu.addEventListener("click",function(event){if(event.target.closest("a"))close();});
  document.addEventListener("keydown",function(event){if(event.key==="Escape")close();});
  document.addEventListener("click",function(event){if(!menu.contains(event.target)&&!toggle.contains(event.target))close();});
  window.addEventListener("resize",function(){if(window.innerWidth>860)close();});
})();
