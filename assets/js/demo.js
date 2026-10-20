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
