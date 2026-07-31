(function () {
    var nav = document.getElementById('mainNav');
    var toggle = document.getElementById('navToggle');
    var links = document.getElementById('navLinks');

    function closeNav() {
        if (!nav) return;
        nav.classList.remove('is-open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
        document.querySelectorAll('.nav-dropdown.is-open').forEach(function (d) {
            d.classList.remove('is-open');
        });
    }

    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
    }

    function activateSection(sectionId) {
        if (!sectionId) return;
        document.querySelectorAll('.nav-link').forEach(function (l) {
            l.classList.remove('active');
        });
        var matching = document.querySelector('.nav-link[data-section="' + sectionId + '"]');
        if (matching) {
            var dropdown = matching.closest('.nav-dropdown');
            if (dropdown) {
                dropdown.querySelector('.nav-link').classList.add('active');
            } else {
                matching.classList.add('active');
            }
        } else {
            document.querySelectorAll('.nav-link').forEach(function (link) {
                var dd = link.closest('.nav-dropdown');
                if (!dd) return;
                var sub = dd.querySelector('.nav-sub-link[data-section="' + sectionId + '"]');
                if (sub) link.classList.add('active');
            });
        }
        document.querySelectorAll('.tab-section').forEach(function (s) {
            s.classList.remove('active');
        });
        var section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('active');
            window.scrollTo({ top: nav ? nav.offsetTop : 0, behavior: 'smooth' });
        }
        closeNav();
    }

    document.querySelectorAll('.nav-link, .nav-sub-link, .btn-hero').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var sectionId = this.getAttribute('data-section');
            if (!sectionId) return;
            e.preventDefault();

            if (this.classList.contains('nav-link') && this.closest('.nav-dropdown') && window.matchMedia('(max-width: 780px)').matches) {
                var dd = this.closest('.nav-dropdown');
                if (!e.target.closest('.nav-sub-link')) {
                    var already = dd.classList.contains('is-open');
                    document.querySelectorAll('.nav-dropdown.is-open').forEach(function (d) {
                        d.classList.remove('is-open');
                    });
                    if (!already) {
                        dd.classList.add('is-open');
                        return;
                    }
                }
            }

            activateSection(sectionId);
        });
    });

    document.addEventListener('click', function (e) {
        if (nav && nav.classList.contains('is-open') && !nav.contains(e.target)) {
            closeNav();
        }
    });

    // Boblende ikoner ved hover på Hjerte / Våbenskjold
    document.querySelectorAll('.nav-dropdown').forEach(function (dropdown) {
        var link = dropdown.querySelector('.nav-link');
        if (!link) return;
        if (!link.querySelector('.nav-icon--heart, .nav-icon--shield')) return;
        dropdown.addEventListener('mouseenter', function () {
            link.classList.add('is-bubbling');
        });
        dropdown.addEventListener('mouseleave', function () {
            link.classList.remove('is-bubbling');
        });
        link.addEventListener('focus', function () {
            link.classList.add('is-bubbling');
        });
        link.addEventListener('blur', function () {
            link.classList.remove('is-bubbling');
        });
    });

    // Klik-zoom på alle produktbilleder: 300% af sektionens hover-størrelse
    document.querySelectorAll('.sign-preview').forEach(function (preview) {
        preview.addEventListener('click', function (e) {
            e.stopPropagation();
            var open = preview.classList.toggle('is-zoomed');
            if (open) {
                document.querySelectorAll('.sign-preview.is-zoomed').forEach(function (other) {
                    if (other !== preview) other.classList.remove('is-zoomed');
                });
            }
        });
    });
    document.addEventListener('click', function (e) {
        if (e.target.closest('.sign-preview')) return;
        document.querySelectorAll('.sign-preview.is-zoomed').forEach(function (el) {
            el.classList.remove('is-zoomed');
        });
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.sign-preview.is-zoomed').forEach(function (el) {
                el.classList.remove('is-zoomed');
            });
        }
    });
})();

document.querySelectorAll('.shipping-toggle').forEach(function (toggle) {
    toggle.addEventListener('change', function () {
        var fields = this.closest('form').querySelector('.shipping-fields');
        if (this.checked) {
            fields.classList.add('visible');
            var pickup = this.closest('form').querySelector('.pickup-toggle');
            if (pickup) pickup.checked = false;
            var pfields = this.closest('form').querySelector('.pickup-fields');
            if (pfields) pfields.classList.remove('visible');
        } else {
            fields.classList.remove('visible');
        }
    });
});

document.querySelectorAll('.pickup-toggle').forEach(function (toggle) {
    toggle.addEventListener('change', function () {
        var fields = this.closest('form').querySelector('.pickup-fields');
        if (this.checked) {
            fields.classList.add('visible');
            var shipping = this.closest('form').querySelector('.shipping-toggle');
            if (shipping) shipping.checked = false;
            var sfields = this.closest('form').querySelector('.shipping-fields');
            if (sfields) sfields.classList.remove('visible');
        } else {
            fields.classList.remove('visible');
        }
    });
});

document.querySelectorAll('.sign-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        var besked = this.querySelector('textarea').value.trim();
        var shippingChecked = this.querySelector('.shipping-toggle').checked;
        var pickupChecked = this.querySelector('.pickup-toggle').checked;
        var mountingEl = this.querySelector('.mounting-toggle');
        var mountingChecked = mountingEl ? mountingEl.checked : false;

        if (!besked) {
            alert('Udfyld venligst din besked.');
            return;
        }

        var sectionTitle = this.closest('section').querySelector('h2').textContent.trim();
        var captionEl = this.closest('.builder-grid');
        captionEl = captionEl ? captionEl.querySelector('.sign-caption') : null;
        var beskrivelse = captionEl
            ? captionEl.innerText.replace(/\s+/g, ' ').trim()
            : '';

        var payload = {
            produkt: sectionTitle,
            beskrivelse: beskrivelse,
            besked: besked,
            shipping: shippingChecked,
            pickup: pickupChecked,
            mounting: mountingChecked
        };

        if (pickupChecked) {
            payload.pickupEmail = this.querySelector('.pickup-email').value.trim();
        }

        if (shippingChecked) {
            var navnEl = this.querySelector('.shipping-fields input[id*="navn"]') || this.querySelector('.shipping-fields input[type="text"]');
            var adresseEl = this.querySelector('.shipping-fields input[id*="adresse"]');
            var mailEl = this.querySelector('.shipping-fields input[id*="mail"], .shipping-fields input[type="email"]');
            var mobilEl = this.querySelector('.shipping-fields input[id*="mobil"], .shipping-fields input[type="tel"]');
            payload.navn = navnEl ? navnEl.value.trim() : '';
            payload.adresse = adresseEl ? adresseEl.value.trim() : '';
            payload.mail = mailEl ? mailEl.value.trim() : '';
            payload.mobil = mobilEl ? mobilEl.value.trim() : '';
        }

        var btn = this.querySelector('.btn-submit');
        btn.textContent = 'Sender...';
        btn.disabled = true;

        var emailBody = {
            'form-name': 'bestilling',
            'bot-field': '',
            subject: 'Ny forespørgsel: ' + (beskrivelse || sectionTitle),
            Produkt: sectionTitle,
            Beskrivelse: beskrivelse || sectionTitle,
            Besked: besked,
            Afhentning: pickupChecked ? 'Ja (Dragør)' : 'Nej',
            Forsendelse: shippingChecked ? 'Ja (55 kr)' : 'Nej',
            Monteringskit: mountingChecked ? 'Ja (+20 kr)' : 'Nej',
            'Afhentnings-email': pickupChecked ? (payload.pickupEmail || '') : '',
            Navn: shippingChecked ? (payload.navn || '') : '',
            Adresse: shippingChecked ? (payload.adresse || '') : '',
            Mail: shippingChecked ? (payload.mail || '') : '',
            Mobil: shippingChecked ? (payload.mobil || '') : ''
        };

        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(emailBody).toString()
        })
        .then(function (resp) {
            if (resp.ok) {
                alert('Tak! Din forespørgsel er sendt.');
                btn.closest('form').querySelectorAll('textarea, input[type="text"], input[type="email"], input[type="tel"]').forEach(function (el) { el.value = ''; });
                btn.closest('form').querySelectorAll('input[type="checkbox"]').forEach(function (el) { el.checked = false; });
                btn.closest('form').querySelectorAll('.shipping-fields, .pickup-fields').forEach(function (el) { el.classList.remove('visible'); });
            } else {
                alert('Fejl: Kunne ikke sende forespørgslen. Prøv igen.');
            }
        })
        .catch(function (err) {
            alert('Der opstod en fejl: ' + err.message);
        })
        .finally(function () {
            btn.textContent = 'Send forespørgsel';
            btn.disabled = false;
        });
    });
});
