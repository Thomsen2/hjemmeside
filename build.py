# -*- coding: utf-8 -*-
"""Build static HTML from data/produkter.json. Run: python build.py"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "produkter.json").read_text(encoding="utf-8"))
PRODUCTS = DATA["products"]
SECTIONS = DATA["sections"]
ASSET_CSS = "/styles.css?v=186"
ASSET_JS = "/script.js?v=55"

BORDKORT_OG_IMAGE = "https://pub-a65460f11bff4b4c9a65a6943613a5ef.r2.dev/cute%20chat.png"
BORDKORT_OG_ALT = "Personlige bordkort i træ på borddækning"


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def filter_products(pred):
    return [p for p in PRODUCTS if pred(p)]


def form_label_for(product: dict) -> str:
    label = (product.get("form_label") or "").strip()
    if label and label != "Skriv dine ønsker til skiltet her":
        return label
    section = product.get("section", "")
    if section == "gavekort":
        return "Indtast tekst til gavekortet"
    if section.startswith("bordkort"):
        return "Indtast navn"
    if section == "fodselstavle":
        return "Indtast navn, dato og vægt/længde"
    return "Indtast Navne, Datoer (2 stk), samt år"


def form_placeholder_for(product: dict) -> str:
    section = product.get("section", "")
    if section.startswith("bordkort"):
        return "Indtast alle de navne du ønsker"
    return "Skriv dine ønsker til skiltet her..."


def render_card(product: dict, first: bool = False) -> str:
    pid = product["id"]
    section = product.get("section", "")
    bordkort_cls = " product-card--bordkort" if section.startswith("bordkort") else ""
    zoom_cls = "" if section.startswith("gavekort") else " product-card--zoom"
    imgs = []
    for i, img in enumerate(product.get("images") or []):
        cls = "product-card__img sign-photo"
        extra = ""
        if img.get("hidden") or "product-card__img--alt" in (img.get("alt") or "") and i > 0:
            cls += " product-card__img--alt"
            extra = " hidden"
        if img.get("hidden"):
            cls += " product-card__img--alt"
            extra = " hidden"
        lazy = "" if first and i == 0 else ' loading="lazy"'
        imgs.append(
            f'<img{lazy} src="{esc(img["src"])}" alt="{esc(img.get("alt") or product["title"])}" class="{cls}"{extra}>'
        )
    media = "\n                    ".join(imgs) or ""
    mounting = ""
    if product.get("mounting"):
        mounting = """
                        <label class="checkbox-label">
                            <input type="checkbox" name="mounting" value="20" class="mounting-toggle">
                            Tilføj monteringskit +20 kr (indeholder 2 klæbepuder + 2 strips)
                        </label>"""
    size = f'<p class="product-card__size">{esc(product["size"])}</p>' if product.get("size") else ""
    return f"""            <article class="product-card product-card--{esc(pid)}{bordkort_cls}{zoom_cls}" data-beskrivelse="{esc(product.get('description') or product['title'])}">
                <div class="product-card__media sign-preview">
                    {media}
                </div>
                <h3 class="product-card__title">{esc(product["title"])}</h3>
                {size}
                <p class="product-card__price">{esc(product["price"])}</p>
                <details class="product-card__order">
                    <summary>Bestil</summary>
                    <form class="sign-form">
                        <div class="form-group">
                            <label for="besked_{esc(pid)}">{esc(form_label_for(product))}</label>
                            <textarea id="besked_{esc(pid)}" name="besked_{esc(pid)}" rows="3" placeholder="{esc(form_placeholder_for(product))}"></textarea>
                        </div>
                        <label class="checkbox-label">
                            <input type="checkbox" name="pickup" value="Dragør" class="pickup-toggle">
                            Afhentning i Dragør (gratis)
                        </label>
                        <div class="pickup-fields">
                            <div class="form-group">
                                <label>Email til afhentningsinfo</label>
                                <input type="email" class="pickup-email" placeholder="din@mail.dk">
                            </div>
                        </div>
                        <label class="checkbox-label">
                            <input type="checkbox" name="shipping" value="55" class="shipping-toggle">
                            Skal sendes (55 kr)
                        </label>{mounting}
                        <div class="shipping-fields">
                            <div class="form-group">
                                <label for="navn_{esc(pid)}">Navn</label>
                                <input type="text" id="navn_{esc(pid)}" name="navn_{esc(pid)}" placeholder="Dit fulde navn">
                            </div>
                            <div class="form-group">
                                <label for="adresse_{esc(pid)}">Adresse</label>
                                <input type="text" id="adresse_{esc(pid)}" name="adresse_{esc(pid)}" placeholder="Din adresse">
                            </div>
                            <div class="form-group">
                                <label for="mail_{esc(pid)}">Mail</label>
                                <input type="email" id="mail_{esc(pid)}" name="mail_{esc(pid)}" placeholder="din@mail.dk">
                            </div>
                            <div class="form-group">
                                <label for="mobil_{esc(pid)}">Mobil nr</label>
                                <input type="tel" id="mobil_{esc(pid)}" name="mobil_{esc(pid)}" placeholder="+45 12 34 56 78">
                            </div>
                        </div>
                        <button type="submit" class="btn-submit">Send forespørgsel</button>
                    </form>
                </details>
            </article>"""


HEADING_MAP = {
    "birkefiner": "Æresportskilt – hjerte i birkefiner",
    "egetrae": "Æresportskilt – hjerte i egetræ",
    "version1": "Æresportskilt – hjerte i bejdset valnød",
    "version2": "Æresportskilt – hjerte i amerikansk valnød",
    "vaabenskjold": "Æresportskilt – våbenskjold i birkefiner",
    "egetrae_v2": "Æresportskilt – våbenskjold i egetræ",
    "version1_v2": "Æresportskilt – våbenskjold i bejdset valnød",
    "bryllup": "Skilte og dekoration til bryllup",
    "gavekort": "Personligt gavekort i træ",
    "bordkort_navne": "Personlige navne bordkort i træ",
    "bordkort_speciale": "Specielle bordkort i træ",
    "fodselstavle": "Fødselstavle",
    "andre_skilte": "Andre skilte",
    "velkomst_skilt": "Velkomstskilt",
}


def render_grids(products: list[dict], group=True, hide_headings: set[str] | None = None) -> str:
    if not products:
        return '<p class="shop-mount__status">Ingen modeller på denne side endnu.</p>'
    if not group:
        cards = [render_card(p, first=(i == 0)) for i, p in enumerate(products)]
        return '<section class="builder"><div class="container"><div class="product-grid">\n' + "\n".join(cards) + "\n</div></div></section>"
    by_section: dict[str, list] = {}
    order = []
    for p in products:
        sid = p["section"]
        if sid not in by_section:
            by_section[sid] = []
            order.append(sid)
        by_section[sid].append(p)
    blocks = []
    first_page = True
    for sid in order:
        items = by_section[sid]
        h2 = HEADING_MAP.get(sid) or SECTIONS.get(sid, {}).get("h2") or sid
        note = SECTIONS.get(sid, {}).get("note") or ""
        note_html = f'<p class="wood-note">{esc(note)}</p>' if note else ""
        intro = SECTIONS.get(sid, {}).get("intro") or []
        intro_html = "".join(f"<p class=\"section-desc\">{esc(t)}</p>" for t in intro)
        cards = [render_card(p, first=(first_page and i == 0)) for i, p in enumerate(items)]
        first_page = False
        anchor = {"bordkort_navne": "navne", "bordkort_speciale": "speciale"}.get(sid)
        id_attr = f' id="{anchor}"' if anchor else ""
        h2_html = ""
        if not (hide_headings and sid in hide_headings):
            h2_html = f'<h2 class="no-divider">{esc(h2)}</h2>\n            '
        blocks.append(
            f"""    <section class="builder"{id_attr}>
        <div class="container">
            {h2_html}{note_html}
            {intro_html}
            <div class="product-grid">
{chr(10).join(cards)}
            </div>
        </div>
    </section>"""
        )
    return "\n".join(blocks)


def nav_html(active: str) -> str:
    def cls(slug, kind="link"):
        base = "nav-link" if kind == "link" else "nav-sub-link"
        return f'{base} active' if active == slug else base

    return f"""    <nav class="main-nav" id="mainNav">
        <div class="container nav-bar">
            <button class="nav-toggle" id="navToggle" aria-label="Åbn menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <div class="nav-links" id="navLinks">
                <a href="/#forside" class="nav-link">
                    <span class="nav-icon nav-icon--heart" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><path d="M12 21s-7-4.4-9.5-8.2C.7 9.8 2.2 6 5.6 6c1.9 0 3.2 1.1 4 2.2C10.4 7.1 11.7 6 13.6 6c3.4 0 4.9 3.8 3.1 6.8C19 16.6 12 21 12 21z"/></svg>
                    </span>
                    Forside
                </a>
                <div class="nav-dropdown">
                    <a href="/#hjerte" class="{cls('hjerte')}">
                        <span class="nav-icon nav-icon--heart" aria-hidden="true">
                            <svg viewBox="0 0 24 24"><path d="M12 21s-7-4.4-9.5-8.2C.7 9.8 2.2 6 5.6 6c1.9 0 3.2 1.1 4 2.2C10.4 7.1 11.7 6 13.6 6c3.4 0 4.9 3.8 3.1 6.8C19 16.6 12 21 12 21z"/></svg>
                            <span class="heart-bubbles" aria-hidden="true">
                                <span class="hb">♥</span>
                                <span class="hb">♥</span>
                                <span class="hb">♥</span>
                                <span class="hb">♥</span>
                                <span class="hb">♥</span>
                            </span>
                        </span>
                        Hjerte
                    </a>
                </div>
                <div class="nav-dropdown">
                    <a href="/#vaabenskjold" class="{cls('vaabenskjold')}">
                        <span class="nav-icon nav-icon--shield" aria-hidden="true">
                            <svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg>
                            <span class="shield-bubbles" aria-hidden="true">
                                <span class="sb"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg></span>
                                <span class="sb"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg></span>
                                <span class="sb"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg></span>
                                <span class="sb"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg></span>
                                <span class="sb"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/></svg></span>
                            </span>
                        </span>
                        Våbenskjold
                    </a>
                </div>
                <a href="/gavekort/" class="{cls('gavekort')}">
                    <span class="nav-icon nav-icon--gift" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><rect x="3" y="10" width="18" height="11" rx="1.5"/><path d="M3 14h18M12 10v11M8.5 7.5C8.5 5.6 9.6 4 12 4s3.5 1.6 3.5 3.5c0 1.4-1 2.5-3.5 2.5S8.5 8.9 8.5 7.5z"/></svg>
                        <span class="gift-bubbles" aria-hidden="true">
                            <span class="gb">$</span>
                            <span class="gb">$</span>
                            <span class="gb">$</span>
                            <span class="gb">$</span>
                            <span class="gb">$</span>
                        </span>
                    </span>
                    Gavekort i træ
                </a>
                <a href="https://bordkort.dk/" class="{cls('bordkort')}">
                    <span class="nav-icon nav-icon--card" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h8M8 14h5"/></svg>
                        <span class="name-bubbles" aria-hidden="true">
                            <span class="nb">Mia</span>
                            <span class="nb">Leo</span>
                            <span class="nb">Ida</span>
                            <span class="nb">Bo</span>
                            <span class="nb">Ava</span>
                        </span>
                    </span>
                    Bordkort
                </a>
                <a href="/fodselstavle/" class="{cls('fodselstavle')}">
                    <span class="nav-icon nav-icon--pram" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg>
                        <span class="pram-bubbles" aria-hidden="true">
                            <span class="pb"><svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg></span>
                            <span class="pb"><svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg></span>
                            <span class="pb"><svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg></span>
                            <span class="pb"><svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg></span>
                            <span class="pb"><svg viewBox="0 0 24 24"><path d="M7 18.5a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zm13 0a1.75 1.75 0 1 1-3.5 0 1.75 1.75 0 0 1 3.5 0zM18.5 16H6.2l-.7-3.2h11.3c1.1 0 1.9.7 2.1 1.6l.6 1.6zM8.5 4.5h4.2c1.8 0 3.3 1.3 3.6 3.1l.5 2.2H7.8l.7-5.3zM8.5 4.5V3h3"/></svg></span>
                        </span>
                    </span>
                    Fødselstavle
                </a>
                <a href="/andre-skilte/" class="{cls('andre-skilte')}">
                    <span class="nav-icon nav-icon--spark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/></svg></span>
                    Andre skilte
                </a>
                <a href="/#bryllup" class="{cls('bryllup') if active in ('bryllup','kobberbryllup','soelvbryllup','guldbryllup') else 'nav-link'}">
                    <span class="nav-icon nav-icon--rings" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg>
                        <span class="ring-bubbles" aria-hidden="true">
                            <span class="rb"><svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg></span>
                            <span class="rb"><svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg></span>
                            <span class="rb"><svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg></span>
                            <span class="rb"><svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg></span>
                            <span class="rb"><svg viewBox="0 0 24 24"><circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="11" r="5.5"/></svg></span>
                        </span>
                    </span>
                    Bryllup
                </a>
                <a href="/#eget-design" class="{cls('eget-design')}">
                    <span class="nav-icon nav-icon--spark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3zM18.5 15.5l.8 2.7 2.7.8-2.7.8-.8 2.7-.8-2.7-2.7-.8 2.7-.8.8-2.7zM5.5 16.5l.6 2 2 .6-2 .6-.6 2-.6-2-2-.6 2-.6.6-2z"/></svg></span>
                    Få lavet dit helt eget design
                </a>
                <a href="/#faq" class="nav-link">
                    <span class="nav-icon nav-icon--faq" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1.4.9-1.4 1.7V14M12 17h.01"/></svg></span>
                    Ofte stillede spørgsmål
                </a>
            </div>
        </div>
    </nav>"""


def nav_html_bordkort(active: str, prefix: str = "") -> str:
    def cls(slug):
        return "nav-link active" if active == slug else "nav-link"

    p = prefix

    return f"""    <nav class="main-nav" id="mainNav">
        <div class="container nav-bar">
            <button class="nav-toggle" id="navToggle" aria-label="Åbn menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <div class="nav-links" id="navLinks">
                <a href="{p}#forside" class="{cls('home')}">
                    <span class="nav-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><path d="M4 10.5L12 4l8 6.5V19a1.5 1.5 0 0 1-1.5 1.5H15v-5.5H9V20.5H5.5A1.5 1.5 0 0 1 4 19V10.5z"/></svg>
                    </span>
                    Forside
                </a>
                <a href="{p}navne/" class="{cls('navne')}">
                    <span class="nav-icon nav-icon--card" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h8M8 14h5"/></svg>
                        <span class="name-bubbles" aria-hidden="true">
                            <span class="nb">Mia</span>
                            <span class="nb">Leo</span>
                            <span class="nb">Ida</span>
                            <span class="nb">Bo</span>
                            <span class="nb">Ava</span>
                        </span>
                    </span>
                    Navne bordkort
                </a>
                <a href="{p}speciale/" class="{cls('speciale')}">
                    <span class="nav-icon nav-icon--spark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/></svg></span>
                    Specielle bordkort
                </a>
                <a href="{p}#eget-design" class="{cls('eget-design')}">
                    <span class="nav-icon nav-icon--spark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3zM18.5 15.5l.8 2.7 2.7.8-2.7.8-.8 2.7-.8-2.7-2.7-.8 2.7-.8.8-2.7zM5.5 16.5l.6 2 2 .6-2 .6-.6 2-.6-2-2-.6 2-.6.6-2z"/></svg></span>
                    Få lavet dit eget design
                </a>
                <a href="{p}#faq" class="nav-link">
                    <span class="nav-icon nav-icon--faq" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1.4.9-1.4 1.7V14M12 17h.01"/></svg></span>
                    Ofte stillede spørgsmål
                </a>
                <a href="https://æresportskilt.dk/" class="nav-link">
                    <span class="nav-icon nav-icon--heart" aria-hidden="true">
                        <svg viewBox="0 0 24 24"><path d="M12 21s-7-4.4-9.5-8.2C.7 9.8 2.2 6 5.6 6c1.9 0 3.2 1.1 4 2.2C10.4 7.1 11.7 6 13.6 6c3.4 0 4.9 3.8 3.1 6.8C19 16.6 12 21 12 21z"/></svg>
                    </span>
                    Æresportskilte
                </a>
            </div>
        </div>
    </nav>"""


def faq_block(items: list[tuple[str, str]]) -> str:
    parts = ['    <section class="faq-section" id="faq">', '        <div class="container">', "            <h2>Ofte stillede spørgsmål</h2>"]
    for q, a in items:
        parts.append(f"            <h3>{esc(q)}</h3>")
        parts.append(f"            <p>{esc(a)}</p>")
    parts += ["        </div>", "    </section>"]
    return "\n".join(parts)


def faq_jsonld(items: list[tuple[str, str]]) -> str:
    entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in items
    ]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False, indent=2)


def local_business_bordkort(*, url: str = "https://bordkort.dk/", page_id: str = "https://bordkort.dk/#business") -> dict:
    return {
        "@type": "LocalBusiness",
        "@id": page_id,
        "name": "Bordkort.dk",
        "url": url,
        "image": BORDKORT_OG_IMAGE,
        "email": "Thomsen2@gmail.com",
        "founder": {"@type": "Person", "name": "Bo Thomsen"},
        "address": {
            "@type": "PostalAddress",
            "postalCode": "2791",
            "addressLocality": "Dragør",
            "addressRegion": "Hovedstaden",
            "addressCountry": "DK",
        },
        "areaServed": {"@type": "Country", "name": "Danmark"},
        "description": "Personlige bordkort i træ til bryllup og fest. Håndlavet i Dragør på Amager.",
    }


def bordkort_jsonld(faq: list[tuple[str, str]]) -> str:
    faq_entity = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }
    graph = [faq_entity, local_business_bordkort()]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


CONTACT_EMAIL = "Thomsen2@gmail.com"

CONTACT_FOOTER = f"""            <p class="footer-contact">Bo Thomsen &middot; 2791 Dragør &middot; <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>"""

CONTACT_ABOUT = f"""            <p class="contact-detail">Bo Thomsen</p>
            <p class="contact-detail">2791 Dragør</p>
            <p class="contact-detail">Mail: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>"""

ABOUT_AESPORT = "Hos Æresportskilt.dk skaber vi håndlavede æresportskilte med kærlighed til træhåndværket. Hvert skilt udføres i nøje udvalgte træsorter, hvor kvalitet og detaljer er i fokus. Vi tilbyder personlig service og skræddersyede løsninger, så dit skilt bliver unikt og holder i generationer."

ABOUT_BORDKORT = "Hos Bordkort.dk laver vi personlige bordkort i træ til bryllup, konfirmation og fest. Hvert bordkort fremstilles på bestilling med fokus på kvalitet og detaljer. Vi tilbyder personlig service – og laver også æresportskilte på Æresportskilt.dk."

def about_section(about_text: str) -> str:
    return f"""    <section class="about">
        <div class="container">
            <p class="about-text">{about_text}</p>
            <h2 style="margin-top:2rem">Kontakt</h2>
            <p>Har du spørgsmål? Kontakt os på:</p>
{CONTACT_ABOUT}
        </div>
    </section>"""

FOOTER = f"""    <footer>
        <div class="container">
{CONTACT_FOOTER}
            <p>&copy; 2026 Æresportskilt.dk. Alle rettigheder forbeholdes. &mdash; <a href="/hjerte/">Hjerte</a> &mdash; <a href="/vaabenskjold/">Våbenskjold</a> &mdash; <a href="/egetrae/">Egetræ</a> &mdash; <a href="/bryllup/">Bryllup</a> &mdash; <a href="/gavekort/">Gavekort</a> &mdash; <a href="https://bordkort.dk/">Bordkort</a> &mdash; <a href="/om-os/">Om os</a></p>
        </div>
    </footer>"""

BORDKORT_FOOTER = f"""    <footer>
        <div class="container">
{CONTACT_FOOTER}
            <p>&copy; 2026 Bordkort.dk. Alle rettigheder forbeholdes. &mdash; <a href="/navne/">Navne bordkort</a> &mdash; <a href="/speciale/">Specielle bordkort</a> &mdash; <a href="https://æresportskilt.dk/">Æresportskilte</a> &mdash; <a href="/om-os/">Om os</a></p>
        </div>
    </footer>"""

NETLIFY_FORM = """    <form name="bestilling" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" hidden aria-hidden="true">
        <input type="text" name="bot-field">
        <input type="hidden" name="form-name" value="bestilling">
        <input type="text" name="subject">
        <input type="text" name="Produkt">
        <input type="text" name="Beskrivelse">
        <input type="text" name="Besked">
        <input type="url" name="Billede-eksempel">
        <input type="text" name="Afhentning">
        <input type="text" name="Forsendelse">
        <input type="text" name="Monteringskit">
        <input type="email" name="Afhentnings-email">
        <input type="text" name="Navn">
        <input type="text" name="Adresse">
        <input type="email" name="Mail">
        <input type="tel" name="Mobil">
    </form>"""


def page_shell(*, slug, title, description, h1, canonical, kicker, crumb, intro_h2, intro, products_html, faq, extra_body="", site_name="Æresportskilt.dk", kicker_brand="Æresportskilt.dk", nav=None, footer=None, favicon="/favicon.svg", intro_before=False, og_image="", og_image_alt="", jsonld=""):
    url = canonical
    breadcrumb = ""
    if crumb:
        home_href = "/" if site_name == "Bordkort.dk" else "/#forside"
        breadcrumb = f'<p class="page-breadcrumb"><a href="{home_href}">Forside</a> / {esc(crumb)}</p>'
    kicker_home = "/" if site_name == "Bordkort.dk" else "/#forside"
    kicker_html = f'<p class="site-kicker"><a href="{kicker_home}">{esc(kicker_brand)}</a></p>' if kicker else ""
    h1_html = f"<h1>{h1}</h1>" if slug == "home" else f"<h1>{esc(h1)}</h1>"
    nav_block = nav(slug) if nav else nav_html(slug)
    footer_block = footer if footer is not None else FOOTER
    intro_html = ""
    if intro:
        paras = "\n".join(f"            <p>{esc(p)}</p>" for p in intro)
        heading = f"            <h2>{esc(intro_h2)}</h2>\n" if intro_h2 else ""
        intro_html = f"""    <section class="intro">
        <div class="container">
{heading}{paras}
        </div>
    </section>"""
    faq_html = faq_block(faq) if faq else ""
    schemas = []
    if jsonld:
        schemas.append(f'    <script type="application/ld+json">\n{jsonld}\n    </script>')
    elif faq:
        schemas.append(f'    <script type="application/ld+json">\n{faq_jsonld(faq)}\n    </script>')
    schema_html = "\n".join(schemas)
    og_html = ""
    if og_image:
        og_html = f"""    <meta property="og:image" content="{esc(og_image)}">
    <meta property="og:image:alt" content="{esc(og_image_alt or title)}">"""
    icon_links = ""
    if "bordkort" in favicon:
        icon_links = """    <link rel="icon" href="/favicon-bordkort.ico?v=3" sizes="any">
    <link rel="icon" href="/favicon-bordkort.png?v=3" type="image/png" sizes="128x128">
    <link rel="apple-touch-icon" href="/apple-touch-icon-bordkort.png?v=3">"""
    else:
        icon_type = "image/png" if favicon.endswith(".png") else "image/svg+xml"
        icon_links = f'    <link rel="icon" href="{esc(favicon)}" type="{icon_type}">'
    if intro_before:
        body_middle = f"{intro_html}\n{products_html}\n{faq_html}"
    else:
        body_middle = f"{products_html}\n{intro_html}\n{faq_html}"
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{esc(description)}">
    <title>{esc(title)}</title>
    <link rel="canonical" href="{esc(url)}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="da_DK">
    <meta property="og:site_name" content="{esc(site_name)}">
    <meta property="og:url" content="{esc(url)}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
{og_html}
{icon_links}
    <link rel="stylesheet" href="{ASSET_CSS}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{schema_html}
</head>
<body>
    <header class="site-header">
        <div class="container">
            {kicker_html}
            {h1_html}
        </div>
    </header>
{nav_block}
    {breadcrumb}
{body_middle}{extra_body}
{footer_block}
{NETLIFY_FORM}
    <script src="{ASSET_JS}"></script>
    <div class="lightbox" id="lightbox" style="display:none">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-img" id="lightboxImg" src="" alt="">
    </div>
    <div id="imgOverlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:9999;justify-content:center;align-items:center;cursor:pointer;" onclick="this.style.display='none'"><img id="imgOverlayImg" src="" alt="" style="max-width:90vw;max-height:90vh;object-fit:contain;"></div>
</body>
</html>
"""


AESPORT_FAQ = [
    ("Hvad er et æresportskilt?", "Et æresportskilt er et personligt skilt i træ, der hænges op som en del af æresporten – typisk ved indgangen til festen. Det viser navne og dato og gør porten mere personlig."),
    ("Hvad kan der stå på et æresportskilt?", "I kan typisk få navne, datoer og år på skiltet efter jeres ønsker. På forespørgselsformularerne skriver I den tekst, I gerne vil have på skiltet."),
    ("Hvordan bestiller jeg et æresportskilt?", "Vælg en model, udfyld formularen og send forespørgslen. I kan vælge afhentning i Dragør eller forsendelse."),
]

BORDKORT_FAQ = [
    ("Hvad er et bordkort i træ?", "Et bordkort i træ er et lille, personligt skilt med gæstens navn – eller et motiv – som står ved kuverten. Det gør borddækningen mere personlig og er et minde, gæsterne kan tage med hjem."),
    ("Hvad koster bordkort?", "Klassiske navnebordkort starter ved 10 kr. stykket. Specielle motiver koster typisk 12 kr. stykket. Prisen står ved hver model."),
    ("Kan I lave et særligt motiv?", "Ja. Har I et tema til festen – sport, dyr, gaming eller noget helt andet – så skriv det i formularen under eget design, så laver vi et forslag."),
    ("Hvordan bestiller jeg?", "Vælg en model, skriv navnene og send forespørgslen. I kan afhente i Dragør eller få bordkortene sendt."),
]


def write_page(rel_path: str, content: str):
    dest = ROOT / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print("wrote", rel_path)


def main():
    hearts = filter_products(lambda p: p["form"] == "hjerte" and not p["section"].startswith("bordkort"))
    shields = filter_products(lambda p: p["form"] == "vaabenskjold")
    oak = filter_products(lambda p: p["wood"] == "egetrae" and p["form"] in ("hjerte", "vaabenskjold"))
    signs = filter_products(lambda p: p["form"] in ("hjerte", "vaabenskjold"))
    wedding = filter_products(lambda p: p["section"] == "bryllup" or (p["form"] == "hjerte" and p["wood"] == "egetrae"))
    copper = filter_products(lambda p: "kobber" in (p["title"] + p["description"]).lower() or p["form"] in ("hjerte", "vaabenskjold"))
    # keep copper page focused: prefer named copper + mixed signs but not 40 items
    copper_named = filter_products(lambda p: "kobber" in (p["title"] + p["description"]).lower())
    if copper_named:
        copper = copper_named + [p for p in shields[:2] + hearts[:3] if p not in copper_named]

    pages = [
        dict(slug="home", path="index.html", title="Æresportskilt i træ – hjerte og våbenskjold til bryllup",
             description="Personligt æresportskilt i træ til bryllup, kobberbryllup, sølvbryllup og guldbryllup. Håndlavet i Dragør. Hjerte eller våbenskjold fra 199 kr.",
             h1='<a href="/">Æresportskilt til bryllup og fest</a>', canonical="https://æresportskilt.dk/",
             kicker=False, crumb="", intro_h2="Personlige æresportskilte i træ",
             intro=["Hos Æresportskilt.dk laver vi personlige æresportskilte i træ til bryllup, kobberbryllup, sølvbryllup og guldbryllup.",
                    "Vælg mellem hjerte eller våbenskjold i birkefiner, egetræ eller valnød, og få et personligt æresportskilt med jeres navne og dato.",
                    "Alle skilte fremstilles på bestilling. Se også undersiderne til hjerte, våbenskjold og de enkelte anledninger."],
             products=hearts, faq=AESPORT_FAQ),
        dict(slug="hjerte", path="hjerte/index.html", title="Hjerte til æresport i træ – personligt æresportskilt",
             description="Bestil et hjerte til æresport i træ. Personligt æresportskilt med navne og dato i birkefiner, egetræ eller valnød. Håndlavet i Dragør fra 199 kr.",
             h1="Hjerte til æresport i træ", canonical="https://æresportskilt.dk/hjerte/", kicker=True, crumb="Hjerte",
             intro_h2="Personligt æresportskilt som hjerte",
             intro=["Et hjerte til æresport er det klassiske valg til bryllup og andre kærlighedsanledninger.",
                    "Vi laver hjerterne i birkefiner, egetræ og valnød. Alle fremstilles på bestilling med jeres navne og dato."],
             products=hearts, faq=[("Hvad koster et hjerte til æresport?", "Et hjerte i birkefiner starter ved 199 kr. Prisen står ved hver model."),
                                  ("Hvilken størrelse har hjertet?", "De fleste hjerter måler 31 x 33 cm.")]),
        dict(slug="vaabenskjold", path="vaabenskjold/index.html", title="Våbenskjold til æresport – æresportskilt i træ",
             description="Bestil et våbenskjold til æresport i træ. Klassisk æresportskilt med navne og dato i birkefiner, egetræ eller valnød.",
             h1="Våbenskjold til æresport", canonical="https://æresportskilt.dk/vaabenskjold/", kicker=True, crumb="Våbenskjold",
             intro_h2="Personligt æresportskilt som våbenskjold",
             intro=["Et våbenskjold giver et klassisk udtryk på æresporten og passer godt til sølv- og guldbryllup.",
                    "Skiltet graveres med navne, dato og eventuelt årstal."],
             products=shields, faq=[("Hvornår vælger man våbenskjold?", "Ofte til sølv- og guldbryllup, eller når I vil have et mere højtideligt udtryk end hjertet.")]),
        dict(slug="egetrae", path="egetrae/index.html", title="Æresportskilt i egetræ – hjerte og våbenskjold",
             description="Æresportskilt i egetræ med personlig gravering. Hjerte eller våbenskjold til bryllup og mærkedage. Fra 249 kr.",
             h1="Æresportskilt i egetræ", canonical="https://æresportskilt.dk/egetrae/", kicker=True, crumb="Egetræ",
             intro_h2="Hjerte og våbenskjold i egetræ",
             intro=["Egetræ giver skiltet et varmt, nordisk udtryk. I kan vælge hjerte eller våbenskjold."],
             products=oak, faq=[("Hvad koster egetræ?", "De fleste modeller i egetræ koster 249 kr.")]),
        dict(slug="bryllup", path="bryllup/index.html", title="Æresportskilt til bryllup – hjerte og velkomstskilt",
             description="Personligt æresportskilt til bryllup i træ. Hjerte, våbenskjold og velkomstskilt med brudeparrets navne og dato.",
             h1="Æresportskilt til bryllup", canonical="https://æresportskilt.dk/bryllup/", kicker=True, crumb="Bryllup",
             intro_h2="Skilt til æresporten på bryllupsdagen",
             intro=["Et æresportskilt til bryllup byder gæsterne velkommen med brudeparrets navne og dato."],
             products=wedding, faq=[("Hvilket skilt er mest populært til bryllup?", "Hjerteformet skilt i træ med navne og dato.")]),
        dict(slug="soelvbryllup", path="soelvbryllup/index.html", title="Æresportskilt til sølvbryllup – 25 års dag i træ",
             description="Æresportskilt til sølvbryllup med navne, dato og 25 år. Hjerte eller våbenskjold i træ, håndlavet i Dragør.",
             h1="Æresportskilt til sølvbryllup", canonical="https://æresportskilt.dk/soelvbryllup/", kicker=True, crumb="Sølvbryllup",
             intro_h2="Personligt skilt til 25 års dagen",
             intro=["På skiltet står typisk parrets navne, dato og 25 år. Mange vælger våbenskjold til sølvbryllup."],
             products=signs, faq=[("Hvad skal der stå på skiltet?", "Oftest navne, dato og 25 år eller ordet sølvbryllup.")]),
        dict(slug="kobberbryllup", path="kobberbryllup/index.html", title="Æresportskilt til kobberbryllup – 12,5 års dag",
             description="Æresportskilt til kobberbryllup i træ. Personligt hjerte eller våbenskjold med navne og 12,5 år.",
             h1="Æresportskilt til kobberbryllup", canonical="https://æresportskilt.dk/kobberbryllup/", kicker=True, crumb="Kobberbryllup",
             intro_h2="Skilt til æresporten ved kobberbryllup",
             intro=["Kobberbryllup fejres efter 12½ år. I kan vælge hjerte eller våbenskjold – også halvt skjold."],
             products=copper, faq=[("Hvad skriver man på skiltet?", "Navne, dato og gerne 12,5 år eller kobberbryllup.")]),
        dict(slug="guldbryllup", path="guldbryllup/index.html", title="Æresportskilt til guldbryllup – 50 års dag i træ",
             description="Æresportskilt til guldbryllup med navne, dato og 50 år. Klassisk våbenskjold eller hjerte i træ.",
             h1="Æresportskilt til guldbryllup", canonical="https://æresportskilt.dk/guldbryllup/", kicker=True, crumb="Guldbryllup",
             intro_h2="Personligt skilt til 50 års dagen",
             intro=["Til guldbryllup vælger mange et våbenskjold i egetræ, gerne med navne, dato og 50 år."],
             products=signs, faq=[("Kan der stå 50 år på skiltet?", "Ja. I skriver selv teksten i formularen.")]),
        dict(slug="gavekort", path="gavekort/index.html", title="Gavekort i træ – personlig pengegave",
             description="Personligt gavekort i træ til bryllup, konfirmation og fødselsdag. Håndlavet i Dragør.",
             h1="Gavekort i træ", canonical="https://æresportskilt.dk/gavekort/", kicker=True, crumb="Gavekort",
             intro_h2="",
             intro=[],
             products=filter_products(lambda p: p["section"] == "gavekort"), faq=[]),
        dict(slug="bordkort", path="bordkort/index.html", title="Bordkort i træ – navne og specielle designs",
             description="Personlige bordkort i træ med navn eller tema. Navne bordkort og specielle bordkort til festen.",
             h1="Bordkort i træ", canonical="https://æresportskilt.dk/bordkort/", kicker=True, crumb="Bordkort",
             intro_h2="Personlige bordkort",
             intro=["Vælg mellem klassiske navnebordkort og specielle motiver i træ."],
             products=filter_products(lambda p: p["section"].startswith("bordkort")), faq=[]),
        dict(slug="fodselstavle", path="fodselstavle/index.html", title="Fødselstavle i træ",
             description="Fødselstavle i træ – en tidløs gave til den nyfødte og familien.",
             h1="Fødselstavle", canonical="https://æresportskilt.dk/fodselstavle/", kicker=True, crumb="Fødselstavle",
             intro_h2="",
             intro=[],
             products=filter_products(lambda p: p["section"] == "fodselstavle"), faq=[]),
        dict(slug="andre-skilte", path="andre-skilte/index.html", title="Andre skilte i træ",
             description="Skræddersyede skilte i træ – kaffebar, velkomst og andre designs efter ønske.",
             h1="Andre skilte", canonical="https://æresportskilt.dk/andre-skilte/", kicker=True, crumb="Andre skilte",
             intro_h2="",
             intro=[],
             products=filter_products(lambda p: p["section"] == "andre_skilte"), faq=[]),
        dict(slug="velkomst-skilt", path="velkomst-skilt/index.html", title="Velkomstskilt i træ",
             description="Velkomstskilt i træ til festen. Personlig tekst, håndlavet i Dragør.",
             h1="Velkomstskilt", canonical="https://æresportskilt.dk/velkomst-skilt/", kicker=True, crumb="Velkomstskilt",
             intro_h2="Velkomstskilt i træ",
             intro=["Et velkomstskilt byder gæsterne velkommen ved indgangen."],
             products=filter_products(lambda p: p["section"] == "velkomst_skilt"), faq=[]),
    ]

    for p in pages:
        if p["slug"] == "home":
            continue
        html_out = page_shell(
            slug=p["slug"],
            title=p["title"],
            description=p["description"],
            h1=p["h1"],
            canonical=p["canonical"],
            kicker=p["kicker"],
            crumb=p["crumb"],
            intro_h2=p["intro_h2"],
            intro=p["intro"],
            intro_before=p.get("intro_before", False),
            products_html=render_grids(p["products"], hide_headings=p.get("hide_product_headings")),
            faq=p["faq"],
        )
        write_page(p["path"], html_out)

    eget = page_shell(
        slug="eget-design",
        title="Få lavet dit helt eget design i træ",
        description="Specialdesignet skilt i træ efter dine ønsker. Send en forespørgsel, så laver vi et forslag og en pris.",
        h1="Få lavet dit helt eget design",
        canonical="https://æresportskilt.dk/eget-design/",
        kicker=True,
        crumb="Eget design",
        intro_h2="Unikt skilt efter dine ønsker",
        intro=["Har du en idé til et unikt skilt i træ? Fortæl os form, tekst, anledning og træsort – så laver vi et designforslag."],
        products_html="",
        faq=[],
        extra_body="""    <section class="builder">
        <div class="container">
            <div class="form-area" style="max-width:520px;margin:0 auto">
                <form class="sign-form">
                    <div class="form-group">
                        <label for="besked_eget_design">Beskriv dit design / ønsker</label>
                        <textarea id="besked_eget_design" name="besked_eget_design" rows="5" placeholder="Beskriv gerne form, tekst, størrelse, træsort og anledning..."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="navn_eget_design">Navn</label>
                        <input type="text" id="navn_eget_design" name="navn_eget_design" placeholder="Dit fulde navn">
                    </div>
                    <div class="form-group">
                        <label for="mail_eget_design">Mail</label>
                        <input type="email" id="mail_eget_design" name="mail_eget_design" placeholder="din@mail.dk">
                    </div>
                    <div class="form-group">
                        <label for="mobil_eget_design">Mobil nr</label>
                        <input type="tel" id="mobil_eget_design" name="mobil_eget_design" placeholder="+45 12 34 56 78">
                    </div>
                    <button type="submit" class="btn-submit">Send forespørgsel</button>
                </form>
            </div>
        </div>
    </section>""",
    )
    write_page("eget-design/index.html", eget)

    omos = page_shell(
        slug="om-os",
        title="Om os – Æresportskilt.dk",
        description="Hos Æresportskilt.dk laver vi håndlavede æresportskilte i træ. Personlig service og afhentning i Dragør.",
        h1="Om os",
        canonical="https://æresportskilt.dk/om-os/",
        kicker=True,
        crumb="Om os",
        intro_h2="Kontakt",
        intro=[],
        products_html="",
        faq=[],
        extra_body=about_section(ABOUT_AESPORT),
    )
    write_page("om-os/index.html", omos)

    bordkort_omos = page_shell(
        slug="om-os",
        title="Om os – Bordkort.dk | Dragør",
        description="Hos Bordkort.dk laver vi personlige bordkort i træ i Dragør på Amager. Personlig service og afhentning efter aftale.",
        h1="Om os",
        canonical="https://bordkort.dk/om-os/",
        kicker=True,
        kicker_brand="Bordkort.dk",
        crumb="Om os",
        intro_h2="",
        intro=[],
        products_html="",
        faq=[],
        extra_body=about_section(ABOUT_BORDKORT),
        site_name="Bordkort.dk",
        nav=lambda slug: nav_html_bordkort(slug, prefix="../"),
        footer=BORDKORT_FOOTER,
        favicon="/favicon-bordkort.ico?v=3",
        og_image=BORDKORT_OG_IMAGE,
        og_image_alt=BORDKORT_OG_ALT,
        jsonld=json.dumps(
            {"@context": "https://schema.org", "@graph": [local_business_bordkort(url="https://bordkort.dk/om-os/", page_id="https://bordkort.dk/om-os/#business")]},
            ensure_ascii=False,
            indent=2,
        ),
    )
    write_page("bordkort-site/om-os/index.html", bordkort_omos)

    bordkort_home = page_shell(
        slug="home",
        title="Bordkort i træ til bryllup | Håndlavet i Dragør",
        description="Personlige bordkort i træ til bryllup, konfirmation og fest på Amager. Navnebordkort fra 10 kr. og specielle motiver. Afhentning i Dragør.",
        h1='<a href="#forside">Bordkort i træ til fest og bryllup</a>',
        canonical="https://bordkort.dk/",
        kicker=False,
        crumb="",
        intro_h2="Personlige bordkort i træ",
        intro=[
            "Hos Bordkort.dk laver vi personlige bordkort i træ til bryllup, konfirmation, fødselsdag og fest — håndlavet i Dragør på Amager.",
            "Vælg klassiske navnebordkort eller specielle motiver – fodbold, heste, gaming og meget mere. Hvert bordkort fremstilles på bestilling.",
            "Gratis afhentning i Dragør efter aftale, eller forsendelse i hele Danmark for 55kr. Se også æresportskilte på Æresportskilt.dk, hvis I skal have skilt til æresporten.",
        ],
        products_html="",
        faq=BORDKORT_FAQ,
        extra_body="""    <section class="builder" id="eget-design">
        <div class="container">
            <h2 class="no-divider">Få lavet dit helt eget design</h2>
            <p class="section-desc">Har I et tema, et logo eller et motiv, I ikke finder her? Beskriv ønsket, så laver vi et forslag og en pris.</p>
            <div class="form-area" style="max-width:520px;margin:0 auto">
                <form class="sign-form">
                    <div class="form-group">
                        <label for="besked_eget_design_bordkort">Beskriv dit design / ønsker</label>
                        <textarea id="besked_eget_design_bordkort" name="besked_eget_design_bordkort" rows="5" placeholder="Beskriv gerne motiv, navne, antal, størrelse og anledning..."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="navn_eget_design_bordkort">Navn</label>
                        <input type="text" id="navn_eget_design_bordkort" name="navn_eget_design_bordkort" placeholder="Dit fulde navn">
                    </div>
                    <div class="form-group">
                        <label for="mail_eget_design_bordkort">Mail</label>
                        <input type="email" id="mail_eget_design_bordkort" name="mail_eget_design_bordkort" placeholder="din@mail.dk">
                    </div>
                    <div class="form-group">
                        <label for="mobil_eget_design_bordkort">Mobil nr</label>
                        <input type="tel" id="mobil_eget_design_bordkort" name="mobil_eget_design_bordkort" placeholder="+45 12 34 56 78">
                    </div>
                    <button type="submit" class="btn-submit">Send forespørgsel</button>
                </form>
            </div>
        </div>
    </section>""",
        site_name="Bordkort.dk",
        nav=nav_html_bordkort,
        footer=BORDKORT_FOOTER,
        favicon="/favicon-bordkort.ico?v=3",
        og_image=BORDKORT_OG_IMAGE,
        og_image_alt=BORDKORT_OG_ALT,
        jsonld=bordkort_jsonld(BORDKORT_FAQ),
    )
    write_page("bordkort-site/index.html", bordkort_home)
    import subprocess
    import sys
    subprocess.run([sys.executable, str(ROOT / "_restructure_bordkort_home.py")], check=True)

    bordkort_navne = page_shell(
        slug="navne",
        title="Navne bordkort i træ – personlige bordkort til fest | Dragør",
        description="Klassiske navnebordkort i træ til bryllup og fest. Personlige bordkort fra 10 kr. Håndlavet i Dragør på Amager.",
        h1="Navne bordkort i træ",
        canonical="https://bordkort.dk/navne/",
        kicker=True,
        kicker_brand="Bordkort.dk",
        crumb="Navne bordkort",
        intro_h2="Personlige navne bordkort i træ",
        intro=[
            "Vælg mellem klassiske navnebordkort i birkefiner og andre designs. Hvert bordkort graveres med gæstens navn.",
            "Afhentning i Dragør eller forsendelse i hele Danmark.",
        ],
        intro_before=True,
        products_html=render_grids(
            filter_products(lambda p: p["section"] == "bordkort_navne"),
            hide_headings={"bordkort_navne"},
        ),
        faq=[],
        site_name="Bordkort.dk",
        nav=lambda slug: nav_html_bordkort("navne", prefix="../"),
        footer=BORDKORT_FOOTER,
        favicon="/favicon-bordkort.ico?v=3",
        og_image=BORDKORT_OG_IMAGE,
        og_image_alt=BORDKORT_OG_ALT,
    )
    write_page("bordkort-site/navne/index.html", bordkort_navne)

    bordkort_speciale = page_shell(
        slug="speciale",
        title="Specielle bordkort i træ – motiver til fest | Dragør",
        description="Specielle bordkort i træ med fodbold, gaming, heste og andre motiver. Fra 10 kr. Håndlavet i Dragør på Amager.",
        h1="Specielle bordkort i træ",
        canonical="https://bordkort.dk/speciale/",
        kicker=True,
        kicker_brand="Bordkort.dk",
        crumb="Specielle bordkort",
        intro_h2="Specielle bordkort i træ",
        intro=[
            "Motivbordkort til børnefødselsdag, konfirmation og fest – fodbold, gaming, dyr og meget mere.",
            "Afhentning i Dragør eller forsendelse i hele Danmark.",
        ],
        intro_before=True,
        products_html=render_grids(
            filter_products(lambda p: p["section"] == "bordkort_speciale"),
            hide_headings={"bordkort_speciale"},
        ),
        faq=[],
        site_name="Bordkort.dk",
        nav=lambda slug: nav_html_bordkort("speciale", prefix="../"),
        footer=BORDKORT_FOOTER,
        favicon="/favicon-bordkort.ico?v=3",
        og_image=BORDKORT_OG_IMAGE,
        og_image_alt=BORDKORT_OG_ALT,
    )
    write_page("bordkort-site/speciale/index.html", bordkort_speciale)

    urls = [
        "https://æresportskilt.dk/",
        "https://æresportskilt.dk/hjerte/",
        "https://æresportskilt.dk/vaabenskjold/",
        "https://æresportskilt.dk/egetrae/",
        "https://æresportskilt.dk/bryllup/",
        "https://æresportskilt.dk/soelvbryllup/",
        "https://æresportskilt.dk/kobberbryllup/",
        "https://æresportskilt.dk/guldbryllup/",
        "https://æresportskilt.dk/gavekort/",
        "https://æresportskilt.dk/bordkort/",
        "https://æresportskilt.dk/fodselstavle/",
        "https://æresportskilt.dk/andre-skilte/",
        "https://æresportskilt.dk/velkomst-skilt/",
        "https://æresportskilt.dk/eget-design/",
        "https://æresportskilt.dk/om-os/",
        "https://bordkort.dk/",
        "https://bordkort.dk/navne/",
        "https://bordkort.dk/speciale/",
        "https://bordkort.dk/om-os/",
    ]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for i, loc in enumerate(urls):
        pri = "1.0" if i == 0 else "0.8"
        sitemap.append(f"  <url><loc>{loc}</loc><lastmod>2026-08-19</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
