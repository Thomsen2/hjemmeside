from pathlib import Path

index = Path(__file__).parent / "index.html"
text = index.read_text(encoding="utf-8")

intro_start = text.index('    <section class="intro">')
faq_start = text.index('    <section class="faq-section" id="faq">', intro_start)
footer_start = text.index('    <footer>', faq_start)

intro_block = text[intro_start:faq_start]
faq_block = text[faq_start:footer_start]
text = text[:intro_start] + text[footer_start:]

intro_block = intro_block.replace('    <section class="intro">', '    <section class="intro aesport-forside">', 1)
faq_block = faq_block.replace('    <section class="faq-section" id="faq">', '    <section class="faq-section" id="faq">', 1)

eget_design = """    <section class="builder" id="eget-design">
        <div class="container">
            <h2 class="no-divider">Få lavet dit helt eget design</h2>
            <p class="section-desc">Har du en idé til et unikt skilt i træ? Fortæl os form, tekst, anledning og træsort – så laver vi et designforslag.</p>
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
    </section>

"""

hero = """    <section class="front-hero aesport-forside" id="forside">
        <div class="container">
            <figure class="front-hero__figure">
                <img src="https://pub-a65460f11bff4b4c9a65a6943613a5ef.r2.dev/lily%20og%20harald%20egetr%C3%A6.png" alt="Æresportskilt våbenskjold i egetræ" class="front-hero__img">
            </figure>
        </div>
    </section>
"""

front_block = hero + intro_block + faq_block + eget_design

insert_at = text.index('    </nav>\n    \n    <section class="builder">')
text = text[:insert_at + len('    </nav>\n\n')] + front_block + text[insert_at + len('    </nav>\n    \n'):]

replacements = [
    ('    <section class="builder">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i birkefiner</h2>',
     '    <section class="builder tab-section" id="birkefiner">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i birkefiner</h2>'),
    ('    <section class="builder">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i egetræ</h2>',
     '    <section class="builder tab-section" id="egetrae">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i egetræ</h2>'),
    ('    <section class="builder">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i bejdset valnød</h2>',
     '    <section class="builder tab-section" id="version1">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i bejdset valnød</h2>'),
    ('    <section class="builder">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i amerikansk valnød</h2>',
     '    <section class="builder tab-section" id="version2">\n        <div class="container">\n            <h2 class="no-divider">Æresportskilt – hjerte i amerikansk valnød</h2>'),
    ('    <section class="builder">\n        <div class="container">\n            <h2 class="no-divider">Skilte og dekoration til bryllup</h2>',
     '    <section class="builder tab-section" id="bryllup">\n        <div class="container">\n            <h2 class="no-divider">Skilte og dekoration til bryllup</h2>'),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Missing section marker: {old[:60]}...")
    text = text.replace(old, new, 1)

text = text.replace("<body>", '<body class="page-aesport-home">', 1)
text = text.replace('/styles.css?v=117', '/styles.css?v=121')
text = text.replace('/script.js?v=38', '/script.js?v=42')

index.write_text(text, encoding="utf-8")
print("index.html restructured")
