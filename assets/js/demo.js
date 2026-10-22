/*!
 * Swift Laundry Services website
 * Designed & developed by Innocent Christo
 * © 2026 Innocent Christo. All rights reserved.
 */
/* Swift Laundry demo: multi-step pickup form, ZIP checker, contact form, FAQ search.
   No backend yet: forms open the visitor's email app (forms.email in site-config.js),
   or POST to forms.endpoint when one is configured. */
(function () {
  "use strict";
  var CFG = window.SWIFT_CONFIG || {}, B = CFG.business || {}, F = CFG.forms || {};
  var doc = document;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var scrollTo = function (el) { if (window.__lenis) window.__lenis.scrollTo(el, { offset: -110 }); else el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); };
  var tel = '<a href="tel:' + (B.phoneE164 || "+17144027530") + '">' + (B.phoneDisplay || "(714) 402-7530") + "</a>";
  var sms = '<a href="sms:' + (B.phoneE164 || "+17144027530") + '">text</a>';

  /* ---------- field validation ---------- */
  var msgFor = function (el) {
    var v = el.validity;
    if (el.type === "checkbox" && !el.checked && el.required) return "Please tick this box to continue.";
    if (v.valueMissing) return "This field is required.";
    if (v.typeMismatch && el.type === "email") return "Please enter a valid email address.";
    if (v.patternMismatch || v.customError) return el.getAttribute("data-msg-pattern") || "Please check the format.";
    if (v.rangeUnderflow) return "Please choose today or a later date.";
    return "";
  };
  var setErr = function (el, msg) {
    var wrap = el.closest(".field"); if (!wrap) return;
    wrap.classList.toggle("has-error", !!msg);
    if (msg) el.setAttribute("aria-invalid", "true"); else el.removeAttribute("aria-invalid");
    var out = $(".field-error", wrap); if (out) out.textContent = msg;
  };
  var check = function (el) {
    if (el.hasAttribute("data-phone-or-email")) {
      var val = el.value.trim();
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) || /^[0-9()+.\- ]{7,}$/.test(val);
      el.setCustomValidity(val && !ok ? "bad" : "");
    }
    var m = el.checkValidity() ? "" : msgFor(el);
    setErr(el, m); return !m;
  };
  var validateIn = function (root) {
    var bad = null;
    $$("input, select, textarea", root).forEach(function (el) {
      if (el.type === "radio" || (el.type === "checkbox" && !el.required)) return;
      if (!check(el) && !bad) bad = el;
    });
    if (bad) bad.focus();
    return !bad;
  };
  $$("form[data-pickup], form[data-contact]").forEach(function (f) {
    $$("input, select, textarea", f).forEach(function (el) {
      el.addEventListener(el.type === "checkbox" ? "change" : "blur", function () { if (el.closest(".has-error")) check(el); });
    });
  });

  var labelOf = function (el) {
    var w = el.closest("[data-summary-label]"); if (w) return w.getAttribute("data-summary-label");
    var l = el.id && $('label[for="' + el.id + '"]'); return l ? l.textContent.replace(/\(optional\)/i, "").trim() : el.name;
  };
  var collect = function (form) {
    var rows = [], seen = {};
    $$("input, select, textarea", form).forEach(function (el) {
      if (el.name === "p-ack") return;
      var grp = el.closest("[data-summary-group]");
      var key = grp ? grp.getAttribute("data-summary-label") : labelOf(el);
      var val;
      if (el.type === "radio" || el.type === "checkbox") { if (!el.checked) return; val = el.getAttribute("data-label") || el.value; }
      else { val = el.tagName === "SELECT" ? (el.value ? el.options[el.selectedIndex].text : "") : el.value.trim(); }
      if (!val) return;
      if (seen[key] != null) rows[seen[key]][1] += ", " + val; else { seen[key] = rows.length; rows.push([key, val]); }
    });
    return rows;
  };
  var send = function (form, rows, ok, fail) {
    var subject = form.getAttribute("data-subject") || "Website request";
    var btn = $("[data-submit]", form), failBox = $("[data-fail]", form);
    if (failBox) failBox.hidden = true;
    if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending request…"; }
    var done = function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } };
    if (F.endpoint) {
      var fd = new FormData(form); fd.append("_subject", subject);
      fetch(F.endpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); done(); ok("endpoint"); })
        .catch(function () { done(); if (failBox) { failBox.hidden = false; scrollTo(failBox); } if (fail) fail(); });
      return;
    }
    if (F.email) {
      var body = subject + "\n\n" + rows.map(function (r) { return r[0] + ": " + r[1]; }).join("\n");
      window.location.href = "mailto:" + F.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      setTimeout(function () { done(); ok("mail"); }, 400);
      return;
    }
    done(); if (failBox) { failBox.hidden = false; scrollTo(failBox); }
  };

  /* ---------- Schedule a Pickup: 3 steps ---------- */
  var pf = $("form[data-pickup]");
  if (pf) {
    var panels = $$("[data-step]", pf), dots = $$("[data-stepper] li"), at = 0;
    var show = function (i) {
      at = i;
      panels.forEach(function (p, k) { p.hidden = k !== i; });
      dots.forEach(function (d, k) { d.classList.toggle("is-current", k === i); d.classList.toggle("is-done", k < i); if (k === i) d.setAttribute("aria-current", "step"); else d.removeAttribute("aria-current"); });
      if (i === 2) {
        var dl = $("[data-review]", pf);
        dl.innerHTML = "";
        collect(pf).forEach(function (r) { var dt = doc.createElement("dt"), dd = doc.createElement("dd"); dt.textContent = r[0]; dd.textContent = r[1]; dl.appendChild(dt); dl.appendChild(dd); });
      }
      scrollTo($("[data-stepper]"));
      var h = $(".step-head", panels[i]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
    };
    $$("[data-next]", pf).forEach(function (b) { b.addEventListener("click", function () { if (validateIn(panels[at])) show(at + 1); }); });
    $$("[data-back]", pf).forEach(function (b) { b.addEventListener("click", function () { show(at - 1); }); });
    pf.addEventListener("keydown", function (e) { if (e.key === "Enter" && e.target.tagName === "INPUT" && at < 2) { e.preventDefault(); var n = $("[data-next]", panels[at]); if (n) n.click(); } });
    pf.addEventListener("submit", function (e) {
      e.preventDefault();
      if (at !== 2) return;
      if (!validateIn(panels[2])) return;
      var rows = collect(pf);
      send(pf, rows, function (how) {
        /* Summary is kept in this tab only (sessionStorage), never in the URL. */
        try { sessionStorage.setItem("swiftRequest", JSON.stringify({ how: how, rows: rows.filter(function (r) { return !/address|mobile|email|instructions/i.test(r[0]); }) })); } catch (x) {}
        window.location.href = "request-received.html";
      });
    });
  }

  /* ---------- Request received ---------- */
  var rr = $("[data-rr-summary]");
  if (rr) {
    var data = null; try { data = JSON.parse(sessionStorage.getItem("swiftRequest") || "null"); } catch (x) {}
    if (data && data.rows && data.rows.length) {
      var dl2 = $("[data-rr-list]");
      data.rows.forEach(function (r) { var dt = doc.createElement("dt"), dd = doc.createElement("dd"); dt.textContent = r[0]; dd.textContent = r[1]; dl2.appendChild(dt); dl2.appendChild(dd); });
      rr.hidden = false;
    }
    if (data && data.how === "mail") $("[data-rr-mail]").hidden = false;
  }

  /* ---------- Contact form ---------- */
  var cf = $("form[data-contact]");
  if (cf) cf.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validateIn(cf)) return;
    send(cf, collect(cf), function () { var ok = $("[data-contact-ok]", cf); ok.hidden = false; ok.focus({ preventScroll: true }); scrollTo(ok); });
  });

  /* ---------- ZIP checker: never claims coverage without the owner's list ---------- */
  var ZIPS = (CFG.zips || []).map(String);
  $$("form[data-zip]").forEach(function (f) {
    var input = $("input", f), out = $(".zip-out", f);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var z = input.value.trim();
      f.classList.remove("is-yes", "is-no", "is-bad", "is-manual");
      if (!/^\d{5}$/.test(z)) { f.classList.add("is-bad"); out.innerHTML = "Please enter a valid five-digit US ZIP code."; input.focus(); return; }
      if (!ZIPS.length) { f.classList.add("is-manual"); out.innerHTML = "We’re finalizing our ZIP list. Call or " + sms + " us on " + tel + " and we’ll check " + z + " for you."; return; }
      if (ZIPS.indexOf(z) > -1) { f.classList.add("is-yes"); out.innerHTML = "Good news: " + z + " is in our area. <a href=\"pickup.html\">Request a pickup</a> and we’ll confirm a time."; }
      else { f.classList.add("is-no"); out.innerHTML = "We don’t currently have a confirmed route for this ZIP. Call or " + sms + " us on " + tel + " to ask about options."; }
    });
  });

  /* ---------- FAQ search ---------- */
  var q = $("[data-faq-search]");
  if (q) {
    var empty = $("[data-faq-empty]");
    q.addEventListener("input", function () {
      var t = q.value.trim().toLowerCase(), any = false;
      $$("[data-faq-group]").forEach(function (g) {
        var vis = 0;
        $$("details[data-faq]", g).forEach(function (d) { var hit = !t || d.textContent.toLowerCase().indexOf(t) > -1; d.hidden = !hit; if (hit) vis++; });
        g.hidden = !vis; if (vis) any = true;
      });
      empty.hidden = any;
    });
  }
})();

/* ---------- Industries We Serve: auto-sliding carousel (vanilla, no libraries) ----------
   Shows 3 / 2 / 1.15 cards, advances one full set every ~4.5 s, loops endlessly
   (cloned edges), pauses on hover, focus, touch and when off-screen. No autoplay
   for prefers-reduced-motion. Horizontal drag only, so Lenis vertical scroll is untouched. */
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DELAY = 4500, C = 6;
  Array.prototype.forEach.call(document.querySelectorAll("[data-biz-carousel]"), function (root) {
    var vp = root.querySelector(".biz-viewport"), track = root.querySelector(".biz-track");
    var real = Array.prototype.slice.call(track.children), n = real.length;
    var dotsBox = root.querySelector(".biz-prog"), cur = root.querySelector("[data-biz-cur]"), live = root.querySelector("[data-biz-live]");
    function clone(el) { var c = el.cloneNode(true); c.setAttribute("aria-hidden", "true"); c.setAttribute("inert", ""); c.classList.add("is-clone");
      Array.prototype.forEach.call(c.querySelectorAll("img"), function (i) { i.alt = ""; i.loading = "eager"; }); return c; }
    real.slice(-C).forEach(function (el) { track.insertBefore(clone(el), real[0]); });
    real.slice(0, C).forEach(function (el) { track.appendChild(clone(el)); });
    root.style.setProperty("--dur", DELAY + "ms");
    var per = 3, pages = 1, idx = 0, timer = null, hold = 0, inView = true, busy = false;

    function measure() {
      var v = parseFloat(getComputedStyle(root).getPropertyValue("--v")) || 3;
      per = Math.max(1, Math.floor(v)); var p = Math.ceil(n / per);
      if (p !== pages || !dotsBox.children.length) {
        pages = p; dotsBox.innerHTML = "";
        for (var i = 0; i < pages; i++) { var b = document.createElement("button"); b.type = "button"; b.appendChild(document.createElement("span"));
          b.setAttribute("aria-label", "Show industries " + (i * per + 1) + " to " + Math.min(n, i * per + per));
          b.addEventListener("click", (function (k) { return function () { go(start(k), true); }; })(i)); dotsBox.appendChild(b); }
      }
      idx = start(page(idx)); place(false);
    }
    function start(p) { return Math.min(p * per, n - per); }
    function page(i) { return i >= n - per ? pages - 1 : Math.floor(i / per); }
    function place(anim) {
      track.classList.toggle("no-anim", !anim);
      var el = track.children[idx + C]; track.style.transform = "translate3d(" + (-(el.offsetLeft - track.children[0].offsetLeft)) + "px,0,0)";
      var pg = page(((idx % n) + n) % n);
      var ri = ((idx % n) + n) % n; if (cur) cur.textContent = (ri + 1 < 10 ? "0" : "") + (ri + 1);
      Array.prototype.forEach.call(dotsBox.children, function (d, k) { d.setAttribute("aria-current", k === pg ? "true" : "false"); d.classList.toggle("is-done", k < pg); d.classList.remove("is-run"); });
      arm(pg);
    }
    function go(i, user) {
      if (busy && !user) return;
      idx = i; busy = !reduce; place(!reduce);
      clearTimeout(root._st); if (reduce) settle(); else root._st = setTimeout(settle, 1000);
      if (user && live) live.textContent = "Showing industries " + (page(((idx % n) + n) % n) * per + 1) + " of " + n;
      if (user) restart();
    }
    function settle() {
      busy = false;
      if (idx >= n) { idx = 0; place(false); } else if (idx < 0) { idx = start(pages - 1); place(false); }
    }
    track.addEventListener("transitionend", function (e) { if (e.target === track) settle(); });
    function next(user) { var p = page(idx); go(p >= pages - 1 ? n : start(p + 1), user); }
    function prev(user) { var p = page(idx); go(p <= 0 ? -per : start(p - 1), user); }
    root.querySelector("[data-next]").addEventListener("click", function () { next(true); });
    root.querySelector("[data-prev]").addEventListener("click", function () { prev(true); });
    vp.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); next(true); } else if (e.key === "ArrowLeft") { e.preventDefault(); prev(true); }
    });

    function arm(pg) {
      var seg = dotsBox.children[pg]; if (!seg) return;
      void seg.offsetWidth; seg.classList.add("is-run");
    }
    dotsBox.addEventListener("animationend", function (e) {
      if (!reduce && !hold && inView && !document.hidden) next(false);
      else { var s = e.target.closest("button"); if (s) { s.classList.remove("is-run"); timer = s; } }
    });
    function sync() { root.classList.toggle("is-paused", !!hold || !inView || document.hidden); }
    function restart() { if (timer && timer.parentNode) { var t = timer; timer = null; t.classList.remove("is-run"); arm(Array.prototype.indexOf.call(dotsBox.children, t)); } }
    function pause() { hold++; sync(); } function resume() { hold = Math.max(0, hold - 1); sync(); if (!hold) restart(); }
    document.addEventListener("visibilitychange", function () { sync(); if (!document.hidden) restart(); });
    root.addEventListener("mouseenter", pause); root.addEventListener("mouseleave", resume);
    root.addEventListener("focusin", function () { if (!root._f) { root._f = 1; pause(); } });
    root.addEventListener("focusout", function (e) { if (!root.contains(e.relatedTarget) && root._f) { root._f = 0; resume(); } });
    var touchT = null;
    root.addEventListener("touchstart", function () { clearTimeout(touchT); if (!root._t) { root._t = 1; pause(); } }, { passive: true });
    root.addEventListener("touchend", function () { clearTimeout(touchT); touchT = setTimeout(function () { if (root._t) { root._t = 0; resume(); restart(); } }, 3500); }, { passive: true });

    /* Drag / swipe (pointer events; vertical moves fall through to the page) */
    var sx = 0, sy = 0, dx = 0, base = 0, drag = false, decided = false, horiz = false;
    vp.addEventListener("pointerdown", function (e) {
      if (e.button) return; drag = true; decided = false; horiz = false; sx = e.clientX; sy = e.clientY; dx = 0;
      if (busy) settle();
      base = -(track.children[idx + C].offsetLeft - track.children[0].offsetLeft);
    });
    vp.addEventListener("pointermove", function (e) {
      if (!drag) return; dx = e.clientX - sx; var dy = e.clientY - sy;
      if (!decided && (Math.abs(dx) > 6 || Math.abs(dy) > 6)) { decided = true; horiz = Math.abs(dx) > Math.abs(dy);
        if (horiz) { vp.classList.add("is-drag"); track.classList.add("no-anim"); try { vp.setPointerCapture(e.pointerId); } catch (_) {} } }
      if (horiz) track.style.transform = "translate3d(" + (base + dx) + "px,0,0)";
    });
    function end() {
      if (!drag) return; drag = false; vp.classList.remove("is-drag");
      if (!horiz) return;
      var th = Math.min(80, vp.offsetWidth * .12);
      if (dx < -th) next(true); else if (dx > th) prev(true); else place(true);
    }
    vp.addEventListener("pointerup", end); vp.addEventListener("pointercancel", end);

    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { inView = es[0].isIntersecting; sync(); if (inView) restart(); }).observe(root);
    var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(measure, 120); });
    measure(); restart();
    root._biz = { next: next, prev: prev, get idx() { return idx; }, get hold() { return hold; } };
  });
})();
