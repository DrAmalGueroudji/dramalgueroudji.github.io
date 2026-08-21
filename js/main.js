/* Progressive enhancement only — every page is fully readable without JS. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- mobile nav toggle ---------- */
  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".nav-toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- scroll reveal with stagger ---------- */
  var revealables = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  // stagger siblings that share a parent
  var seen = new Map();
  revealables.forEach(function (el) {
    var p = el.parentElement;
    var n = seen.get(p) || 0;
    el.style.setProperty("--reveal-delay", Math.min(n * 0.08, 0.4) + "s");
    seen.set(p, n + 1);
  });

  if (!reduceMotion && "IntersectionObserver" in window) {
    var revealer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("revealed");
            revealer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    revealables.forEach(function (el) { revealer.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("revealed"); });
  }

  /* ---------- count-up stats ---------- */
  var counters = document.querySelectorAll(".count[data-count]");
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (!target || reduceMotion) { el.textContent = target; return; }
    var duration = 1200;
    var start = null;
    function step(ts) {
      if (start === null) start = ts;
      var t = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased);
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length && "IntersectionObserver" in window) {
    var counting = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            counting.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) { counting.observe(el); });
  }

  /* ---------- de-duplicate year labels inside each publication list ---------- */
  document.querySelectorAll(".pub-list").forEach(function (list) {
    if (list.closest(".invited-wrap")) return; // cards keep their year
    var lastYear = null;
    list.querySelectorAll(".pub").forEach(function (li) {
      var y = li.getAttribute("data-year");
      if (y && y === lastYear) li.classList.add("year-repeat");
      lastYear = y;
    });
  });
})();
