// Entrada das seções, título que alterna e leve paralaxe das peças do topo. Sem dependências.
(function () {
  var calmo = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // entrada: se o observador falhar, tudo aparece do mesmo jeito
  var itens = document.querySelectorAll(".rv");
  var mostrarTudo = function () { itens.forEach(function (el) { el.classList.add("in"); }); };
  if (!("IntersectionObserver" in window) || calmo) {
    mostrarTudo();
  } else {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -6% 0px" });
    itens.forEach(function (el) { io.observe(el); });
    setTimeout(function () {
      itens.forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("in");
      });
    }, 1200);
  }

  // título que alterna
  var rot = document.getElementById("rot");
  if (rot && !calmo) {
    var falas = rot.querySelectorAll(".rot");
    var atual = 0;
    setInterval(function () {
      if (document.hidden) return;
      var sai = falas[atual];
      atual = (atual + 1) % falas.length;
      sai.classList.remove("on");
      sai.classList.add("off");
      falas[atual].classList.add("on");
      setTimeout(function () { sai.classList.remove("off"); }, 520);
    }, 2600);
  }

  // paralaxe: só com mouse
  var par = document.getElementById("par");
  if (par && !calmo && window.matchMedia("(hover: hover)").matches) {
    var hero = par.closest(".hero");
    hero.addEventListener("mousemove", function (e) {
      var r = hero.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      par.style.transform = "translate3d(" + (x * -22).toFixed(1) + "px," + (y * -16).toFixed(1) + "px,0)";
    });
    hero.addEventListener("mouseleave", function () { par.style.transform = ""; });
  }
})();
