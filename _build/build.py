#!/usr/bin/env python3
# Swift Laundry Services site generator.
# Designed & developed by Innocent Christo. © 2026 Innocent Christo.
"""Generates the demo site's HTML pages. Run: python3 _build/build.py (from repo root).
Shared header / menu / tab bar / footer live here so every page stays in sync."""
import re, json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://swift-laundry-services.github.io/website-demo/"
LUCIDE = "/workspace/swift-v3-img/lucide/package/icons/"
IMGS = json.load(open(os.path.join(ROOT, "_build/images.json")))
_ic = json.load(open(os.path.join(ROOT, "_build/icons.json"))) if os.path.exists(os.path.join(ROOT, "_build/icons.json")) else {}
def I(name):
    if name not in _ic:
        s = open(LUCIDE + name + ".svg").read()
        body = re.search(r">\s*(.*)</svg>", s.split("-->", 1)[1], re.S).group(1)
        body = " ".join(l.strip() for l in body.strip().splitlines())
        _ic[name] = f'<svg class="lu lu-{name}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{body}</svg>'
    return _ic[name]
SRC_INDEX = open(os.path.join(ROOT, "_build/v3-index.html")).read()
IG = re.search(r'(<svg aria-hidden="true" focusable="false" viewBox="-0 -416 448 448">.*?</svg>)', SRC_INDEX, re.S).group(1)
FB = re.search(r'(<svg aria-hidden="true" focusable="false" viewBox="0 -448 512 510">.*?</svg>)', SRC_INDEX, re.S).group(1)
TEL = "tel:+17144027530"; SMS = "sms:+17144027530"; PHONE = "(714) 402-7530"

def pic(key, alt, sizes, cls="", eager=False):
    m = IMGS[key]; ws = m["ws"]; W = ws[-1]; H = m["h"]
    ss = ", ".join(f"assets/img/demo/{key}-{w}.webp {w}w" for w in ws)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}><source type="image/webp" srcset="{ss}" sizes="{sizes}">'
            f'<img src="assets/img/demo/{key}-{m["jpg"]}.jpg" alt="{alt}" width="{W}" height="{H}" {load}></picture>')

def tbc(text="To be confirmed"):
    return f'<span class="tbc" title="Needs the owner’s confirmation before launch">{I("circle-alert")}{text}</span>'

NAV = [("services.html", "Services &amp; Pricing"), ("how-it-works.html", "How It Works"), ("about.html", "About"), ("service-area.html", "Service Area &amp; Contact")]
MENU = [("index.html", "house", "Home"), ("services.html", "tag", "Services &amp; Pricing"), ("pickup.html", "truck", "Schedule a Pickup"),
        ("how-it-works.html", "list-checks", "How It Works"), ("about.html", "users-round", "About"), ("service-area.html", "map-pin", "Service Area &amp; Contact"),
        ("faq.html", "circle-help", "FAQs"), ("laundry-care.html", "shirt", "Laundry Care")]
TABS = [("index.html", "house", "Home"), ("services.html", "tag", "Pricing"), ("pickup.html", "truck", "Pickup"), ("service-area.html", "message-circle-more", "Contact")]

def cur(a, b): return ' aria-current="page"' if a == b else ""

def head(path, title, desc, extra=""):
    url = BASE + ("" if path == "index.html" else path)
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<!-- Designed & developed by Innocent Christo. © 2026 Innocent Christo. Built for Swift Laundry Services. -->
<meta name="author" content="Innocent Christo">
<link rel="author" href="humans.txt">{extra}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#3E157B">
<meta name="color-scheme" content="light">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Swift Laundry">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Swift Laundry Services">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/montserrat-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
<link rel="stylesheet" href="assets/css/demo.css">
</head>'''

def header(path):
    nav = "".join(f'<li><a href="{h}"{cur(h, path)}>{l}</a></li>' for h, l in NAV)
    menu = "".join(f'<li><a href="{h}"{cur(h, path)}>{I(i)}<span>{l}</span></a></li>' for h, i, l in MENU)
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-header>
  <div class="bar">
    <a class="brand" href="index.html" aria-label="Swift Laundry Services — home"><img src="assets/img/logo.svg" alt="Swift Laundry Services" width="324" height="112" data-logo></a>
    <nav class="primary-nav" aria-label="Main"><ul class="nav-list">{nav}</ul></nav>
    <div class="header-actions">
      <a class="btn btn--purple btn--sm header-member" href="pickup.html">Schedule a Pickup</a>
      <a class="icon-btn header-call" href="{TEL}" data-href="tel" aria-label="Call us on {PHONE}">{I("phone")}</a>
      <button class="icon-btn menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open menu">{I("menu").replace('class="lu lu-menu"', 'class="lu lu-menu i-open"')}{I("x").replace('class="lu lu-x"', 'class="lu lu-x i-close"')}</button>
    </div>
  </div>
</header>
<nav class="menu-panel" id="site-menu" aria-label="Menu" hidden>
  <ul>{menu}<li class="menu-call"><a href="{TEL}" data-href="tel">{I("phone")}<span>Call <span data-bind="phone">{PHONE}</span></span></a></li></ul>
</nav>
<main id="main">
'''

def footer(path):
    tabs = []
    for h, i, l in TABS:
        if h == "pickup.html":
            tabs.append(f'<a class="tab-item tab-order" href="{h}"{cur(h, path)}><span class="fab">{I(i)}</span><span>{l}</span></a>')
        else:
            tabs.append(f'<a class="tab-item" href="{h}"{cur(h, path)}>{I(i)}<span>{l}</span></a>')
    tabs = "\n  ".join(tabs)
    return f'''</main>
<div class="sheet-backdrop" data-sheet-backdrop hidden></div>
<nav class="tabbar" aria-label="Quick links">
  {tabs}
  <button class="tab-item" type="button" aria-controls="site-menu" aria-expanded="false" data-menu-more>{I("layout-grid")}<span>More</span></button>
</nav>
<footer class="site-footer has-blobs">
  <div class="blobs blobs--dark" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap">
    <div class="footer-grid footer-grid--4">
      <div class="footer-brand">
        <a class="logo-chip" href="index.html" aria-label="Swift Laundry Services — home"><img src="assets/img/logo.svg" alt="Swift Laundry Services" width="324" height="112" loading="lazy" data-logo></a>
        <p>Laundry pickup &amp; delivery for Garfield Heights and selected Cleveland neighborhoods. We pick up, wash, dry and neatly fold your laundry, then bring it back to your door.</p>
      </div>
      <nav aria-labelledby="f-explore"><h2 id="f-explore">Explore</h2><ul class="footer-links"><li><a href="services.html">Services &amp; Pricing</a></li><li><a href="how-it-works.html">How It Works</a></li><li><a href="about.html">About</a></li><li><a href="service-area.html">Service Area &amp; Contact</a></li><li><a href="pickup.html">Schedule a Pickup</a></li></ul></nav>
      <nav aria-labelledby="f-help"><h2 id="f-help">Help</h2><ul class="footer-links"><li><a href="faq.html">FAQs</a></li><li><a href="laundry-care.html">Laundry Care</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="service-terms.html">Service Terms</a></li></ul></nav>
      <div>
        <h2>Get in touch</h2>
        <ul class="footer-contact">
          <li><a href="{TEL}" data-href="tel">{I("phone")}<span data-bind="phone">{PHONE}</span></a></li>
          <li><a href="{SMS}" data-href="sms">{I("message-square")}<span>Text us</span></a></li>
          <li data-requires="business.email" hidden><a href="#" data-href="email">{I("mail")}<span data-bind="email"></span></a></li>
          <li>{I("map-pin")}<span>Garfield Heights &amp; selected Cleveland neighborhoods</span></li>
        </ul>
        <a class="btn btn--cyan btn--sm" href="pickup.html" style="margin-top:16px">Schedule a Pickup {I("arrow-right")}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-bind="year">2026</span> Swift Laundry Services</span>
      <ul class="footer-social" data-social-row hidden>
        <li><a data-social="instagram" href="#" aria-label="Instagram" hidden>{IG}</a></li>
        <li><a data-social="facebook" href="#" aria-label="Facebook" hidden>{FB}</a></li>
      </ul>
    </div>
    <p class="demo-note">{I("flask-conical")}<span><strong>Demo for client review.</strong> Items marked “To be confirmed” (ZIP list, fees, turnaround and policies) need the owner’s confirmation before launch. Photos are generated concept images from the design package.</span></p>
  </div>
</footer>
<script src="assets/js/site-config.js"></script>
<script src="assets/vendor/lenis.min.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/demo.js"></script>
</body>
</html>
'''

def band(title, crumb, eyebrow="", sub=""):
    return f'''<section class="page-band"><div class="band-inner has-blobs"><div class="blobs blobs--dark" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div><div class="wrap"><div>{f'<span class="band-eyebrow">{eyebrow}</span>' if eyebrow else ""}<h1>{title}</h1>{f'<p class="band-sub">{sub}</p>' if sub else ""}</div><nav class="crumb" aria-label="Breadcrumb"><ol><li><a href="index.html">{I("house")}Home</a></li><li><span class="sep" aria-hidden="true">/</span><span aria-current="page">{crumb}</span></li></ol></nav></div></div></section>
'''

def media_hero(eyebrow, title, sub, img, alt, actions="", extra=""):
    return f'''<section class="d-hero" aria-labelledby="hero-title">
  <div class="d-hero-inner has-blobs"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
    <div class="d-hero-copy">
      <span class="hero-chip"><span class="dot">{I("map-pin")}</span>{eyebrow}</span>
      <h1 id="hero-title">{title}</h1>
      <p>{sub}</p>
      {actions}{extra}
    </div>
    <div class="d-hero-media">{pic(img, alt, "(max-width: 860px) 100vw, 50vw", eager=True)}</div>
  </div>
</section>
'''

def cta(title, label="Schedule a Pickup", href="pickup.html"):
    return f'''<section class="d-cta" aria-label="{html.escape(re.sub('<[^>]+>', '', title), quote=True)}">
  <div class="d-cta-inner has-blobs"><div class="blobs blobs--dark" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
    <h2>{title}</h2>
    <div class="d-cta-actions"><a class="btn btn--cyan" href="{href}">{label} {I("arrow-right")}</a><a class="btn btn--ghost-light" href="{TEL}" data-href="tel">{I("phone")}Call <span data-bind="phone">{PHONE}</span></a></div>
  </div>
</section>
'''

def zipcheck(id_, compact=False):
    return f'''<form class="zip-card{' zip-card--compact' if compact else ''}" data-zip action="#" novalidate aria-labelledby="{id_}-t">
  <span class="icon-tile icon-tile--soft">{I("map-pin")}</span>
  <label id="{id_}-t" for="{id_}">Do we serve your neighborhood?</label>
  <div class="zip-row"><input class="input" id="{id_}" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="Enter ZIP code" aria-describedby="{id_}-out"><button class="btn btn--purple" type="submit">Check availability</button></div>
  <p class="zip-out" id="{id_}-out" role="status" aria-live="polite"></p>
</form>'''

TIERS = [("Single Load", "1/2 Full Laundry Bag", "1-10 lbs", 41.99, "single", "shopping-bag"),
         ("Couple Load", "1 Full Laundry Bag", "10-25 lbs", 56.99, "couple", "package"),
         ("Family Load", "2 Full Laundry Bags", "25-40 lbs", 79.99, "family", "boxes"),
         ("Duvet or blanket", "", "", 41.99, "duvet", "bed-double")]
EXTRA_NOTE = 'Any additional weight will be <span data-price="extraPerLb">$1.90</span>/lb (We weigh your order at pickup)'

def tiers(choose=True):
    out = []
    for i, (name, size, wt, price, slug, ic) in enumerate(TIERS):
        btn = f'<a class="btn {"btn--purple" if i != 1 else "btn--cyan"} btn--block" href="pickup.html?tier={slug}">Choose pickup</a>' if choose else ""
        rng = " · ".join(x for x in (size, wt) if x) or "&nbsp;"
        out.append(f'''<li data-reveal class="tier{' tier--pop' if i == 1 else ''}">
      <span class="tier-icon">{I(ic)}</span>
      <h3>{name}</h3>
      <p class="tier-price" data-price="washFold.{i}.price">${price}</p>
      <p class="tier-range">{rng}</p>
      {btn}
    </li>''')
    return f'''<ul class="tiers tiers--4" role="list">
    {"".join(out)}
  </ul>
  <p class="tier-note">{EXTRA_NOTE}</p>'''

def price_tables():
    return '''<section class="d-section d-section--tint ptables" aria-labelledby="dc-title">
  <div class="wrap">
    <div class="ptable" data-reveal><h2 class="h-md" id="dc-title">Dry Cleaning Prices</h2><ul class="price-list" role="list" data-render="dryCleaning"></ul></div>
    <div class="ptable" data-reveal><h2 class="h-md" id="ir-title">Ironing Prices</h2><ul class="price-list" role="list" data-render="ironing"></ul></div>
    <p class="tier-note">Prices subject to change</p>
  </div>
</section>
'''

IND = [("ind-seniors","Seniors &amp; Supported Living","heart-handshake","Caregiver chatting with a group of seniors in a bright lounge"),
       ("ind-health","Health Care","stethoscope","Doctor listening to a young patient’s heartbeat"),
       ("ind-construction","Construction","hard-hat","Cranes over a high-rise building under construction at sunset"),
       ("ind-industrial","Industrial &amp; Manufacturing","factory","Aerial view of an industrial plant"),
       ("ind-nonprofits","Nonprofits &amp; Shelters","hand-heart","Volunteers serving food at a community kitchen"),
       ("ind-education","Educational Institutions","graduation-cap","Empty classroom with desks and a projector screen")]
IND += [("ind-spa","Salons, Spas &amp; Massage Studios","scissors","Massage table in a calm spa room, set with a folded teal towel"),
        ("ind-gym","Gyms &amp; Sports Teams","dumbbell","Spacious modern gym with weight racks and training equipment"),
        ("ind-hotel","Hotels &amp; Hospitality","hotel","Hotel bed with crisp white sheets and two folded white bathrobes"),
        ("ind-airbnb","Airbnb &amp; Short-Term Rentals","key-round","Bright modern rental bedroom with a neatly made bed"),
        ("ind-events","Events &amp; Catering","utensils-crossed","Banquet hall table dressed with a white tablecloth and floral centerpiece"),
        ("ind-realestate","Real Estate &amp; Property Managers","building-2","Apartment building with rows of balconies among green trees"),
        ("ind-offices","Offices &amp; Small Businesses","briefcase","Open-plan office with a team working at their desks")]
# Photo credits for the ind-* images: see CREDITS.md
QUOTE = "service-area.html?topic=business#contact-form"
def industries(full=True):
    n = len(IND)
    hid = "industries" if full else "industries-home"
    cards = "".join(f'<li class="biz-card biz-slide" role="group" aria-roledescription="slide" aria-label="{i+1} of {n}: {t}">{pic(k, alt, "(max-width: 600px) 82vw, (max-width: 1100px) 46vw, 30vw")}<h3><span class="biz-ic">{I(ic)}</span>{t}</h3></li>' for i, (k, t, ic, alt) in enumerate(IND))
    intro = ("Linens, uniforms, towels and bedding for organizations of every size, picked up and returned on a schedule that works for you." if full
             else "Swift Laundry also handles linens, uniforms and towels for businesses and organizations.")
    more = (f'<div class="biz-carousel" data-biz-carousel data-reveal role="region" aria-roledescription="carousel" aria-label="Industries we serve">'
            f'<div class="biz-viewport" tabindex="0" aria-label="Industries we serve. Use the left and right arrow keys to browse."><ul class="biz-track" role="list">{cards}</ul></div>'
            f'<div class="biz-ctrls"><button type="button" class="biz-arrow" data-prev aria-label="Previous industries">{I("chevron-left")}</button>'
            f'<div class="biz-prog" role="group" aria-label="Choose a set of industries"></div>'
            f'<span class="biz-count" aria-hidden="true"><b data-biz-cur>01</b> / {n:02d}</span>'
            f'<button type="button" class="biz-arrow" data-next aria-label="Next industries">{I("chevron-right")}</button></div>'
            f'<p class="visually-hidden" aria-live="polite" data-biz-live></p></div>')
    acts = (f'<a class="btn btn--cyan" href="{QUOTE}">Request a business quote {I("arrow-right")}</a>' +
            ("" if full else f'<a class="btn btn--ghost-light" href="services.html#industries">See all industries {I("arrow-right")}</a>'))
    return f'''<section class="biz" id="{hid}" aria-labelledby="{hid}-title">
  <div class="biz-panel has-blobs"><div class="blobs blobs--dark" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap">
    <div class="center"><span class="eyebrow eyebrow--light" data-reveal>{I("building-2")}For businesses &amp; organizations</span>
    <h2 data-reveal class="h-lg" id="{hid}-title">Industries We Serve</h2><p data-reveal class="biz-lead">{intro}</p></div>
    {more}
    <div class="biz-actions" data-reveal>{acts}</div>
    <p class="biz-note">Commercial pricing and pickup schedules are quoted per business. {tbc("Commercial rates to be confirmed")}</p>
  </div></div>
</section>'''

def card(icon, title, text):
    return f'<li data-reveal class="mini-card"><span class="icon-tile icon-tile--soft">{I(icon)}</span><div><h3>{title}</h3><p>{text}</p></div></li>'

def faq(q, a):
    return f'<details class="faq" data-faq><summary>{q}<span class="pm" aria-hidden="true">{I("plus")}</span></summary><div class="faq-body">{a}</div></details>'

def steps():
    S = [("calendar-check", "Book your pickup", "Request a pickup online or by phone. We confirm the time with you."),
         ("shopping-bag", "Leave your bag ready", "Place your laundry in any secure bag, ready at the agreed time and place."),
         ("washing-machine", "We wash &amp; fold", "We personally wash, dry and neatly fold your items at local laundromats."),
         ("truck", "Fresh laundry delivered", "We bring your clean, folded laundry back to your door.")]
    return '<ol class="steps" role="list">' + "".join(f'<li data-reveal class="step"><span class="step-icon">{I(i)}<span class="step-n">{n+1}</span></span><h3>{n+1}. {t}</h3><p>{d}</p></li>' for n, (i, t, d) in enumerate(S)) + "</ol>"

PAGES = {}
def page(path, title, desc, body, extra_head=""):
    PAGES[path] = head(path, title, desc, extra_head) + "\n" + header(path) + body + footer(path)

# ------------------------------------------------------------------ HOME
page("index.html", "Swift Laundry Services | Laundry pickup & delivery in Garfield Heights",
 "We pick up your laundry, wash, dry and neatly fold it, then bring it back to your door. Garfield Heights and selected Cleveland neighborhoods.",
 media_hero("Laundry pickup &amp; delivery · Garfield Heights", "Clean clothes.<br><span class=\"grad-text\">Delivered.</span>",
  "We pick up your laundry, wash, dry and neatly fold it, then bring it back to your door.", "hero-bag",
  "Smiling customer handing a purple Swift Laundry bag to a Swift team member at her front door",
  f'<div class="hero-actions"><a class="btn btn--purple" href="pickup.html">Schedule a Pickup {I("arrow-right")}</a><a class="btn btn--outline" href="services.html">See Prices</a></div>'
  f'<ul class="trust" role="list"><li>{I("calendar-sync")}One-time or recurring pickups</li><li>{I("heart")}Care preferences welcome</li></ul>')
 + f'''<div class="wrap zip-float">{zipcheck("zip-home")}</div>

<section class="d-section has-blobs" aria-labelledby="how-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
  <div class="wrap center"><span class="eyebrow" data-reveal>Personal service, from pickup to delivery</span><h2 data-reveal class="h-lg" id="how-title">Laundry day, handled.</h2></div>
  <div class="wrap">{steps()}</div>
  <div class="wrap center link-row"><a class="text-link" href="how-it-works.html">How it works {I("arrow-right")}</a><a class="text-link" href="services.html">Services &amp; pricing {I("arrow-right")}</a><a class="text-link" href="laundry-care.html">Laundry care {I("arrow-right")}</a></div>
</section>

<section class="d-section d-section--tint" aria-labelledby="price-title">
  <div class="wrap center"><span class="eyebrow" data-reveal>Wash, dry &amp; fold</span><h2 data-reveal class="h-lg" id="price-title">Simple options for everyday laundry</h2></div>
  <div class="wrap">{tiers()}</div>
</section>

{industries(False)}

<section class="d-section" aria-labelledby="fit-title">
  <div class="wrap center"><h2 data-reveal class="h-md" id="fit-title">Make it fit your routine</h2></div>
  <ul class="wrap mini-cards" role="list">
    {card("calendar-days", "Weekly pickups", "One-time, weekly or biweekly requests to keep laundry off your to-do list.")}
    {card("droplets", "Detergent preferences", "Tell us what works for you, such as regular or fragrance-free.")}
    {card("bed-double", "Bedding &amp; towels", "Machine-washable bedding or regular towel pickups: ask for a quote.")}
  </ul>
</section>

<section class="d-section" aria-labelledby="local-title">
  <div class="wrap split">
    <div data-reveal class="split-media">{pic("hands-fold", "Hands neatly folding a freshly washed light-blue shirt next to stacks of folded towels", "(max-width: 860px) 100vw, 45vw")}</div>
    <div>
      <h2 data-reveal class="h-md" id="local-title">Local care. Clear communication.</h2>
      <p data-reveal class="copy">We personally wash your laundry at local laundromats, then fold, package and return it to your door.</p>
      <a data-reveal class="text-link" href="about.html">Meet Swift Laundry {I("arrow-right")}</a>
      <div class="faq-stack">
        {faq("Where is my laundry washed?", "<p>We personally wash your laundry at local laundromats, then fold, package and return it to your door.</p>")}
        {faq("Do I need to be home?", "<p>Tell us your access instructions when you book (for example where to leave your bag). We confirm the pickup and return arrangement with you before your pickup.</p><p class=\"tbc-line\">" + tbc("Unattended-pickup rules to be confirmed") + "</p>")}
        {faq("When will my laundry be returned?", "<p>We confirm turnaround and your return delivery when booking.</p>")}
      </div>
      <a class="text-link" href="faq.html">All FAQs {I("arrow-right")}</a>
    </div>
  </div>
</section>
''' + re.search(r'(<section class="reviews has-blobs".*?</section>)', SRC_INDEX, re.S).group(1) + "\n\n" + cta("Get your laundry day back."))

# ------------------------------------------------------------------ SERVICES
page("services.html", "Services & Pricing | Swift Laundry Services",
 "Wash, dry and fold with pickup and return delivery. Single, Couple and Family Load options. Garfield Heights and selected Cleveland neighborhoods.",
 band("Fresh laundry. Clear options.", "Services &amp; Pricing", "Services &amp; Pricing", "Pickup, washing and drying, neat folding, packaging and return delivery.") + f'''
<section class="d-section has-blobs" aria-labelledby="inc-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
  <div class="wrap split split--rev">
    <div>
      <span class="eyebrow" data-reveal>Every order includes</span>
      <h2 data-reveal class="h-md" id="inc-title">Wash, dry &amp; fold, door to door</h2>
      <ul class="check-list" role="list">
        <li>{I("truck")}Pickup from your door</li><li>{I("washing-machine")}Washing and drying</li><li>{I("shirt")}Neat folding</li><li>{I("package")}Packaging</li><li>{I("house")}Return delivery</li>
      </ul>
      <p class="small-muted">Pickup and delivery fees, if any, are confirmed when booking. {tbc("Fees to be confirmed")}</p>
    </div>
    <div data-reveal class="split-media">{pic("pickup-stack", "Stacks of neatly folded towels and clothes beside a purple Swift Laundry bag", "(max-width: 860px) 100vw, 45vw")}</div>
  </div>
</section>
<section class="d-section d-section--tint" aria-labelledby="tiers-title">
  <div class="wrap center"><span class="eyebrow" data-reveal>Current options</span><h2 data-reveal class="h-lg" id="tiers-title">Choose your order size</h2></div>
  <div class="wrap">{tiers()}</div>
</section>
{price_tables()}{industries(True)}
<section class="d-section" aria-labelledby="freq-title">
  <div class="wrap center"><h2 data-reveal class="h-md" id="freq-title">How often?</h2><p class="copy lead" data-reveal>Request a one-time pickup, or ask for weekly or biweekly pickups. Availability is confirmed before booking.</p></div>
  <ul class="wrap mini-cards" role="list">
    {card("calendar", "One-time", "A single pickup whenever you need it.")}
    {card("calendar-sync", "Weekly", "A regular weekly pickup request.")}
    {card("calendar-range", "Biweekly", "A pickup every other week.")}
  </ul>
</section>
<section class="d-section" aria-labelledby="special-title">
  <div class="wrap">
    <div data-reveal class="quote-panel has-blobs"><div class="blobs blobs--dark" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
      <div><span class="eyebrow eyebrow--light">Special services</span><h2 class="h-md" id="special-title">Bedding &amp; towels: ask for a quote</h2>
      <p>Machine-washable bedding and regular towel pickups (including small-business towels) are quote requests, confirmed before booking. {tbc("Bedding &amp; towel prices to be confirmed")}</p></div>
      <a class="btn btn--cyan" href="service-area.html?topic=bedding#contact-form">Ask for a quote {I("arrow-right")}</a>
    </div>
  </div>
</section>
''' + cta("Ready for a lighter laundry day?"))

# ------------------------------------------------------------------ PICKUP
def field(id_, label, typ="text", req=True, auto="", extra="", span=False, opt=False, hint=""):
    o = ' <span class="optional">(optional)</span>' if opt else ""
    ctrl = (f'<textarea class="textarea" id="{id_}" name="{id_}"{" required" if req else ""} aria-describedby="{id_}-error" {extra}></textarea>' if typ == "textarea"
            else f'<input class="input" id="{id_}" name="{id_}" type="{typ}"{" required" if req else ""}{f" autocomplete={chr(34)}{auto}{chr(34)}" if auto else ""} aria-describedby="{id_}-error" {extra}>')
    h = f'<span class="field-hint">{hint}</span>' if hint else ""
    return f'<div class="field{" span-2" if span else ""}"><label for="{id_}">{label}{o}</label>{ctrl}{h}<span class="field-error" id="{id_}-error" aria-live="polite"></span></div>'

def choices(name, typ, items, legend, checked=0):
    c = "".join(f'<label class="choice"><input type="{typ}" name="{name}" value="{v}" data-label="{l}"{" checked" if i == checked else ""}><span>{l}</span></label>' for i, (v, l) in enumerate(items))
    return f'<fieldset class="fieldset span-2" data-summary-group data-summary-label="{legend}"><legend>{legend}</legend><div class="choice-grid">{c}</div></fieldset>'

LOAD_ROWS = "".join(f'''<div class="load-row" data-load="{k}" data-idx="{i}"><div class="load-info"><strong>{n}</strong><span>{c}</span></div><div class="load-price" data-price="washFold.{i}.price">{pr}</div><div class="qty" role="group" aria-label="Quantity of {n}"><button type="button" class="qty-btn" data-dec aria-label="Fewer {n}">−</button><input class="qty-in" type="number" min="0" max="20" value="0" inputmode="numeric" data-qty="{k}" aria-label="{n} quantity"><button type="button" class="qty-btn" data-inc aria-label="More {n}">+</button></div></div>'''
  for i,(k,n,c,pr) in enumerate([("single","Single Load","1/2 Full Laundry Bag · 1-10 lbs","$41.99"),("couple","Couple Load","1 Full Laundry Bag · 10-25 lbs","$56.99"),("family","Family Load","2 Full Laundry Bags · 25-40 lbs","$79.99"),("duvet","Duvet or blanket","One item","$41.99")]))

page("pickup.html", "Schedule a Pickup | Swift Laundry Services",
 "Request a laundry pickup in Garfield Heights and selected Cleveland neighborhoods. We’ll confirm availability, timing and fees with you.",
 band("Your next laundry day starts here.", "Schedule a Pickup", "Schedule a Pickup", "Request a pickup. We’ll confirm availability, timing and fees with you.") + f'''
<section class="form-section has-blobs" aria-labelledby="pickup-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap form-layout">
    <div data-reveal class="form-card">
      <h2 class="visually-hidden" id="pickup-title">Pickup request</h2>
      <ol class="stepper" role="list" data-stepper>
        <li class="is-current"><span class="sn">1</span><span class="sl">Your details</span></li>
        <li><span class="sn">2</span><span class="sl">Choose your load</span></li>
        <li><span class="sn">3</span><span class="sl">Pickup time</span></li>
        <li><span class="sn">4</span><span class="sl">Review &amp; total</span></li>
      </ol>
      <form data-pickup data-subject="Pickup request — Swift Laundry Services" action="#" method="post" novalidate>
        <fieldset class="step-panel" data-step="1">
          <legend class="step-head"><span class="icon-tile icon-tile--soft">{I("user-round")}</span><span><strong>Your details</strong><small>Let us know where to pick up your laundry.</small></span></legend>
          <div class="form-grid form-grid--2">
            {field("p-name", "Full name", auto="name", span=True)}
            {field("p-phone", "Mobile number", "tel", auto="tel", extra='inputmode="tel" pattern="[0-9\\(\\)+. \\-]{7,}" data-msg-pattern="Please enter a valid phone number."')}
            {field("p-email", "Email", "email", req=False, auto="email", opt=True)}
            {field("p-address", "Pickup address", auto="street-address", span=True, extra='placeholder="Street address, apartment / unit"')}
            {field("p-city", "City", auto="address-level2", extra='placeholder="e.g. Garfield Heights"')}
            {field("p-zip", "ZIP code", auto="postal-code", extra='inputmode="numeric" maxlength="5" pattern="[0-9]{5}" data-msg-pattern="Please enter a valid five-digit US ZIP code."')}
          </div>
          <div class="step-actions"><span></span><button class="btn btn--purple" type="button" data-next>Next: choose your load {I("arrow-right")}</button></div>
        </fieldset>
        <fieldset class="step-panel" data-step="2" hidden>
          <legend class="step-head"><span class="icon-tile icon-tile--soft">{I("shopping-bag")}</span><span><strong>Choose your load</strong><small>Pick a load size, then how many of each.</small></span></legend>
          <div class="load-list" data-loads role="group" aria-label="Load sizes">{LOAD_ROWS}</div>
          <p class="field-error load-error" data-load-error aria-live="polite"></p>
          <div class="load-sum" data-load-sum aria-live="polite"><span>Estimated total</span><strong data-load-total>$0.00</strong></div>
          <p class="small-muted">{EXTRA_NOTE}</p>
          <div class="form-grid form-grid--2" style="margin-top:18px">
            <div class="field span-2"><label for="p-detergent">Detergent preference <span class="optional">(optional)</span></label><select class="select" id="p-detergent" name="p-detergent"><option>Standard</option><option>Fragrance-free</option><option>I’ll describe it below</option></select><span class="field-error" aria-live="polite"></span></div>
          </div>
          <div hidden data-summary-label="Order"><input type="hidden" name="order-lines" data-order-lines></div>
          <div class="step-actions"><button class="btn btn--outline" type="button" data-back>{I("arrow-left")} Back</button><button class="btn btn--purple" type="button" data-next>Next: pickup time {I("arrow-right")}</button></div>
        </fieldset>
        <fieldset class="step-panel" data-step="3" hidden>
          <legend class="step-head"><span class="icon-tile icon-tile--soft">{I("calendar-days")}</span><span><strong>Pickup time</strong><small>Choose the day and a 1-hour pickup slot.</small></span></legend>
          <div class="form-grid form-grid--2">
            {field("p-date", "Pickup date", "date", span=True, extra="data-min-today", hint="A request, not a reserved slot. We confirm it with you.")}
            <fieldset class="fieldset span-2" data-summary-group data-summary-label="Pickup time" data-slots><legend>Pickup slot <span class="optional">(1 hour)</span></legend>
              <div class="slot-cols"><div class="slot-col"><h3 class="slot-h">{I("sunrise")}Morning</h3><div class="slot-grid" data-slots-morning></div></div><div class="slot-col"><h3 class="slot-h">{I("sun")}Afternoon</h3><div class="slot-grid" data-slots-afternoon></div></div></div>
              <span class="field-error" data-slot-error aria-live="polite"></span>
              <span class="field-hint">{tbc("Pickup hours to be confirmed")}</span>
            </fieldset>
            {choices("frequency", "radio", [("one-time", "One-time"), ("weekly", "Weekly"), ("biweekly", "Biweekly")], "Frequency")}
            {field("p-notes", "Access instructions or laundry preferences", "textarea", req=False, opt=True, span=True, extra='placeholder="e.g. door code, where to leave items, special care instructions"')}
            <div class="field span-2 check-field" data-summary-label="Contactless pickup"><label class="check"><input type="checkbox" name="p-contactless" value="Yes" data-label="Yes"><span>Contactless pickup requested</span></label></div>
          </div>
          <div class="step-actions"><button class="btn btn--outline" type="button" data-back>{I("arrow-left")} Back</button><button class="btn btn--purple" type="button" data-next>Next: review &amp; total {I("arrow-right")}</button></div>
        </fieldset>
        <fieldset class="step-panel" data-step="4" hidden>
          <legend class="step-head"><span class="icon-tile icon-tile--soft">{I("clipboard-check")}</span><span><strong>Review &amp; total</strong><small>Check your order and price, then confirm your request.</small></span></legend>
          <dl class="review-list" data-review></dl>
          <div class="total-card" aria-live="polite"><div><span>Estimated total</span><small>Final price is confirmed after we check your order at pickup. Extra weight is <span data-price="extraPerLb">$1.90</span>/lb.</small></div><strong data-review-total>$0.00</strong></div>
          <div hidden data-summary-label="Estimated total"><input type="hidden" name="order-total" data-order-total></div>
          <div class="field check-field" data-ack><label class="check"><input type="checkbox" name="p-ack" id="p-ack" required aria-describedby="p-ack-error"><span>I’ve reviewed the <a href="laundry-care.html" target="_blank" rel="noopener">laundry care policy</a> and <a href="service-terms.html" target="_blank" rel="noopener">service terms</a>.</span></label><span class="field-error" id="p-ack-error" aria-live="polite"></span></div>
          <p class="small-muted">Your details are only used to arrange this pickup. See our <a href="privacy.html" target="_blank" rel="noopener">privacy notice</a>.</p>
          <div class="step-actions"><button class="btn btn--outline" type="button" data-back>{I("arrow-left")} Back</button><button class="btn btn--purple" type="submit" data-submit>Confirm &amp; Request Pickup</button></div>
          <p class="small-muted center">No payment is taken online. You pay once your laundry has been checked and confirmed at pickup.</p>
        </fieldset>
        <div class="form-fail" data-fail hidden role="alert"><strong>We couldn’t send your request.</strong> Your pickup has not been booked. Please try again or call/text us on <a href="{TEL}" data-href="tel">{PHONE}</a>.</div>
      </form>
    </div>
    <aside class="aside-stack" aria-label="About your request">
      <div data-reveal class="aside-card">
        {pic("pickup-stack", "Folded laundry beside a purple Swift Laundry bag", "380px", cls="aside-photo")}
        <h3>What happens next?</h3>
        <ul class="next-list" role="list">
          <li>{I("clipboard-list")}<div><strong>We review your request</strong><span>We check the details and reach out to you.</span></div></li>
          <li>{I("calendar-check")}<div><strong>We confirm timing and fees</strong><span>We let you know if your requested date and time are available and share the fees with you.</span></div></li>
          <li>{I("scale")}<div><strong>We check your bag at pickup</strong><span>We look through your laundry to confirm the load size and your final price before we wash.</span></div></li>
          <li>{I("phone-call")}<div><strong>We call when it’s ready</strong><span>Once your laundry is done, we call you to arrange the drop-off time.</span></div></li>
        </ul>
      </div>
      <div data-reveal class="aside-card">
        <h3>Pricing reminder</h3>
        <ul class="mini-prices" role="list"><li><span>Single Load</span><strong data-price="washFold.0.price">$41.99</strong><small>1-10 lbs</small></li><li><span>Couple Load</span><strong data-price="washFold.1.price">$56.99</strong><small>10-25 lbs</small></li><li><span>Family Load</span><strong data-price="washFold.2.price">$79.99</strong><small>25-40 lbs</small></li><li><span>Duvet or blanket</span><strong data-price="washFold.3.price">$41.99</strong></li></ul>
        <p class="small-muted">{EXTRA_NOTE}</p>
      </div>
      <a data-reveal class="aside-card help-card" href="{TEL}" data-href="tel"><span class="icon-tile">{I("phone")}</span><span><strong>Need help booking?</strong>Call or text <span data-bind="phone">{PHONE}</span></span></a>
    </aside>
  </div>
</section>
''')

# ------------------------------------------------------------------ REQUEST RECEIVED
page("request-received.html", "Request received | Swift Laundry Services", "Thanks! Your pickup request is received.",
 f'''<section class="d-section has-blobs received" aria-labelledby="rr-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap narrow">
    <div data-reveal class="form-card center">
      <span class="ok-badge">{I("circle-check-big")}</span>
      <h1 class="h-lg" id="rr-title">Thanks! Your request is received.</h1>
      <p class="copy">Your pickup is not confirmed yet. We’ll contact you to confirm availability, timing and fees.</p>
      <p class="small-muted" data-rr-mail hidden>Your email app opened with your request filled in. If you haven’t pressed <strong>Send</strong> yet, please do, or call or text us.</p>
      <div class="rr-summary" data-rr-summary hidden><h2 class="h-sm">Your request</h2><dl class="review-list" data-rr-list></dl></div>
      <p class="pill-note">{I("wallet")}No payment has been taken.</p>
      <div class="hero-actions center-actions"><a class="btn btn--purple" href="index.html">{I("house")}Back to Home</a><a class="btn btn--outline" href="{TEL}" data-href="tel">{I("phone")}Call us</a><a class="btn btn--outline" href="{SMS}" data-href="sms">{I("message-square")}Text us</a></div>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ ABOUT
page("about.html", "About | Swift Laundry Services", "Personal care for everyday laundry: a local pickup and delivery service built around your routine.",
 media_hero("About Swift Laundry", "Personal care for everyday laundry.", "A local pickup and delivery service built around your routine.", "about-handoff",
  "Swift team member handing a purple Swift Laundry bag to a customer at her door",
  f'<div class="hero-actions"><a class="btn btn--purple" href="pickup.html">Schedule a Pickup {I("arrow-right")}</a><a class="btn btn--outline" href="how-it-works.html">How it works</a></div>') + f'''
<section class="d-section" aria-labelledby="sw-title">
  <div class="wrap center"><h2 data-reveal class="h-lg" id="sw-title">How Swift works</h2><p class="copy lead" data-reveal>We pick up your laundry, personally wash it at local laundromats, then fold, package and return it to your door.</p></div>
  <ul class="wrap mini-cards" role="list">
    {card("truck", "Convenient pickups", "We pick up your laundry at your door, on a schedule that works for you.")}
    {card("layers", "Care preferences welcome", "Tell us how you like your laundry, and we’ll do our best to follow your requests.")}
    {card("message-circle-more", "Clear communication", "We’ll keep you updated about your pickup, washing and delivery.")}
  </ul>
</section>
<section class="band-wide" aria-hidden="true"><div class="wrap"><div data-reveal class="wide-photo">{pic("fold-strip", "", "(max-width: 1320px) 100vw, 1320px")}</div></div></section>
<section class="d-section" aria-labelledby="story-title">
  <div class="wrap narrow">
    <div data-reveal class="placeholder-card">
      <span class="eyebrow">Our story</span>
      <h2 class="h-md" id="story-title">Meet the owner</h2>
      <p>{tbc("Owner to supply")} The owner’s story, in her own words, goes here: who she is, why she started Swift Laundry, and how she cares for each order. We won’t publish credentials, team size or years of experience until she supplies them, and real photos are used only with permission.</p>
    </div>
  </div>
</section>
<section class="d-section d-section--tint" aria-labelledby="pref-title">
  <div class="wrap center"><h2 data-reveal class="h-md" id="pref-title">Tell us how you like your laundry</h2></div>
  <ul class="wrap mini-cards" role="list">
    {card("droplets", "Detergent preferences", "Tell us what works for you, such as regular or fragrance-free.")}
    {card("wind", "Drying preferences", "Let us know if you prefer regular or low heat drying.")}
    {card("shirt", "Special garment instructions", "Share any special-care items or instructions, and we’ll do our best to accommodate.")}
  </ul>
  <p class="wrap center small-muted">We’ll confirm which requests we can accommodate before washing. Full details on our <a href="laundry-care.html">Laundry Care page</a>.</p>
</section>
<section class="d-section" aria-labelledby="first-title">
  <div class="wrap split split--top">
    <div>
      <h2 data-reveal class="h-md" id="first-title">Before your first pickup</h2>
      <div class="faq-stack">
        {faq("Where is my laundry washed?", "<p>We personally wash your laundry at local laundromats.</p>")}
        {faq("Which items can I send?", "<p>Start with everyday machine-washable clothing. Ask us about bedding or items needing special care.</p>")}
        {faq("When will my laundry be returned?", "<p>We confirm turnaround and your return delivery when booking.</p>")}
      </div>
      <a class="text-link" href="faq.html">More questions {I("arrow-right")}</a>
    </div>
    <div data-reveal class="aside-card">
      <h3>Getting your bag ready</h3>
      <ul class="next-list" role="list">
        <li>{I("shopping-bag")}<div><strong>Bag your laundry securely.</strong></div></li>
        <li>{I("key-round")}<div><strong>Share access instructions.</strong></div></li>
        <li>{I("tag")}<div><strong>Tell us about special-care items before pickup.</strong></div></li>
      </ul>
    </div>
  </div>
</section>
''' + cta("Laundry help, right at your door."))

# ------------------------------------------------------------------ SERVICE AREA & CONTACT
SOC = f'''<li><a data-reveal class="contact-card" href="https://www.instagram.com/swiftlaundryservicess/" data-social="instagram" rel="noopener" target="_blank"><span class="icon-tile">{IG}</span><div><h3>Instagram</h3><span class="value">@swiftlaundryservicess</span></div></a></li>
    <li><a data-reveal class="contact-card" href="#" data-social="facebook" rel="noopener" target="_blank"><span class="icon-tile">{FB}</span><div><h3>Facebook</h3><span class="value">Swift Laundry</span><span class="meta">Garfield Heights, OH</span></div></a></li>'''
page("service-area.html", "Service Area & Contact | Swift Laundry Services", "Check whether we serve your ZIP code, or call, text or message Swift Laundry Services.",
 band("Let’s make laundry easier.", "Service Area &amp; Contact", "Service Area &amp; Contact", "Garfield Heights and selected Cleveland neighborhoods.") + f'''
<section class="d-section has-blobs" aria-labelledby="area-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
  <div class="wrap split split--top">
    <div>
      <h2 data-reveal class="h-md" id="area-title">Check your ZIP code</h2>
      <p data-reveal class="copy">We serve Garfield Heights and selected Cleveland neighborhoods. {tbc("Exact ZIP list to be confirmed")}</p>
      {zipcheck("zip-area")}
    </div>
    <div data-reveal class="map-card">
      <iframe data-map data-lenis-prevent src="https://maps.google.com/maps?q=Garfield%20Heights%2C%20OH&amp;z=12&amp;output=embed" title="Map of Garfield Heights, Ohio and nearby Cleveland neighborhoods" width="800" height="600" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <p class="map-cap">{I("info")}Map is for orientation only, not an exact coverage boundary.</p>
    </div>
  </div>
</section>
<section class="d-section d-section--tint" aria-labelledby="reach-title">
  <div class="wrap center"><h2 data-reveal class="h-md" id="reach-title">Reach us directly</h2></div>
  <ul class="wrap contact-cards contact-cards--5" role="list">
    <li><a data-reveal class="contact-card" href="{TEL}" data-href="tel"><span class="icon-tile">{I("phone")}</span><div><h3>Call</h3><span class="value" data-bind="phone">{PHONE}</span></div></a></li>
    <li><a data-reveal class="contact-card" href="{SMS}" data-href="sms"><span class="icon-tile">{I("message-square")}</span><div><h3>Text</h3><span class="value" data-bind="phone">{PHONE}</span></div></a></li>
    <li><a data-reveal class="contact-card" href="mailto:swiftlaundryservicess@gmail.com" data-href="email"><span class="icon-tile">{I("mail")}</span><div><h3>Email</h3><span class="value" data-bind="email">swiftlaundryservicess@gmail.com</span></div></a></li>
    {SOC}
  </ul>
</section>
<section class="form-section" id="contact-form" aria-labelledby="cf-title">
  <div class="wrap narrow">
    <div data-reveal class="form-card">
      <h2 class="h-sm" id="cf-title">Send us a message</h2>
      <p class="small-muted" style="margin-bottom:18px">Questions, a bedding quote, or business towels? We’ll contact you using the details you provide.</p>
      <form data-contact data-subject="Website inquiry — Swift Laundry Services" action="#" method="post" novalidate>
        <div class="form-grid form-grid--2">
          {field("c-name", "Name", auto="name")}
          {field("c-reach", "Phone or email", auto="email", extra='data-phone-or-email data-msg-pattern="Please enter a phone number or email address."')}
          <div class="field span-2"><label for="c-type">Inquiry type</label><select class="select" id="c-type" name="c-type" data-prefill="topic" required aria-describedby="c-type-error"><option value="">Choose one…</option><option value="household">Household laundry</option><option value="bedding">Bedding quote</option><option value="towels">Business towels</option><option value="business">Business / commercial quote</option><option value="other">Other</option></select><span class="field-error" id="c-type-error" aria-live="polite"></span></div>
          {field("c-msg", "Message", "textarea", span=True)}
        </div>
        <div class="step-actions"><span class="small-muted">Prefer to talk? <a href="{TEL}" data-href="tel">Call</a> or <a href="{SMS}" data-href="sms">text</a> us.</span><button class="btn btn--purple" type="submit" data-submit>Send inquiry</button></div>
        <div class="form-result" data-contact-ok hidden role="status" tabindex="-1"><h3>{I("check")}Thanks, your inquiry has been received.</h3><p>Your email app should have opened with your message filled in. Please press send. We’ll contact you using the details provided.</p></div>
        <div class="form-fail" data-fail hidden role="alert"><strong>We couldn’t send your message.</strong> Please try again or call/text us on <a href="{TEL}" data-href="tel">{PHONE}</a>.</div>
      </form>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ HOW IT WORKS
def stage(n, icon, title, text, extra=""):
    return f'<li data-reveal class="stage"><span class="stage-n">{n}</span><div class="stage-body"><span class="icon-tile icon-tile--soft">{I(icon)}</span><h3>{title}</h3><p>{text}</p>{extra}</div></li>'
page("how-it-works.html", "How It Works | Swift Laundry Services", "Laundry day made simple: request a pickup, bag your laundry, we weigh and confirm, then wash, dry, fold and return.",
 band("Laundry day made simple.", "How It Works", "How It Works", "Four simple stages, from request to your door.") + f'''
<section class="d-section has-blobs" aria-labelledby="st-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap narrow"><h2 class="visually-hidden" id="st-title">The four stages</h2>
  <ol class="stages" role="list">
    {stage(1, "calendar-check", "Request a pickup", "Request a pickup online or by phone. We review your request and confirm availability, timing and fees with you.", f'<a class="text-link" href="pickup.html">Schedule a Pickup {I("arrow-right")}</a>')}
    {stage(2, "shopping-bag", "Bag and prepare after confirmation", "Once your pickup is confirmed, bag your laundry securely and leave it ready using the access instructions you agreed with us.", f'<a class="text-link" href="laundry-care.html#before">Getting your bag ready {I("arrow-right")}</a>')}
    {stage(3, "scale", "Weigh and confirm your total", "We weigh your laundry and confirm the total with you before washing.")}
    {stage(4, "washing-machine", "Wash, dry, fold and return", "We personally wash and dry your laundry at local laundromats, neatly fold and package it, then return it within the agreed return window.")}
  </ol>
  <div data-reveal class="notice">{I("info")}<p>Pickup and return windows are agreed with you when booking. Turnaround is confirmed when booking. {tbc("Pickup hours &amp; turnaround to be confirmed")}</p></div>
  </div>
</section>
<section class="d-section d-section--tint" aria-labelledby="hp-title">
  <div class="wrap center"><h2 data-reveal class="h-md" id="hp-title">Prices at a glance</h2></div>
  <div class="wrap">{tiers()}</div>
</section>
''' + cta("Ready when you are."))

# ------------------------------------------------------------------ FAQ
NEEDS = ["Is my order washed separately?", "What if no one is home at pickup?", "Which items can’t you accept?", "How do you handle stains?", "How do I cancel or change a pickup?", "What happens if a pickup is missed?", "What if an item is lost or damaged?", "When do I pay?"]
G = [("pickup", "truck", "Pickup &amp; delivery", [
       ("Do you serve my area?", '<p>We serve Garfield Heights and selected Cleveland neighborhoods. Check your ZIP code on our <a href="service-area.html">Service Area page</a>, or call or text <a href="tel:+17144027530" data-href="tel">(714) 402-7530</a>.</p>'),
       ("Can I set up recurring pickups?", "<p>Yes. You can request one-time, weekly or biweekly pickups. Availability is confirmed before booking.</p>"),
       ("When will my laundry be returned?", "<p>We confirm turnaround and your return delivery when booking.</p>")]),
     ("pricing", "tag", "Pricing", [
       ("How much does it cost?", '<p>Single Load (1-10 lbs) <strong data-price="washFold.0.price">$41.99</strong>, Couple Load (10-25 lbs) <strong data-price="washFold.1.price">$56.99</strong>, Family Load (25-40 lbs) <strong data-price="washFold.2.price">$79.99</strong>, Duvet or blanket <strong data-price="washFold.3.price">$41.99</strong>. See <a href="services.html">Services &amp; Pricing</a>.</p>'),
       ("How is the weight measured?", "<p>We weigh your laundry and confirm the weight and total with you before washing.</p>"),
       ("Are there extra fees?", "<p>Pickup fees and turnaround are confirmed when booking. " + EXTRA_NOTE + ".</p><p class=\"tbc-line\">" + tbc("Fees to be confirmed") + "</p>")]),
     ("care", "shirt", "Laundry care", [
       ("Where is my laundry washed?", "<p>We personally wash your laundry at local laundromats, then fold, package and return it to your door.</p>"),
       ("Can I choose my detergent?", "<p>Yes. Tell us your detergent and drying preferences when you book. We confirm which requests we can accommodate before washing.</p>"),
       ("Do you wash bedding or towels?", '<p>Machine-washable bedding and regular towel pickups are quote requests. <a href="service-area.html?topic=bedding#contact-form">Ask for a quote</a>.</p>')])]
groups = "".join(f'''<section class="faq-group" data-faq-group aria-labelledby="g-{k}"><h2 class="faq-group-title" id="g-{k}"><span class="icon-tile icon-tile--soft">{I(ic)}</span>{t}</h2><div class="faq-stack">{"".join(faq(q, a) for q, a in qs)}</div></section>''' for k, ic, t, qs in G)
page("faq.html", "FAQs | Swift Laundry Services", "Answers about pickup and delivery, pricing and laundry care at Swift Laundry Services.",
 band("Frequently asked questions", "FAQs", "FAQs", "Pickup &amp; delivery, pricing and laundry care.") + f'''
<section class="d-section has-blobs" aria-label="Questions"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
  <div class="wrap narrow">
    <div class="faq-tools">
      <label class="search" for="faq-q">{I("search")}<span class="visually-hidden">Search questions</span><input class="input" id="faq-q" type="search" placeholder="Search questions" data-faq-search autocomplete="off"></label>
      <div class="faq-chips" role="group" aria-label="Jump to a category"><a href="#g-pickup">Pickup &amp; delivery</a><a href="#g-pricing">Pricing</a><a href="#g-care">Laundry care</a></div>
    </div>
    {groups}
    <div class="faq-empty" data-faq-empty hidden role="status"><p><strong>No matching questions.</strong> Ask us directly: <a href="service-area.html#contact-form">send a message</a> or call/text <a href="tel:+17144027530" data-href="tel">(714) 402-7530</a>.</p></div>
    <div data-reveal class="placeholder-card">
      <h2 class="h-sm">{tbc("Awaiting owner’s answers")} More questions coming</h2>
      <p>These answers will be added once the owner confirms them. They are not shown as open questions until then:</p>
      <ul class="dash-list">{"".join(f"<li>{q}</li>" for q in NEEDS)}</ul>
    </div>
  </div>
</section>
''' + cta("Still have a question?", "Contact us", "service-area.html#contact-form"))

# ------------------------------------------------------------------ LAUNDRY CARE
def care_sec(id_, icon, title, inner):
    return f'<section class="care-sec" id="{id_}" aria-labelledby="{id_}-t"><h2 class="h-sm" id="{id_}-t"><span class="icon-tile icon-tile--soft">{I(icon)}</span>{title}</h2>{inner}</section>'
page("laundry-care.html", "Laundry Care | Swift Laundry Services", "How to prepare your laundry for pickup, the preferences we accept and how we handle special items.",
 band("Care starts with clear instructions.", "Laundry Care", "Laundry Care Information", "How to prepare your laundry, and how we care for it.") + f'''
<section class="d-section has-blobs" aria-label="Laundry care information"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span></div>
  <div class="wrap care-layout">
    <nav class="jump" aria-label="On this page"><p class="jump-title">On this page</p><ul role="list"><li><a href="#before">Before pickup</a></li><li><a href="#prefs">Preferences</a></li><li><a href="#special">Special items</a></li><li><a href="#stains">Stains &amp; results</a></li><li><a href="#policies">Policies to come</a></li></ul></nav>
    <div class="care-main">
      {care_sec("before", "shopping-bag", "Before pickup", f'<ul class="check-list" role="list"><li>{I("check")}Empty all pockets.</li><li>{I("check")}Bag your laundry securely.</li><li>{I("check")}Flag any items with special care labels.</li><li>{I("check")}Tell us about special items before pickup.</li></ul>')}
      {care_sec("prefs", "droplets", "Preferences", "<p>Tell us your detergent preference (such as regular or fragrance-free), drying preference (regular or low heat) and any special garment instructions when you book. We confirm which requests we can accommodate before washing.</p>")}
      {care_sec("special", "bed-double", "Special items", '<p>Start with everyday machine-washable clothing. Machine-washable bedding and regular towel pickups are quote requests, subject to acceptance. <a href="service-area.html?topic=bedding#contact-form">Ask for a quote</a>.</p>')}
      {care_sec("stains", "sparkles", "Stains &amp; results", "<p>We take care with every load, but we can’t promise complete stain removal, sterilization or allergy-safe results.</p>")}
      {care_sec("policies", "file-text", "Policies to come", f'<div class="placeholder-card"><p>{tbc("Owner to supply")} The owner will confirm these before launch: whether each order is washed separately, items we can’t accept, how stains are handled, and how to report a lost or damaged item.</p></div>')}
    </div>
  </div>
</section>
''' + cta("Ready for your first pickup?"))

# ------------------------------------------------------------------ PRIVACY & TERMS
def textpage(path, title, crumb, desc, intro, secs):
    toc = "".join(f'<li><a href="#s{i+1}">{t}</a></li>' for i, (t, _) in enumerate(secs))
    body = "".join(f'<section id="s{i+1}" aria-labelledby="s{i+1}-t"><h2 id="s{i+1}-t">{i+1}. {t}</h2>{c}</section>' for i, (t, c) in enumerate(secs))
    page(path, f"{title} | Swift Laundry Services", desc, band(title, crumb) + f'''
<section class="d-section" aria-label="{title}">
  <div class="wrap text-page">
    <div class="tp-meta"><p><strong>Effective date:</strong> {tbc("Owner to set")}</p><div class="placeholder-card"><p>{tbc("Draft")} This is a layout draft for review. The owner must supply and approve the final wording before launch.</p></div><p class="copy">{intro}</p></div>
    <nav class="tp-toc" aria-label="Contents"><p class="jump-title">Contents</p><ol>{toc}</ol></nav>
    <div class="tp-body">{body}</div>
  </div>
</section>
''')
P_ = lambda t: f'<p class="ph">{tbc("Owner to supply")} {t}</p>'
textpage("privacy.html", "Privacy Notice", "Privacy", "How Swift Laundry Services handles the information you share with us.",
 "This notice explains what information you share with Swift Laundry Services when you use this website, and how it is used.",
 [("Information you share", "<p>When you request a pickup or send an inquiry, you may give us your name, phone number, email address, pickup address, city and ZIP code, preferred dates and times, and laundry or access instructions.</p>"),
  ("How it is used", "<p>We use these details to review your request, contact you, and arrange your pickup and return delivery.</p>"),
  ("How the forms work today", "<p>On this version of the site, the pickup and contact forms don’t store anything on our website. Submitting a form opens your own email app with your details filled in, addressed to <a href=\"mailto:swiftlaundryservicess@gmail.com\" data-href=\"email\">swiftlaundryservicess@gmail.com</a>. Nothing is sent until you press send.</p>"),
  ("Service providers", "<p>This website is hosted on GitHub Pages. The service-area map is provided by Google Maps and loads only on the Service Area page.</p>" + P_("Form, messaging and record-keeping providers once a booking system is in place.")),
  ("Analytics and cookies", "<p>This demo does not use analytics or advertising cookies.</p>" + P_("Update if analytics are added.")),
  ("Keeping and accessing your information", P_("Who can access records, how long they are kept, and how to request a change or deletion.")),
  ("Marketing", "<p>We don’t sign you up for marketing when you request a pickup.</p>" + P_("Any separate marketing choices.")),
  ("Contact", '<p>Questions about this notice: call or text <a href="tel:+17144027530" data-href="tel">(714) 402-7530</a>.</p>')])
textpage("service-terms.html", "Service Terms", "Service Terms", "The terms for Swift Laundry Services pickup, wash, dry, fold and delivery.",
 "These terms will describe how pickup requests are accepted and how your laundry is handled.",
 [("Requests and acceptance", "<p>Submitting a request does not book a pickup. We review each request and confirm availability, timing and fees with you before your pickup.</p>" + P_("Full order-acceptance process.")),
  ("Coverage and timing", "<p>We serve Garfield Heights and selected Cleveland neighborhoods. Pickup windows and turnaround are confirmed when booking.</p>" + P_("Confirmed ZIP list, pickup hours and capacity.")),
  ("Weight and pricing", '<p>Current options: Single Load 1-10 lbs, Couple Load 10-25 lbs, Family Load 25-40 lbs, Duvet or blanket. See <a href="services.html">Services &amp; Pricing</a>. Weight and total are confirmed before washing.</p>' + P_("Rounding, minimum order, delivery fees and tax.")),
  ("Payment", P_("When and how payment is taken.")),
  ("Accepted and excluded items", '<p>See <a href="laundry-care.html">Laundry Care</a> for how to prepare your laundry.</p>' + P_("Items that can’t be accepted.")),
  ("Cancellations and missed pickups", P_("How to cancel or change a pickup, and what happens if a pickup is missed.")),
  ("Recurring pickups", P_("How to change, skip or stop weekly or biweekly pickups.")),
  ("Lost or damaged items", P_("How to report a concern and how it is resolved.")),
  ("Contact", '<p>Call or text <a href="tel:+17144027530" data-href="tel">(714) 402-7530</a>, or email <a href="mailto:swiftlaundryservicess@gmail.com" data-href="email">swiftlaundryservicess@gmail.com</a>.</p>')])

# ------------------------------------------------------------------ 404
B404 = '''
<base href="/website-demo/">
<script>
  /* 404.html can be served at any depth, so point relative URLs at the site root.
     On GitHub Pages the site lives under /website-demo/; on a custom domain it lives at /. */
  (function () {
    var PROJECT_BASE = "/website-demo/";
    var root = location.pathname.indexOf(PROJECT_BASE) === 0 ? PROJECT_BASE : "/";
    document.querySelector("base").href = root;
  })();
</script>'''
page("404.html", "Page not found | Swift Laundry Services", "This page has wandered off.",
 f'''<section class="d-section has-blobs received" aria-labelledby="nf-title"><div class="blobs" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
  <div class="wrap narrow"><div class="form-card center">
    <span class="ok-badge ok-badge--soft">{I("search-x")}</span>
    <h1 class="h-lg" id="nf-title">This page has wandered off.</h1>
    <p class="copy">Let’s get you back to fresh laundry.</p>
    <div class="hero-actions center-actions"><a class="btn btn--purple" href="index.html">{I("house")}Home</a><a class="btn btn--cyan" href="pickup.html">Schedule a Pickup</a><a class="btn btn--outline" href="service-area.html">Contact</a></div>
  </div></div>
</section>
''', B404)

# ------------------------------------------------------------------ redirects for old routes
REDIR = {"order.html": "pickup.html", "contact.html": "service-area.html", "why-choose-us.html": "about.html", "login.html": "index.html"}
for old, new in REDIR.items():
    PAGES[old] = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<!-- Designed & developed by Innocent Christo. © 2026 Innocent Christo. Built for Swift Laundry Services. -->
<meta name="author" content="Innocent Christo">
<link rel="author" href="humans.txt">
<title>Moved | Swift Laundry Services</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{new}">
<meta http-equiv="refresh" content="0; url={new}">
<script>location.replace("{new}" + location.search + location.hash);</script>
</head><body><p>This page has moved to <a href="{new}">{new}</a>.</p></body></html>
'''

for p, s in PAGES.items():
    open(os.path.join(ROOT, p), "w").write(s)
json.dump(_ic, open(os.path.join(ROOT, "_build/icons.json"), "w"), indent=0)
print("wrote", len(PAGES), "pages")
