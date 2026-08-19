# -*- coding: utf-8 -*-
"""Extract product cards from the current index.html into data/produkter.json."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def slugify(text: str, used: set[str]) -> str:
    text = text.lower()
    text = text.replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    base = text[:60] or "produkt"
    slug = base
    n = 2
    while slug in used:
        slug = f"{base}-{n}"
        n += 1
    used.add(slug)
    return slug


def infer(title: str, section: str, desc: str) -> dict:
    blob = f"{title} {section} {desc}".lower()
    form = "andet"
    if "våben" in blob or "vaaben" in blob:
        form = "vaabenskjold"
    elif "hjerte" in blob:
        form = "hjerte"
    wood = ""
    if "egetr" in blob:
        wood = "egetrae"
    elif "valnød" in blob or "valdnød" in blob:
        wood = "valnod"
    elif "birk" in blob:
        wood = "birkefiner"
    occasions = []
    if "kobber" in blob:
        occasions.append("kobberbryllup")
    if "sølv" in blob or "solv" in blob:
        occasions.append("soelvbryllup")
    if "guld" in blob:
        occasions.append("guldbryllup")
    if "bryllup" in blob or section == "bryllup":
        occasions.append("bryllup")
    if "konfirm" in blob:
        occasions.append("konfirmation")
    return {"form": form, "wood": wood, "occasions": occasions}


class CardParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section_id = ""
        self.section_h2 = ""
        self.section_note = ""
        self.section_intro = []
        self.products = []
        self.sections_meta = {}
        self._in_section = False
        self._section_class = ""
        self._in_h2 = False
        self._in_note = False
        self._in_intro_p = False
        self._in_card = False
        self._card_depth = 0
        self._in_title = False
        self._in_size = False
        self._in_price = False
        self._in_label = False
        self._capture = ""
        self._card = None
        self._await_label_for_textarea = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "")
        if tag == "section" and attrs.get("id") and "tab-section" in classes:
            self._in_section = True
            self.section_id = attrs["id"]
            self.section_h2 = ""
            self.section_note = ""
            self.section_intro = []
            self._section_class = classes
        if not self._in_section:
            return
        if tag == "h2":
            self._in_h2 = True
            self._capture = ""
        elif tag == "p" and "wood-note" in classes:
            self._in_note = True
            self._capture = ""
        elif tag == "p" and "section-intro" in self._section_class or (
            tag == "p" and self.section_id
            and not self._in_card
            and "product-card" not in classes
            and "wood-note" not in classes
            and "section-desc" in classes
        ):
            self._in_intro_p = True
            self._capture = ""
        elif tag == "p" and not self._in_card and "section-desc" in classes:
            self._in_intro_p = True
            self._capture = ""
        elif tag == "article" and "product-card" in classes:
            self._in_card = True
            self._card_depth = 1
            self._card = {
                "section": self.section_id,
                "description": attrs.get("data-beskrivelse", ""),
                "title": "",
                "size": "",
                "price": "",
                "images": [],
                "form_label": "Skriv dine ønsker til skiltet her",
                "mounting": False,
            }
            return
        if self._in_card:
            if tag == "article":
                self._card_depth += 1
            if tag == "img":
                src = attrs.get("src", "")
                if src:
                    self._card["images"].append(
                        {
                            "src": src,
                            "alt": attrs.get("alt", ""),
                            "hidden": "hidden" in attrs or "product-card__img--alt" in classes,
                        }
                    )
            if tag == "h3" and "product-card__title" in classes:
                self._in_title = True
                self._capture = ""
            if tag == "p" and "product-card__size" in classes:
                self._in_size = True
                self._capture = ""
            if tag == "p" and "product-card__price" in classes:
                self._in_price = True
                self._capture = ""
            if tag == "label" and attrs.get("for", "").startswith("besked") or (
                tag == "label" and self._await_label_for_textarea
            ):
                self._in_label = True
                self._capture = ""
            if tag == "label" and attrs.get("for"):
                if "besked" in attrs.get("for", ""):
                    self._in_label = True
                    self._capture = ""
            if tag == "input" and "mounting-toggle" in classes:
                self._card["mounting"] = True

    def handle_endtag(self, tag):
        if self._in_h2 and tag == "h2":
            self.section_h2 = re.sub(r"\s+", " ", self._capture).strip()
            self._in_h2 = False
        if self._in_note and tag == "p":
            self.section_note = re.sub(r"\s+", " ", self._capture).strip()
            self._in_note = False
        if self._in_intro_p and tag == "p":
            text = re.sub(r"\s+", " ", self._capture).strip()
            if text:
                self.section_intro.append(text)
            self._in_intro_p = False
        if self._in_title and tag == "h3":
            self._card["title"] = re.sub(r"\s+", " ", self._capture).strip()
            self._in_title = False
        if self._in_size and tag == "p":
            self._card["size"] = re.sub(r"\s+", " ", self._capture).strip()
            self._in_size = False
        if self._in_price and tag == "p":
            self._card["price"] = re.sub(r"\s+", " ", self._capture).strip()
            self._in_price = False
        if self._in_label and tag == "label":
            text = re.sub(r"\s+", " ", self._capture).strip()
            if text and "navn" not in text.lower() and "mail" not in text.lower():
                self._card["form_label"] = text
            self._in_label = False
        if self._in_card:
            if tag == "article":
                self._card_depth -= 1
                if self._card_depth <= 0:
                    self.products.append(self._card)
                    self._card = None
                    self._in_card = False
        if tag == "section" and self._in_section and not self._in_card:
            self.sections_meta[self.section_id] = {
                "id": self.section_id,
                "h2": self.section_h2,
                "note": self.section_note,
                "intro": self.section_intro,
                "class": self._section_class,
            }
            self._in_section = False

    def handle_data(self, data):
        if self._in_h2 or self._in_note or self._in_intro_p or self._in_title or self._in_size or self._in_price or self._in_label:
            self._capture += data


def main():
    parser = CardParser()
    parser.feed(HTML)
    used = set()
    products = []
    for i, p in enumerate(parser.products, 1):
        inferred = infer(p["title"], p["section"], p["description"])
        p["id"] = slugify(p["title"] or p["description"] or f"produkt-{i}", used)
        p.update(inferred)
        products.append(p)

    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    payload = {"sections": parser.sections_meta, "products": products}
    (out / "produkter.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{len(products)} produkter, {len(parser.sections_meta)} sektioner")
    for sid, meta in parser.sections_meta.items():
        n = sum(1 for p in products if p["section"] == sid)
        print(f"  {sid}: {n}  ({meta.get('h2')})")


if __name__ == "__main__":
    main()
