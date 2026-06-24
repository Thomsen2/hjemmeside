document.querySelectorAll('.nav-link, .nav-sub-link').forEach(function (link) {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        var sectionId = this.getAttribute('data-section');
        document.querySelectorAll('.nav-link').forEach(function (l) { l.classList.remove('active'); });
        var dropdown = this.closest('.nav-dropdown');
        if (dropdown) {
            dropdown.querySelector('.nav-link').classList.add('active');
        } else {
            this.classList.add('active');
        }
        document.querySelectorAll('.tab-section').forEach(function (s) { s.classList.remove('active'); });
        var section = document.getElementById(sectionId);
        if (section) section.classList.add('active');
    });
});

document.querySelectorAll('.shipping-toggle').forEach(function (toggle) {
    toggle.addEventListener('change', function () {
        var fields = this.closest('form').querySelector('.shipping-fields');
        if (this.checked) {
            fields.classList.add('visible');
            var pickup = this.closest('form').querySelector('.pickup-toggle');
            if (pickup) pickup.checked = false;
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
        var mountingChecked = this.querySelector('.mounting-toggle').checked;

        if (!besked) {
            alert('Udfyld venligst din besked.');
            return;
        }

        var sectionTitle = this.closest('section').querySelector('h2').textContent.trim();

        var payload = {
            produkt: sectionTitle,
            besked: besked,
            shipping: shippingChecked,
            pickup: pickupChecked,
            mounting: mountingChecked
        };

        if (pickupChecked) {
            payload.pickupEmail = this.querySelector('.pickup-email').value.trim();
        }

        if (shippingChecked) {
            payload.navn = this.querySelector('.shipping-fields input[id*="navn"]').value.trim();
            payload.adresse = this.querySelector('.shipping-fields input[id*="adresse"]').value.trim();
            payload.mail = this.querySelector('.shipping-fields input[id*="mail"]').value.trim();
            payload.mobil = this.querySelector('.shipping-fields input[id*="mobil"]').value.trim();
        }

        var btn = this.querySelector('.btn-submit');
        btn.textContent = 'Sender...';
        btn.disabled = true;

        fetch('/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(function (resp) { return resp.json(); })
        .then(function (data) {
            if (data.success) {
                alert('Tak! Din forespørgsel er gemt.');
                btn.closest('form').querySelectorAll('textarea, input[type="text"], input[type="email"], input[type="tel"]').forEach(function (el) { el.value = ''; });
                btn.closest('form').querySelectorAll('input[type="checkbox"]').forEach(function (el) { el.checked = false; });
            } else {
                alert('Fejl: ' + data.error);
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

document.querySelectorAll('.sign-photo').forEach(function (img) {
    img.style.cursor = 'pointer';
    img.addEventListener('click', function () {
        window.open(this.src, '_blank');
    });
});
