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

    var aesportMenus = {
        birkefiner: true,
        egetrae: true,
        version1: true,
        version2: true,
        vaabenskjold: true,
        egetrae_v2: true,
        version1_v2: true,
        version2_v2: true
    };

    function scrollToFaq() {
        var el = document.getElementById('faq');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function activateSection(sectionId) {
        if (!sectionId || document.body.classList.contains('page-aesport-home')) return;

        if (sectionId === 'faq') {
            if (document.getElementById('faq')) {
                var current = document.querySelector('.tab-section.active');
                var currentId = current && current.id;
                if (currentId && !aesportMenus[currentId] && document.getElementById('birkefiner')) {
                    activateSection('birkefiner');
                } else {
                    document.body.classList.remove('hide-aesport-intro');
                    closeNav();
                }
                setTimeout(scrollToFaq, 50);
                return;
            }
        }

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
        document.body.classList.toggle('hide-aesport-intro', !aesportMenus[sectionId]);
        closeNav();
    }

    document.querySelectorAll('.nav-link, .nav-sub-link, .btn-hero, .footer-om-os').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var href = this.getAttribute('href') || '';
            var path = href.split('#')[0];
            var isSeoPath = /^\/[a-z0-9-]+\/?$/.test(path);

            if (this.classList.contains('nav-link') && this.closest('.nav-dropdown') && window.matchMedia('(max-width: 780px)').matches) {
                var dd = this.closest('.nav-dropdown');
                if (dd.querySelector('.nav-submenu') && !e.target.closest('.nav-sub-link')) {
                    var already = dd.classList.contains('is-open');
                    document.querySelectorAll('.nav-dropdown.is-open').forEach(function (d) {
                        d.classList.remove('is-open');
                    });
                    if (!already) {
                        e.preventDefault();
                        dd.classList.add('is-open');
                        return;
                    }
                }
            }

            if (isSeoPath) return;

            var sectionId = this.getAttribute('data-section');
            if (!sectionId) return;

            if (sectionId !== 'faq' && !document.getElementById(sectionId)) {
                window.location.href = '/#' + sectionId;
                return;
            }
            e.preventDefault();

            activateSection(sectionId);
            if (history.replaceState) {
                history.replaceState(null, '', '#' + sectionId);
            } else {
                location.hash = sectionId;
            }
        });
    });

    var hashPages = {
        gavekort: '/gavekort/',
        bordkort: '/bordkort/',
        bordkort_navne: '/bordkort/',
        bordkort_speciale: '/bordkort/',
        fodselstavle: '/fodselstavle/',
        andre_skilte: '/andre-skilte/',
        velkomst_skilt: '/velkomst-skilt/',
        eget_design: '/eget-design/',
        bestil: '/om-os/',
        vaabenskjold: '/vaabenskjold/',
        birkefiner: '/hjerte/',
        egetrae: '/egetrae/',
        bryllup: '/bryllup/'
    };

    var hashId = (location.hash || '').replace(/^#/, '');
    if (hashId === 'bordkort') hashId = 'bordkort_speciale';
    var aesportHomeHashes = {
        forside: true,
        faq: true,
        'eget-design': true,
        birkefiner: true,
        egetrae: true,
        version1: true,
        version2: true,
        bryllup: true,
        vaabenskjold: true
    };
    var onAesportHome = document.body.classList.contains('page-aesport-home');
    if (hashId && hashPages[hashId] && !(onAesportHome && aesportHomeHashes[hashId])) {
        location.replace(hashPages[hashId]);
        return;
    }
    if (!document.body.classList.contains('page-bordkort') && !onAesportHome && hashId && document.getElementById(hashId)) {
        activateSection(hashId);
    }

    document.addEventListener('click', function (e) {
        if (nav && nav.classList.contains('is-open') && !nav.contains(e.target)) {
            closeNav();
        }
    });

    // Boblende ikoner ved hover på Hjerte / Våbenskjold / Gavekort / Bordkort / Fødselstavle / Bryllup
    function bindBubbling(host, link) {
        if (!link) return;
        host.addEventListener('mouseenter', function () {
            link.classList.add('is-bubbling');
        });
        host.addEventListener('mouseleave', function () {
            link.classList.remove('is-bubbling');
        });
        link.addEventListener('focus', function () {
            link.classList.add('is-bubbling');
        });
        link.addEventListener('blur', function () {
            link.classList.remove('is-bubbling');
        });
    }

    document.querySelectorAll('.nav-dropdown').forEach(function (dropdown) {
        var link = dropdown.querySelector('.nav-link');
        if (link && link.querySelector('.nav-icon--heart, .nav-icon--shield, .nav-icon--card, .nav-icon--rings')) {
            bindBubbling(dropdown, link);
        }
        dropdown.addEventListener('mouseleave', function () {
            var focused = dropdown.querySelector(':focus');
            if (focused) focused.blur();
            dropdown.classList.remove('is-open');
        });
    });

    document.querySelectorAll('.nav-link').forEach(function (link) {
        if (!link.querySelector('.nav-icon--gift, .nav-icon--pram, .nav-icon--card, .nav-icon--rings')) return;
        if (link.closest('.nav-dropdown')) return;
        bindBubbling(link, link);
    });

    // Klik-zoom på alle produktbilleder: 300% af sektionens hover-størrelse
    // Specielle bordkort: vis miljøbillede (tallerken) i overlay
    document.querySelectorAll('.sign-preview').forEach(function (preview) {
        preview.addEventListener('click', function (e) {
            e.stopPropagation();

            if (preview.classList.contains('product-card__media')) {
                var altImg = preview.querySelector('.product-card__img--alt');
                var mainImg = preview.querySelector('.product-card__img:not(.product-card__img--alt)');
                var showImg = altImg || mainImg;
                var overlay = document.getElementById('imgOverlay');
                var overlayImg = document.getElementById('imgOverlayImg');
                if (showImg && overlay && overlayImg) {
                    overlayImg.src = showImg.currentSrc || showImg.src;
                    overlayImg.alt = showImg.alt || '';
                    overlay.style.display = 'flex';
                }
                return;
            }

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
            var overlay = document.getElementById('imgOverlay');
            if (overlay) overlay.style.display = 'none';
        }
    });

    var bordkortNavne = document.getElementById('navne');
    var bordkortSpeciale = document.getElementById('speciale');
    if (bordkortNavne && bordkortSpeciale && bordkortNavne.classList.contains('tab-section')) {
        function syncBordkortCatalog() {
            var hash = (location.hash || '#forside').replace(/^#/, '');
            var isCatalog = hash === 'navne' || hash === 'speciale';
            document.body.classList.toggle('bordkort-view-catalog', isCatalog);
            document.body.classList.remove('hide-aesport-intro');
            bordkortNavne.classList.toggle('active', hash === 'navne');
            bordkortSpeciale.classList.toggle('active', hash === 'speciale');
            document.querySelectorAll('#navLinks .nav-link[href^="#"]').forEach(function (link) {
                var target = (link.getAttribute('href') || '#forside').slice(1);
                link.classList.toggle('active', target === hash);
            });
            if (isCatalog) {
                window.scrollTo({ top: nav ? nav.offsetTop : 0, behavior: 'smooth' });
            } else {
                var scrollTarget = document.getElementById(hash === 'forside' ? 'forside' : hash);
                if (scrollTarget) {
                    setTimeout(function () {
                        scrollTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 50);
                } else if (hash === 'forside') {
                    window.scrollTo({ top: nav ? nav.offsetTop : 0, behavior: 'smooth' });
                }
            }
            closeNav();
        }
        if (!location.hash) {
            history.replaceState(null, '', '#forside');
        }
        window.addEventListener('hashchange', syncBordkortCatalog);
        document.querySelectorAll('#navLinks .nav-link[href^="#"], footer a[href^="#"]').forEach(function (link) {
            link.addEventListener('click', function () {
                setTimeout(syncBordkortCatalog, 0);
            });
        });
        syncBordkortCatalog();
    }

    var aesportCatalogIds = ['birkefiner', 'egetrae', 'version1', 'version2', 'vaabenskjold', 'bryllup'];
    var aesportBirkefiner = document.getElementById('birkefiner');
    if (onAesportHome && aesportBirkefiner && aesportBirkefiner.classList.contains('tab-section')) {
        function getAesportHash() {
            var hash = (location.hash || '#forside').replace(/^#/, '');
            return hash || 'forside';
        }

        function syncAesportHomeCatalog() {
            var hash = getAesportHash();
            var isCatalog = aesportCatalogIds.indexOf(hash) !== -1;

            document.body.classList.remove('hide-aesport-intro');
            document.body.classList.toggle('aesport-view-catalog', isCatalog);

            document.querySelectorAll('.tab-section').forEach(function (section) {
                section.classList.toggle('active', isCatalog && section.id === hash);
            });

            document.querySelectorAll('#navLinks .nav-link[href^="#"], header h1 a[href^="#"]').forEach(function (link) {
                var target = (link.getAttribute('href') || '#forside').slice(1);
                link.classList.toggle('active', target === hash);
            });

            closeNav();

            requestAnimationFrame(function () {
                if (isCatalog) {
                    window.scrollTo({ top: nav ? nav.offsetTop : 0, behavior: 'smooth' });
                    return;
                }
                var scrollTarget = document.getElementById(hash);
                if (scrollTarget) {
                    scrollTarget.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    window.scrollTo({ top: nav ? nav.offsetTop : 0, behavior: 'smooth' });
                }
            });
        }

        function navigateAesportHome(hash) {
            var target = '#' + hash;
            if (location.hash === target) {
                syncAesportHomeCatalog();
            } else {
                location.hash = hash;
            }
        }

        function resetAesportHomeForLeave() {
            document.body.classList.remove('aesport-view-catalog', 'hide-aesport-intro');
            document.querySelectorAll('.tab-section').forEach(function (section) {
                section.classList.remove('active');
            });
            if (location.hash !== '#forside') {
                history.replaceState(null, '', '#forside');
                syncAesportHomeCatalog();
            }
        }

        document.addEventListener('click', function (e) {
            var link = e.target.closest('a[href^="#"]');
            if (link) {
                var href = link.getAttribute('href') || '';
                if (href !== '#') {
                    var hash = href.slice(1);
                    if (aesportHomeHashes[hash] || document.getElementById(hash)) {
                        e.preventDefault();
                        navigateAesportHome(hash);
                    }
                }
                return;
            }
            link = e.target.closest('a[href]');
            if (!link) return;
            var path = link.getAttribute('href') || '';
            if (!path || path.charAt(0) === '#') return;
            if (/^https?:\/\//i.test(path) && path.indexOf(location.origin) !== 0) return;
            if (path.charAt(0) === '/' || path.indexOf(location.origin) === 0) {
                resetAesportHomeForLeave();
            }
        }, true);

        window.addEventListener('hashchange', syncAesportHomeCatalog);
        window.addEventListener('popstate', syncAesportHomeCatalog);
        window.addEventListener('pageshow', function (e) {
            syncAesportHomeCatalog();
            if (e.persisted) {
                requestAnimationFrame(syncAesportHomeCatalog);
            }
        });

        if (!location.hash || location.hash === '#') {
            history.replaceState(null, '', '#forside');
        }
        syncAesportHomeCatalog();
    }
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
        var shippingToggle = this.querySelector('.shipping-toggle');
        var pickupToggle = this.querySelector('.pickup-toggle');
        var shippingChecked = shippingToggle ? shippingToggle.checked : false;
        var pickupChecked = pickupToggle ? pickupToggle.checked : false;
        var mountingEl = this.querySelector('.mounting-toggle');
        var mountingChecked = mountingEl ? mountingEl.checked : false;

        if (!besked) {
            alert('Udfyld venligst din besked.');
            return;
        }

        var sectionTitle = this.closest('section').querySelector('h2').textContent.trim();
        var card = this.closest('.product-card');
        var grid = this.closest('.builder-grid');
        var beskrivelse = '';
        var imgEl = null;
        if (card) {
            beskrivelse = (card.getAttribute('data-beskrivelse') || '').trim();
            if (!beskrivelse) {
                var t = card.querySelector('.product-card__title');
                var p = card.querySelector('.product-card__price');
                var s = card.querySelector('.product-card__size');
                beskrivelse = [t && t.textContent, p && p.textContent, s && s.textContent]
                    .filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
            }
            imgEl = card.querySelector('.product-card__img:not(.product-card__img--alt)') || card.querySelector('.sign-photo');
        } else if (grid) {
            var captionEl = grid.querySelector('.sign-caption');
            beskrivelse = captionEl
                ? captionEl.innerText.replace(/\s+/g, ' ').trim()
                : '';
            imgEl = grid.querySelector('.sign-photo');
        }
        var billedeUrl = '';
        if (imgEl && imgEl.src) {
            try { billedeUrl = new URL(imgEl.getAttribute('src'), window.location.href).href; }
            catch (err) { billedeUrl = imgEl.src; }
        }

        var payload = {
            produkt: sectionTitle,
            beskrivelse: beskrivelse,
            besked: besked,
            shipping: shippingChecked,
            pickup: pickupChecked,
            mounting: mountingChecked
        };

        if (pickupChecked) {
            var pickupEmailEl = this.querySelector('.pickup-email');
            payload.pickupEmail = pickupEmailEl ? pickupEmailEl.value.trim() : '';
        }

        var navnEl = this.querySelector('.shipping-fields input[id*="navn"]') || this.querySelector('input[id*="navn"]');
        var adresseEl = this.querySelector('.shipping-fields input[id*="adresse"]') || this.querySelector('input[id*="adresse"]');
        var mailEl = this.querySelector('.shipping-fields input[id*="mail"], .shipping-fields input[type="email"]') || this.querySelector('input[id*="mail"], input[type="email"]:not(.pickup-email)');
        var mobilEl = this.querySelector('.shipping-fields input[id*="mobil"], .shipping-fields input[type="tel"]') || this.querySelector('input[id*="mobil"], input[type="tel"]');
        var hasContactFields = !!(navnEl || mailEl || mobilEl);

        if (shippingChecked || hasContactFields) {
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
            'Billede-eksempel': billedeUrl,
            Afhentning: pickupChecked ? 'Ja (Dragør)' : 'Nej',
            Forsendelse: shippingChecked ? 'Ja (55 kr)' : 'Nej',
            Monteringskit: mountingChecked ? 'Ja (+20 kr)' : 'Nej',
            'Afhentnings-email': pickupChecked ? (payload.pickupEmail || '') : '',
            Navn: payload.navn || '',
            Adresse: payload.adresse || '',
            Mail: payload.mail || '',
            Mobil: payload.mobil || ''
        };

        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(emailBody).toString()
        })
        .then(function (resp) {
            if (resp.ok) {
                alert('Tak! Din forespørgsel er sendt. Hold øje med din mail, for bekræftelse af design og betaling');
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
