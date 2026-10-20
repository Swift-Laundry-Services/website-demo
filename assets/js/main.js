/* Swift Laundry Services — site behaviour (vanilla JS; Lenis is self-hosted in assets/vendor).
   Business details, prices and form targets live in site-config.js. */
(function () {
  "use strict";
  var CFG = window.SWIFT_CONFIG || {};
  var B = CFG.business || {};
  var P = CFG.pricing || {};
  var doc = document;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var money = function (n) { return "$" + Number(n).toFixed(2); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var get = function (path) { return path.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, CFG); };
  var ICON = function (paths, cls) { return '<svg class="icon ' + (cls || "") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + paths + "</svg>"; };
  var I_CHECK = '<path d="M20 6 9 17l-5-5"/>';
  var I_INFO = '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>';

  /* ---------- Business details ---------- */
  var smsHref = function (body) { return "sms:" + B.phoneE164 + (body ? "?&body=" + encodeURIComponent(body) : ""); };
  $$("[data-bind]").forEach(function (el) {
    var key = el.getAttribute("data-bind");
    if (key === "phone" && B.phoneDisplay) el.textContent = B.phoneDisplay;
    if (key === "email" && B.email) el.textContent = B.email;
    if (key === "address" && B.address) el.textContent = B.address;
    if (key === "hours" && B.hours) el.textContent = B.hours;
    if (key === "serviceArea" && B.serviceArea) el.textContent = B.serviceArea;
    if (key === "extraPerLb" && P.extraPerLb != null) el.textContent = money(P.extraPerLb);
    if (key === "priceFrom" && P.washFold && P.washFold.length) el.textContent = money(Math.min.apply(null, P.washFold.filter(function (x) { return x.confirmed; }).map(function (x) { return x.price; })));
    if (key === "year") el.textContent = new Date().getFullYear();
  });
  $$("[data-price]").forEach(function (el) {
    var v = get("pricing." + el.getAttribute("data-price"));
    if (typeof v === "number") el.textContent = money(v);
  });
  $$("[data-href]").forEach(function (el) {
    var t = el.getAttribute("data-href");
    if (t === "tel" && B.phoneE164) el.href = "tel:" + B.phoneE164;
    if (t === "sms" && B.phoneE164) el.href = smsHref("");
    if (t === "email" && B.email) el.href = "mailto:" + B.email;
  });
  $$("[data-requires]").forEach(function (el) { el.hidden = !get(el.getAttribute("data-requires")); });
  $$("[data-fallback-for]").forEach(function (el) { el.hidden = !!get(el.getAttribute("data-fallback-for")); });
  $$("[data-social]").forEach(function (el) {
    var url = (CFG.social || {})[el.getAttribute("data-social")];
    if (url) { el.href = url; el.hidden = false; } else { el.hidden = true; }
  });
  $$("[data-social-row]").forEach(function (row) { row.hidden = !$$("[data-social]", row).some(function (a) { return !a.hidden; }); });

  /* ---------- Service-area map ---------- */
  var MAP = CFG.map || {};
  $$("[data-map]").forEach(function (f) { if (MAP.embedUrl && f.getAttribute("src") !== MAP.embedUrl) f.setAttribute("src", MAP.embedUrl); });
  $$("[data-map-link]").forEach(function (a) { if (MAP.linkUrl) a.href = MAP.linkUrl; });
  $$("[data-map-caption]").forEach(function (el) { if (MAP.caption) el.textContent = MAP.caption; });

  /* ---------- Logo (owner is sending a new one: set brand.logo in site-config.js) ---------- */
  var BR = CFG.brand || {};
  if (BR.logo) $$("img[data-logo]").forEach(function (img) { img.src = BR.logo; });

  /* ---------- Pricing (layout matches the design PDF) ---------- */
  var IMG = "assets/img/design/";
  var BAGS = {"bag": [274, 548, 456], "bag-small": [214, 428, 282], "duvet": [536, 1072, 280]};
  var art = function (it) {
    var p = function (n, h) {
      var m = BAGS[n];
      return '<picture><source type="image/webp" srcset="' + IMG + n + "-" + m[0] + ".webp 1x, " + IMG + n + "-" + m[1] + '.webp 2x"><img src="' + IMG + n + "-" + m[0] + '.png" alt="" width="' + m[0] + '" height="' + m[2] + '" loading="lazy" style="height:' + h + 'px;width:auto"></picture>';
    };
    if (it.bags === "duvet") return p("duvet", 74);
    if (it.bags >= 2) return '<span style="display:flex">' + p("bag", 120) + '<span style="margin-left:-36px">' + p("bag", 120) + "</span></span>";
    if (it.bags >= 1) return p("bag", 120);
    return p("bag-small", 76);
  };
  $$('[data-render="washFold"]').forEach(function (wrap) {
    wrap.innerHTML = (P.washFold || []).map(function (it) {
      return '<li class="wf"><div class="art" aria-hidden="true">' + art(it) + "</div>" +
        '<h3 class="h-sm">' + esc(it.name) + "</h3>" +
        '<p class="price">' + money(it.price) + (it.confirmed ? "" : '<span class="visually-hidden"> (price to be confirmed)</span>') + "</p>" +
        (it.size ? "<p>" + esc(it.size) + "</p>" : "") + (it.weight ? "<p>" + esc(it.weight) + "</p>" : "") + "</li>";
    }).join("");
  });
  $$('[data-render="dryCleaning"], [data-render="ironing"]').forEach(function (list) {
    var items = P[list.getAttribute("data-render")] || [];
    list.innerHTML = items.map(function (it) {
      return '<li><span class="name">' + esc(it.name) + '</span><span class="line" aria-hidden="true"></span><span class="amt">' + money(it.price) + (it.confirmed ? "" : '<span class="visually-hidden"> (to be confirmed)</span>') + "</span></li>";
    }).join("");
  });
  $$("[data-tbc-for]").forEach(function (el) {
    var key = el.getAttribute("data-tbc-for");
    var items = key === "any" ? [].concat(P.washFold || [], P.dryCleaning || [], P.ironing || []) : (P[key] || []);
    el.hidden = !items.some(function (x) { return x && x.confirmed === false; });
  });

  /* ---------- Header: tall on the home page until scrolled (as in the PDF) ---------- */
  var header = $(".site-header");
  var onScroll = function () { if (header) header.classList.toggle("is-scrolled", window.scrollY > 40); };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- "View all industries" and other disclosure buttons ---------- */
  $$("[data-toggle]").forEach(function (btn) {
    var target = doc.getElementById(btn.getAttribute("aria-controls"));
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", String(open));
      if (target) target.hidden = !open;
    });
  });

  /* ---------- Prefill from query string (?topic=quote, ?service=dry-cleaning) ---------- */
  try {
    var qs = new URLSearchParams(window.location.search);
    qs.forEach(function (val, key) {
      $$('[data-prefill="' + key + '"]').forEach(function (el) {
        if (el.tagName === "SELECT") { el.value = val; }
        else if (el.type === "checkbox" || el.type === "radio") { if (el.value === val) el.checked = true; }
      });
    });
  } catch (e) { /* older browsers: ignore */ }

  /* ---------- Login tabs ---------- */
  $$("[data-tabs]").forEach(function (tabs) {
    var btns = $$('[role="tab"]', tabs);
    var select = function (btn) {
      btns.forEach(function (b) {
        var on = b === btn;
        b.setAttribute("aria-selected", String(on));
        b.tabIndex = on ? 0 : -1;
        $("#" + b.getAttribute("aria-controls")).hidden = !on;
      });
    };
    if (window.location.hash === "#create") { var cb = doc.getElementById("tab-create"); if (cb) select(cb); }
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { select(b); });
      b.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          var n = btns[(i + (e.key === "ArrowRight" ? 1 : btns.length - 1)) % btns.length];
          select(n); n.focus(); e.preventDefault();
        }
      });
    });
  });

  /* ---------- Forms ---------- */
  var MESSAGES = {
    valueMissing: "This field is required.",
    typeMismatch: { email: "Please enter a valid email address.", tel: "Please enter a valid phone number." },
    patternMismatch: "Please check the format."
  };
  var fieldMessage = function (el) {
    var v = el.validity;
    if (v.valueMissing) return el.getAttribute("data-msg-required") || MESSAGES.valueMissing;
    if (v.typeMismatch) return MESSAGES.typeMismatch[el.type] || "Please check this value.";
    if (v.patternMismatch) return el.getAttribute("data-msg-pattern") || MESSAGES.patternMismatch;
    if (v.tooShort) return "Please use at least " + el.minLength + " characters.";
    if (v.rangeUnderflow) return el.getAttribute("data-msg-min") || "Please choose a later date.";
    return "";
  };
  var setError = function (wrap, msg) {
    if (!wrap) return;
    var out = $(".field-error", wrap);
    wrap.classList.toggle("has-error", !!msg);
    $$("input, select, textarea", wrap).forEach(function (c) { if (msg) c.setAttribute("aria-invalid", "true"); else c.removeAttribute("aria-invalid"); });
    if (out) out.textContent = msg || "";
  };
  var validate = function (form) {
    var firstBad = null;
    $$(".field", form).forEach(function (wrap) {
      var ctrl = $("input, select, textarea", wrap);
      if (!ctrl || ctrl.type === "checkbox" || ctrl.type === "radio") return;
      var msg = ctrl.checkValidity() ? "" : fieldMessage(ctrl);
      setError(wrap, msg);
      if (msg && !firstBad) firstBad = ctrl;
    });
    $$("[data-require-one]", form).forEach(function (fs) {
      var ok = $$("input", fs).some(function (i) { return i.checked; });
      setError(fs, ok ? "" : fs.getAttribute("data-require-one"));
      if (!ok && !firstBad) firstBad = $("input", fs);
    });
    var bad = $$('[aria-invalid="true"]', form);
    if (bad.length) firstBad = bad[0]; // earliest in DOM order
    if (firstBad) firstBad.focus();
    return !firstBad;
  };
  var summarize = function (form) {
    var lines = [];
    $$(".field, [data-summary-group]", form).forEach(function (wrap) {
      var label = (wrap.getAttribute("data-summary-label") || ($("label, legend", wrap) || {}).textContent || "").replace(/\(optional\)/i, "").trim();
      var vals = $$("input, select, textarea", wrap).filter(function (c) {
        return (c.type === "checkbox" || c.type === "radio") ? c.checked : c.value.trim() !== "" && c.type !== "password";
      }).map(function (c) { return (c.type === "checkbox" || c.type === "radio") ? (c.getAttribute("data-label") || c.value) : c.value.trim(); });
      if (label && vals.length) lines.push(label + ": " + vals.join(", "));
    });
    return lines;
  };
  var resultPanel = function (form, html) {
    var box = $(".form-result", form.parentNode) || doc.createElement("div");
    box.className = "form-result";
    box.setAttribute("role", "status");
    box.setAttribute("tabindex", "-1");
    box.innerHTML = html;
    if (!box.parentNode) form.parentNode.insertBefore(box, form.nextSibling);
    box.hidden = false;
    box.focus({ preventScroll: true });
    if (window.__lenis) window.__lenis.scrollTo(box, { offset: -120 }); else box.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
  };

  $$("form[data-form]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    $$("input, select, textarea", form).forEach(function (c) {
      var evt = (c.type === "checkbox" || c.type === "radio") ? "change" : "blur";
      c.addEventListener(evt, function () {
        var wrap = c.closest(".field, [data-require-one]");
        if (!wrap || !wrap.classList.contains("has-error")) return;
        if (wrap.hasAttribute("data-require-one")) setError(wrap, $$("input", wrap).some(function (i) { return i.checked; }) ? "" : wrap.getAttribute("data-require-one"));
        else setError(wrap, c.checkValidity() ? "" : fieldMessage(c));
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var kind = form.getAttribute("data-form");
      var subject = form.getAttribute("data-subject") || "Website enquiry";

      if (kind === "login") {
        resultPanel(form, "<h3>" + ICON(I_INFO) + "Customer accounts are coming soon</h3><p>Online accounts aren’t live yet. You can still book a pickup online or call or text us on <a href=\"tel:" + B.phoneE164 + "\">" + esc(B.phoneDisplay) + "</a>.</p><div class=\"btn-row\"><a class=\"btn btn--primary btn--sm\" href=\"order.html\">Order a pickup</a></div>");
        return;
      }

      var lines = summarize(form);
      var body = subject + "\n\n" + lines.join("\n");
      var F = CFG.forms || {};

      if (F.endpoint) {
        var btn = $('[type="submit"]', form);
        if (btn) { btn.disabled = true; btn.setAttribute("aria-busy", "true"); }
        var fd = new FormData(form);
        fd.append("_subject", subject);
        fetch(F.endpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
          .then(function (r) { if (!r.ok) throw new Error(r.status); })
          .then(function () {
            form.reset();
            resultPanel(form, "<h3>" + ICON(I_CHECK) + "Thank you — we’ve got your request</h3><p>We’ll be in touch soon. If it’s urgent, call or text <a href=\"tel:" + B.phoneE164 + "\">" + esc(B.phoneDisplay) + "</a>.</p>");
          })
          .catch(function () {
            resultPanel(form, "<h3>" + ICON(I_INFO) + "Something went wrong</h3><p>Your request couldn’t be sent. Please call or text us on <a href=\"tel:" + B.phoneE164 + "\">" + esc(B.phoneDisplay) + "</a>.</p>");
          })
          .then(function () { if (btn) { btn.disabled = false; btn.removeAttribute("aria-busy"); } });
        return;
      }

      if (F.email) {
        window.location.href = "mailto:" + F.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        resultPanel(form, "<h3>" + ICON(I_CHECK) + "Almost done</h3><p>Your email app should open with your request filled in — just press send. Nothing opened? Call or text <a href=\"tel:" + B.phoneE164 + "\">" + esc(B.phoneDisplay) + "</a>.</p>");
        return;
      }

      // No backend configured yet: hand the visitor a ready-made text message.
      resultPanel(form,
        "<h3>" + ICON(I_INFO) + "Online booking is almost ready</h3>" +
        "<p>Our online form isn’t connected yet, so nothing has been sent. Your details are ready to go — tap below to send them to us by text, or give us a call.</p>" +
        '<div class="btn-row"><a class="btn btn--primary btn--sm" href="' + smsHref(body) + '">' + ICON('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>') + "Text my request</a>" +
        '<a class="btn btn--outline btn--sm" href="tel:' + B.phoneE164 + '">Call ' + esc(B.phoneDisplay) + "</a></div>");
    });
  });

  /* ---------- Date inputs: no past dates ---------- */
  $$('input[type="date"][data-min-today]').forEach(function (el) {
    var d = new Date(); d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    el.min = d.toISOString().slice(0, 10);
  });

  /* ======================================================================
     Version 3 (modernized PDF): menu sheet, testimonials carousel,
     smooth scrolling (Lenis), scroll-reveal, PWA service worker.
     ====================================================================== */
  var ICONS = {"quote": "<svg class=\"lu lu-quote\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z\" /> <path d=\"M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z\" /></svg>", "star": "<svg class=\"lu lu-star\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z\" /></svg>", "user-round": "<svg class=\"lu lu-user-round\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"8\" r=\"5\" /> <path d=\"M20 21a8 8 0 0 0-16 0\" /></svg>", "chevron-left": "<svg class=\"lu lu-chevron-left\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"m15 18-6-6 6-6\" /></svg>", "chevron-right": "<svg class=\"lu lu-chevron-right\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"m9 18 6-6-6-6\" /></svg>", "pause": "<svg class=\"lu lu-pause\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><rect x=\"14\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\" /> <rect x=\"5\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\" /></svg>", "play": "<svg class=\"lu lu-play\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z\" /></svg>", "check": "<svg class=\"lu lu-check\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M20 6 9 17l-5-5\" /></svg>", "info": "<svg class=\"lu lu-info\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 16v-4\" /> <path d=\"M12 8h.01\" /></svg>", "message-circle-more": "<svg class=\"lu lu-message-circle-more\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719\" /> <path d=\"M8 12h.01\" /> <path d=\"M12 12h.01\" /> <path d=\"M16 12h.01\" /></svg>", "phone": "<svg class=\"lu lu-phone\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384\" /></svg>", "tag": "<svg class=\"lu lu-tag\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z\" /> <circle cx=\"7.5\" cy=\"7.5\" r=\".5\" fill=\"currentColor\" /></svg>"};

  /* ---------- Menu: header button (tablet/phone) + "More" tab open the same panel ---------- */
  var menuPanel = $("#site-menu");
  var backdrop = $("[data-sheet-backdrop]");
  var openers = $$('[aria-controls="site-menu"]');
  var lastOpener = null;
  var setMenu2 = function (open, opener) {
    if (!menuPanel) return;
    menuPanel.hidden = !open;
    if (backdrop) backdrop.hidden = !open;
    doc.documentElement.classList.toggle("menu-open", open);
    openers.forEach(function (b) {
      b.setAttribute("aria-expanded", String(open && (b === opener || !opener)));
      if (b.classList.contains("menu-toggle")) b.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    if (window.__lenis) { if (open) window.__lenis.stop(); else window.__lenis.start(); }
    if (open) { lastOpener = opener; var first = $("a", menuPanel); if (first) first.focus({ preventScroll: true }); }
    else if (opener !== false && lastOpener) { lastOpener.focus({ preventScroll: true }); }
  };
  openers.forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      setMenu2(menuPanel.hidden, b);
    });
  });
  if (backdrop) backdrop.addEventListener("click", function () { setMenu2(false); });
  doc.addEventListener("keydown", function (e) { if (e.key === "Escape" && menuPanel && !menuPanel.hidden) setMenu2(false); });
  doc.addEventListener("click", function (e) { if (menuPanel && !menuPanel.hidden && !menuPanel.contains(e.target)) setMenu2(false); });
  if (menuPanel) $$("a", menuPanel).forEach(function (a) { a.addEventListener("click", function () { setMenu2(false, false); }); });

  /* ---------- Testimonials (data: SWIFT_CONFIG.testimonials) ---------- */
  var initials = function (name) {
    return String(name || "").split(/\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w.charAt(0).toUpperCase(); }).join("");
  };
  $$("[data-testimonials]").forEach(function (root) {
    var data = (CFG.testimonials || []).filter(function (t) { return t && t.quote; });
    var track = $(".t-track", root);
    var section = root.closest("section") || doc;
    var controls = $("[data-t-controls]", section);
    var dotsWrap = $("[data-t-dots]", root);
    var note = $("[data-t-note]", root);
    if (data.length) {
      track.innerHTML = data.map(function (t, i) {
        var sample = !!t.sample;
        var stars = "";
        if (!sample && t.rating) {
          var n = Math.max(0, Math.min(5, Math.round(t.rating)));
          stars = '<span class="stars" role="img" aria-label="Rated ' + n + ' out of 5">' + new Array(n + 1).join(ICONS.star) + "</span>";
        }
        var tag = sample ? '<span class="t-tag">' + ICONS.tag + "Sample review</span>" : "";
        var av = t.anonymous || !t.name ? ICONS["user-round"] : esc(initials(t.name));
        return '<li class="t-card ' + (sample ? "t-card--sample" : (i === 0 ? "t-card--real" : "")) + '" aria-roledescription="slide" aria-label="' + (i + 1) + " of " + data.length + '">' +
          '<div class="t-top"><span class="t-quote" aria-hidden="true">' + ICONS.quote + "</span>" + stars + tag + "</div>" +
          '<blockquote class="t-text"><p>' + esc(t.quote) + "</p></blockquote>" +
          '<div class="t-who"><span class="t-avatar" aria-hidden="true">' + av + "</span><div>" +
          '<p class="t-name">' + esc(t.name || "Customer") + "</p>" +
          '<p class="t-meta">' + esc([t.detail, t.location].filter(Boolean).join(" · ")) + "</p></div></div></li>";
      }).join("");
      if (note) note.hidden = !data.some(function (t) { return t.sample; });
    }
    var cards = $$(".t-card", track);
    if (cards.length < 2) return;
    controls.hidden = false;
    dotsWrap.hidden = false;
    var DELAY = (CFG.testimonialsAutoplayMs || 5000);
    var idx = 0, timer = null, userStopped = reduceMotion;
    dotsWrap.setAttribute("role", "group");
    dotsWrap.setAttribute("aria-label", "Choose a review");
    dotsWrap.innerHTML = cards.map(function (_, i) { return '<button class="t-dot" type="button" aria-label="Show review ' + (i + 1) + '"></button>'; }).join("");
    var dots = $$(".t-dot", dotsWrap);
    var maxScroll = function () { return track.scrollWidth - track.clientWidth; };
    var cardLeft = function (i) { return cards[i].offsetLeft - cards[0].offsetLeft; };
    var go = function (i, user) {
      idx = (i + cards.length) % cards.length;
      var left = Math.min(cardLeft(idx), maxScroll());
      track.scrollTo({ left: left, behavior: reduceMotion ? "auto" : "smooth" });
      mark(idx);
      if (user) track.setAttribute("aria-live", "polite");
    };
    var mark = function (i) { dots.forEach(function (d, k) { d.setAttribute("aria-current", k === i ? "true" : "false"); }); };
    var nearest = function () {
      var sl = track.scrollLeft, best = 0, bd = Infinity;
      cards.forEach(function (c, i) { var d = Math.abs(Math.min(cardLeft(i), maxScroll()) - sl); if (d < bd) { bd = d; best = i; } });
      if (sl >= maxScroll() - 4) { /* at the end: several cards share the last position; keep the requested index if it is one of them */
        if (Math.min(cardLeft(idx), maxScroll()) >= maxScroll() - 4) best = idx;
      }
      return best;
    };
    var scrollTimer;
    track.addEventListener("scroll", function () {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(function () { idx = nearest(); mark(idx); }, 120);
    }, { passive: true });
    var playBtn = $("[data-t-toggle]", section);
    var held = function () { return root.matches(":hover") || root.contains(doc.activeElement) || touchHold; };
    var touchHold = false, visible = true;
    var sync = function () {
      var running = !userStopped && visible && !doc.hidden;
      if (!running) { clearInterval(timer); timer = null; }
      else if (!timer) {
        timer = setInterval(function () { if (!held()) { track.setAttribute("aria-live", "off"); go(idx + 1, false); } }, DELAY);
      }
      root.classList.toggle("is-playing", running);
      if (playBtn) {
        playBtn.setAttribute("aria-label", userStopped ? "Start automatic sliding" : "Pause automatic sliding");
        playBtn.classList.toggle("is-stopped", userStopped);
      }
    };
    $("[data-t-prev]", section).addEventListener("click", function () { go(idx - 1, true); });
    $("[data-t-next]", section).addEventListener("click", function () { go(idx + 1, true); });
    dots.forEach(function (d, i) { d.addEventListener("click", function () { go(i, true); }); });
    if (playBtn) playBtn.addEventListener("click", function () { userStopped = !userStopped; sync(); });
    var holdT; track.addEventListener("touchstart", function () { touchHold = true; clearTimeout(holdT); }, { passive: true });
    track.addEventListener("touchend", function () { holdT = setTimeout(function () { touchHold = false; }, 4000); }, { passive: true });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { go(idx + 1, true); e.preventDefault(); }
      if (e.key === "ArrowLeft") { go(idx - 1, true); e.preventDefault(); }
    });
    doc.addEventListener("visibilitychange", sync);
    /* only autoplay while the carousel is on screen */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[es.length - 1].isIntersecting; if (!visible) { clearInterval(timer); timer = null; root.classList.remove("is-playing"); } else sync(); }, { threshold: 0.25 }).observe(root);
    }
    mark(0);
    sync();
    root.__carousel = { go: go, get index() { return idx; }, get playing() { return !!timer && !held(); } };
  });

  /* ---------- Smooth scrolling (Lenis, self-hosted). Off for reduced motion. ---------- */
  if (!reduceMotion && window.Lenis) {
    try {
      var lenis = new window.Lenis({ autoRaf: true, anchors: { offset: -90 }, lerp: 0.11, wheelMultiplier: 1, smoothWheel: true, syncTouch: false });
      window.__lenis = lenis;
      if (header) lenis.on("scroll", onScroll);
    } catch (e) { /* fall back to native smooth scrolling */ }
  }

  /* ---------- Scroll reveal ---------- */
  var revealEls = $$("[data-reveal]");
  if (!reduceMotion && "IntersectionObserver" in window && revealEls.length) {
    doc.documentElement.classList.add("js-reveal");
    var groups = new Map();
    revealEls.forEach(function (el) {
      var p = el.parentNode; var n = groups.get(p) || 0; groups.set(p, n + 1);
      if (n) el.style.setProperty("--d", Math.min(n, 5) * 0.08 + "s");
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Installable app: service worker (network-first, offline fallback) ---------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
  }
})();

/* Accordions: opening one closes the others (nested ones keep their parent open) */
document.addEventListener("toggle", function (e) {
  var d = e.target;
  if (!(d instanceof HTMLDetailsElement) || !d.open) return;
  document.querySelectorAll("details[open]").forEach(function (o) {
    if (o !== d && !o.contains(d) && !d.contains(o)) o.open = false;
  });
}, true);

/* Safety: never leave the menu backdrop stuck (back/forward cache, tab restore) */
(function () {
  function reset() {
    var p = document.getElementById("site-menu"), b = document.querySelector("[data-sheet-backdrop]");
    if (p) p.hidden = true; if (b) b.hidden = true;
    document.documentElement.classList.remove("menu-open");
    document.querySelectorAll('[aria-controls="site-menu"]').forEach(function (x) { x.setAttribute("aria-expanded", "false"); });
    if (window.__lenis) window.__lenis.start();
  }
  window.addEventListener("pageshow", reset);
  var b = document.querySelector("[data-sheet-backdrop]");
  if (b) b.addEventListener("touchend", function () { setTimeout(reset, 0); }, { passive: true });
})();
