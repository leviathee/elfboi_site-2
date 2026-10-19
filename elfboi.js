/* ============================================================
   elfboi — behaviour
   1. Squiggle field (ambient, replaces the old circles)
   2. Tag filtering on the tool grid
   3. Side-nav scrollspy on tool pages
   4. Kit newsletter form
   ============================================================ */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. CURSOR PARALLAX -------------------------
     The drawings lean a little toward the cursor. Small enough
     that it registers as aliveness rather than as an effect.
     Set MAX to 0 to switch it off.
  ---------------------------------------------------------- */

  var PARALLAX_MAX = 5; // px

  function initParallax() {
    if (reduced || PARALLAX_MAX === 0) return;
    if (!window.matchMedia("(hover: hover)").matches) return;

    document.querySelectorAll(".tile").forEach(function (tile) {
      var art = tile.querySelector(".tile-art");
      if (!art) return;

      tile.addEventListener("mousemove", function (e) {
        var r = tile.getBoundingClientRect();
        var nx = (e.clientX - r.left) / r.width - 0.5;
        var ny = (e.clientY - r.top) / r.height - 0.5;
        art.style.transform = "translate(" + (nx * PARALLAX_MAX * 2).toFixed(2) + "px," +
                              (ny * PARALLAX_MAX * 2).toFixed(2) + "px)";
      });

      tile.addEventListener("mouseleave", function () {
        art.style.transform = "";
      });
    });
  }

  /* ---------- 1c. BACKDROP -------------------------------
     Waveforms drifting like clouds: sine, triangle, sawtooth and
     square, spread across the full height of the window, moving
     at different speeds. Run your pointer through one and it
     dissolves.

     BACKDROP: "waves" | "rain" | "none"
  ---------------------------------------------------------- */

  var BACKDROP = "waves";
  var WAVE_COLOURS = ["#4F7942", "#E3A347", "#C04334", "#33658A", "#7A51B1", "#197278"];
  var WAVE_MAX = 3;              // how many may be on screen at once
  var WAVE_GAP = [14000, 26000]; // ms between new ones
  var WAVE_SECONDS = [65, 110];  // how long one takes to cross
  var WAVE_BANDS = 5;            // vertical bands, so they never stack up

  var waveCount = 0;
  var lastBands = [];

  function pickBand() {
    // Choose a band that has not been used for the last couple of waves.
    var options = [];
    for (var i = 0; i < WAVE_BANDS; i++) {
      if (lastBands.indexOf(i) === -1) options.push(i);
    }
    if (!options.length) options = [0, 1, 2, 3, 4];
    var band = options[Math.floor(Math.random() * options.length)];
    lastBands.push(band);
    if (lastBands.length > 2) lastBands.shift();
    var slice = 92 / WAVE_BANDS;
    return 2 + band * slice + Math.random() * (slice * 0.55);
  }

  function wavePoints(kind, w, amp, cycles) {
    var steps = kind === "square" || kind === "saw" ? cycles * 4 : 72;
    var pts = [];
    for (var i = 0; i <= steps; i++) {
      var t = i / steps;
      var phase = t * cycles;
      var y;
      if (kind === "sine") {
        y = Math.sin(phase * Math.PI * 2);
      } else if (kind === "triangle") {
        var ft = phase % 1;
        y = ft < 0.5 ? -1 + ft * 4 : 3 - ft * 4;
      } else if (kind === "saw") {
        y = ((phase % 1) * 2) - 1;
      } else {
        y = (phase % 1) < 0.5 ? -1 : 1;
      }
      pts.push([t * w, 70 + y * amp]);
    }
    return pts;
  }

  function toPath(pts) {
    return pts.map(function (p, i) {
      return (i === 0 ? "M" : " L") + p[0].toFixed(1) + "," + p[1].toFixed(1);
    }).join("");
  }

  function makeWave() {
    var host = document.querySelector(".backdrop");
    if (!host || waveCount >= WAVE_MAX) return;

    var kinds = ["sine", "triangle", "saw", "square"];
    var kind = kinds[Math.floor(Math.random() * kinds.length)];
    var w = 300 + Math.random() * 300;   // narrower
    var amp = 8 + Math.random() * 14;    // shallower
    var cycles = 5 + Math.floor(Math.random() * 6); // tighter
    var colour = WAVE_COLOURS[Math.floor(Math.random() * WAVE_COLOURS.length)];

    var pts = wavePoints(kind, w, amp, cycles);
    var d = toPath(pts);

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "wave-drift");
    svg.setAttribute("width", w);
    svg.setAttribute("height", 140);
    svg.setAttribute("aria-hidden", "true");

    var line = document.createElementNS("http://www.w3.org/2000/svg", "path");
    line.setAttribute("d", d);
    line.setAttribute("stroke", colour);
    line.setAttribute("class", "wave-line");

    var hit = document.createElementNS("http://www.w3.org/2000/svg", "path");
    hit.setAttribute("d", d);
    hit.setAttribute("class", "wave-hit");

    svg.appendChild(line);
    svg.appendChild(hit);

    svg.style.top = pickBand() + "%";
    var dur = WAVE_SECONDS[0] + Math.random() * (WAVE_SECONDS[1] - WAVE_SECONDS[0]);
    svg.style.animationDuration = dur + "s";
    if (Math.random() < 0.45) svg.style.animationName = "cross-back";

    var gone = false;

    function scatter() {
      // Break the line into bits that drift off in their own directions,
      // the way a cloud comes apart rather than a light being switched off.
      var every = Math.max(1, Math.floor(pts.length / 14));
      for (var i = 0; i < pts.length; i += every) {
        var bit = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        bit.setAttribute("class", "wave-bit");
        bit.setAttribute("cx", pts[i][0]);
        bit.setAttribute("cy", pts[i][1]);
        bit.setAttribute("r", (0.8 + Math.random() * 1.2).toFixed(1));
        bit.setAttribute("fill", colour);
        var ang = Math.random() * Math.PI * 2;
        var dist = 12 + Math.random() * 30;
        bit.style.setProperty("--dx", (Math.cos(ang) * dist).toFixed(1) + "px");
        bit.style.setProperty("--dy", (Math.sin(ang) * dist - 8).toFixed(1) + "px");
        bit.style.animationDelay = (Math.random() * 0.28).toFixed(2) + "s";
        bit.style.animationDuration = (1.1 + Math.random() * 0.9).toFixed(2) + "s";
        svg.appendChild(bit);
      }
    }

    function dissolve(withBits) {
      if (gone) return;
      gone = true;
      if (withBits) scatter();
      svg.classList.add("is-gone");
      setTimeout(function () {
        svg.remove();
        waveCount--;
      }, 2200);
    }

    hit.addEventListener("mouseenter", function () { dissolve(true); });
    hit.addEventListener("touchstart", function () { dissolve(true); }, { passive: true });

    host.appendChild(svg);
    waveCount++;
    setTimeout(function () { dissolve(false); }, dur * 1000);
  }

  function initBackdrop() {
    if (BACKDROP === "none") return;

    if (BACKDROP === "rain") {
      document.documentElement.setAttribute("data-backdrop", "rain");
      return;
    }

    var host = document.createElement("div");
    host.className = "backdrop";
    host.setAttribute("aria-hidden", "true");
    document.body.appendChild(host);

    if (reduced) return;

    for (var i = 0; i < 2; i++) setTimeout(makeWave, i * 7000);
    (function loop() {
      var wait = WAVE_GAP[0] + Math.random() * (WAVE_GAP[1] - WAVE_GAP[0]);
      setTimeout(function () { makeWave(); loop(); }, wait);
    })();
  }

  /* ---------- 2. TAG FILTERING ----------------------------- */

  function initFilters() {
    var buttons = document.querySelectorAll(".filter");
    var tiles = document.querySelectorAll(".tile");
    if (!buttons.length || !tiles.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var want = btn.dataset.filter;

        buttons.forEach(function (b) {
          b.setAttribute("aria-pressed", String(b === btn));
        });

        tiles.forEach(function (tile) {
          var tags = (tile.dataset.tags || "").split(" ");
          tile.hidden = !(want === "all" || tags.indexOf(want) !== -1);
        });
      });
    });
  }

  /* ---------- 3. SIDE-NAV SCROLLSPY ------------------------ */

  function initSidenav() {
    var links = document.querySelectorAll(".sidenav a");
    if (!links.length) return;

    var map = {};
    var targets = [];

    links.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      if (el) { map[id] = link; targets.push(el); }
    });

    if (!("IntersectionObserver" in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          links.forEach(function (l) { l.classList.remove("is-active"); });
          var active = map[entry.target.id];
          if (active) active.classList.add("is-active");
        }
      });
    }, { rootMargin: "-12% 0px -70% 0px", threshold: 0 });

    targets.forEach(function (t) { observer.observe(t); });
  }

  /* ---------- 4. NEWSLETTER (Kit) ------------------------
     The number below is a Kit FORM ID. It is public by design and
     safe to sit in this file.

     Never put an API key here. A v4 key (kit_xxxxxxxx) is a
     server-side secret, and anything in this file is readable by
     every visitor: it would let anyone read, export, and delete
     the whole subscriber list.

     Submitting happens in the background, so nobody is bounced to
     a Kit page. Set KIT_FORM_ID to "" to switch the forms off.
  ---------------------------------------------------------- */

  var KIT_FORM_ID = "9845746";

  function initSignup() {
    var forms = document.querySelectorAll(".signup-form");
    if (!forms.length) return;

    forms.forEach(function (form) {
      var input = form.querySelector("input[type=email]");
      var button = form.querySelector("button");
      var note = form.parentElement.querySelector(".signup-note, .note-foot");
      var original = note ? note.innerHTML : "";

      function say(text, bad) {
        if (!note) return;
        note.textContent = text;
        note.style.color = bad ? "#C04334" : "var(--accent-deep)";
      }

      form.addEventListener("submit", function (e) {
        e.preventDefault();

        if (!input || !input.value || input.value.indexOf("@") === -1) {
          say("That address does not look right.", true);
          return;
        }

        if (!KIT_FORM_ID) {
          say("Add your Kit form ID in elfboi.js to make this live.", true);
          return;
        }

        button.disabled = true;
        var label = button.textContent;
        button.textContent = "sending";

        var body = new FormData();
        body.append("email_address", input.value);

        fetch("https://app.kit.com/forms/" + KIT_FORM_ID + "/subscriptions", {
          method: "POST",
          body: body,
          headers: { Accept: "application/json" }
        })
          .then(function (r) { return r.json(); })
          .then(function () {
            form.style.display = "none";
            say("Thank you. Check your inbox to confirm.");
          })
          .catch(function () {
            say("Something went wrong. Write to hello@elfboi.io instead.", true);
            if (note) setTimeout(function () { note.innerHTML = original; note.style.color = ""; }, 6000);
          })
          .finally(function () {
            button.disabled = false;
            button.textContent = label;
          });
      });
    });
  }


  /* ---------- BEFORE AND AFTER PLAYERS ---------------------
     One <audio> per clip, built on first press so nothing is
     fetched until somebody asks for it. Starting one stops any
     other, because the point is to compare them, not to hear
     two at once.
     --------------------------------------------------------- */

  function initPlayers() {
    var clips = [].slice.call(document.querySelectorAll(".clip[data-src]"));
    if (!clips.length) return;

    var playing = null;

    function fmt(t) {
      if (!isFinite(t)) return "0:00";
      var m = Math.floor(t / 60), s = Math.floor(t % 60);
      return m + ":" + (s < 10 ? "0" : "") + s;
    }

    clips.forEach(function (clip) {
      var btn = clip.querySelector(".clip-play");
      var bar = clip.querySelector(".clip-bar");
      var fill = clip.querySelector(".clip-fill");
      var time = clip.querySelector(".clip-time");
      var audio = null;
      var raf = 0;

      function paint() {
        if (!audio || !audio.duration) return;
        fill.style.width = (100 * audio.currentTime / audio.duration) + "%";
        time.textContent = fmt(audio.duration - audio.currentTime);
        if (!audio.paused) raf = requestAnimationFrame(paint);
      }

      function build() {
        audio = new Audio();
        audio.preload = "none";
        audio.src = clip.getAttribute("data-src");
        audio.addEventListener("loadedmetadata", function () {
          clip.classList.remove("is-loading");
          time.textContent = fmt(audio.duration);
        });
        audio.addEventListener("ended", function () {
          clip.classList.remove("is-playing");
          fill.style.width = "0%";
          time.textContent = fmt(audio.duration);
          playing = null;
        });
        audio.addEventListener("error", function () {
          clip.classList.remove("is-loading", "is-playing");
          time.textContent = "unavailable";
        });
      }

      btn.addEventListener("click", function () {
        if (!audio) { build(); clip.classList.add("is-loading"); }

        if (!audio.paused) {
          audio.pause();
          clip.classList.remove("is-playing");
          cancelAnimationFrame(raf);
          playing = null;
          return;
        }

        if (playing && playing !== stop) playing();
        audio.play().then(function () {
          clip.classList.remove("is-loading");
          clip.classList.add("is-playing");
          playing = stop;
          paint();
        }).catch(function () {
          clip.classList.remove("is-loading");
          time.textContent = "unavailable";
        });
      });

      function stop() {
        if (audio && !audio.paused) audio.pause();
        clip.classList.remove("is-playing");
        cancelAnimationFrame(raf);
      }

      bar.addEventListener("click", function (e) {
        if (!audio || !audio.duration) return;
        var r = bar.getBoundingClientRect();
        audio.currentTime = audio.duration * Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
        paint();
      });
    });
  }


  /* ---------- SCREENSHOT GALLERY ---------------------------
     One slide visible, the rest kept in the document so the
     count is honest and the browser can cache them. Arrow keys
     work when the gallery has focus, and a drag moves it on a
     touch screen.
     --------------------------------------------------------- */

  function initGallery() {
    [].forEach.call(document.querySelectorAll(".shotbox"), function (box) {
      var slides = [].slice.call(box.querySelectorAll(".shot-slide"));
      if (slides.length < 2) { if (slides[0]) slides[0].classList.add("is-current"); return; }

      var count = box.querySelector(".shotbox-count b");
      var at = 0;

      function show(n) {
        at = (n + slides.length) % slides.length;
        slides.forEach(function (s, i) { s.classList.toggle("is-current", i === at); });
        if (count) count.textContent = (at + 1 < 10 ? "0" : "") + (at + 1);
      }
      show(0);

      [].forEach.call(box.querySelectorAll(".shotbox-arrow"), function (btn) {
        btn.addEventListener("click", function () {
          show(at + parseInt(btn.getAttribute("data-dir"), 10));
        });
      });

      box.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { show(at - 1); e.preventDefault(); }
        if (e.key === "ArrowRight") { show(at + 1); e.preventDefault(); }
      });

      var x0 = null;
      var stage = box.querySelector(".shotbox-stage");
      stage.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      stage.addEventListener("touchend", function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 40) show(at + (dx < 0 ? 1 : -1));
        x0 = null;
      }, { passive: true });
    });
  }

  /* ---------- BOOT ----------------------------------------- */

  function boot() {
    initBackdrop();
    initParallax();
    initFilters();
    initSidenav();
    initSignup();
    initPlayers();
    initGallery();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();


