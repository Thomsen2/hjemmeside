# -*- coding: utf-8 -*-
"""Restructure bordkort-site/index.html to match æresportskilt.dk forside layout."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
index = ROOT / "bordkort-site" / "index.html"
text = index.read_text(encoding="utf-8")

if "page-bordkort" in text and "bordkort-forside" in text:
    print("bordkort-site/index.html already restructured")
    raise SystemExit(0)

intro_start = text.index('    <section class="intro">')
faq_start = text.index('    <section class="faq-section" id="faq">', intro_start)
eget_start = text.index('    <section class="builder" id="eget-design">', faq_start)
footer_start = text.index("    <footer>", eget_start)

intro_block = text[intro_start:faq_start]
faq_block = text[faq_start:eget_start]
eget_block = text[eget_start:footer_start]
text = text[:intro_start] + text[footer_start:]

intro_block = intro_block.replace(
    '    <section class="intro">',
    '    <section class="intro bordkort-forside">',
    1,
)
faq_block = faq_block.replace(
    '    <section class="faq-section" id="faq">',
    '    <section class="faq-section" id="faq">',
    1,
)

hero = """    <section class="front-hero bordkort-forside" id="forside">
        <div class="container">
            <figure class="front-hero__figure">
                <img src="https://pub-a65460f11bff4b4c9a65a6943613a5ef.r2.dev/cute%20chat.png" alt="Personlige bordkort i træ på borddækning" class="front-hero__img">
            </figure>
        </div>
    </section>
"""

front_block = hero + intro_block + faq_block + eget_block

insert_at = text.index('    </nav>\n')
nav_end = insert_at + len('    </nav>\n')
text = text[:nav_end] + "\n" + front_block + text[nav_end:]

text = text.replace(
    '    <section class="builder" id="navne">',
    '    <section class="builder tab-section" id="navne">',
    1,
)
text = text.replace(
    '    <section class="builder" id="speciale">',
    '    <section class="builder tab-section" id="speciale">',
    1,
)

text = text.replace("<body>", '<body class="page-bordkort">', 1)

index.write_text(text, encoding="utf-8")
print("bordkort-site/index.html restructured")
