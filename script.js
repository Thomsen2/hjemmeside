document.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        var sectionId = this.getAttribute('data-section');
        document.querySelectorAll('.nav-link').forEach(function (l) { l.classList.remove('active'); });
        this.classList.add('active');
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
        if (this.checked) {
            var shipping = this.closest('form').querySelector('.shipping-toggle');
            if (shipping) shipping.checked = false;
            var fields = this.closest('form').querySelector('.shipping-fields');
            if (fields) fields.classList.remove('visible');
        }
    });
});

function handleFormSubmit(form, e) {
    e.preventDefault();

    var textarea = form.querySelector('textarea');
    var besked = textarea ? textarea.value.trim() : '';

    if (!besked) {
        alert('Udfyld venligst din besked.');
        return;
    }

    var shippingChecked = form.querySelector('.shipping-toggle').checked;
    var pickupChecked = form.querySelector('.pickup-toggle').checked;
    var mountingChecked = form.querySelector('.mounting-toggle').checked;
    var testChecked = form.querySelector('input[name="test"]') ? form.querySelector('input[name="test"]').checked : false;

    var caption = form.closest('.builder-grid').querySelector('.sign-caption');
    var captionText = caption ? caption.textContent.replace(/\s+/g, ' ').trim() : 'Æresportskilt';

    var bodyParts = 'Produkt: ' + captionText + '\n\n' +
        'Besked: ' + besked;

    var ekstra = [];
    if (pickupChecked) ekstra.push('Afhentning i Dragør (gratis)');
    if (shippingChecked) ekstra.push('Skal sendes (55 kr)');
    if (mountingChecked) ekstra.push('Monteringskit (+20 kr)');
    if (testChecked) ekstra.push('test');
    if (ekstra.length > 0) bodyParts += '\n\nTilvalg: ' + ekstra.join(', ');

    if (shippingChecked) {
        var fieldsContainer = form.querySelector('.shipping-fields');
        var navn = fieldsContainer.querySelectorAll('input[type="text"]')[0].value.trim();
        var adresse = fieldsContainer.querySelectorAll('input[type="text"]')[1].value.trim();
        var postnr = fieldsContainer.querySelector('.postnr-input').value.trim();
        var by = fieldsContainer.querySelector('.by-input').value.trim();
        var mail = fieldsContainer.querySelector('input[type="email"]').value.trim();
        var mobil = fieldsContainer.querySelector('input[type="tel"]').value.trim();
        bodyParts += '\n\n--- Levering ---\n' +
            'Navn: ' + navn + '\n' +
            'Adresse: ' + adresse + '\n' +
            'Post nr.: ' + postnr + '\n' +
            'By: ' + by + '\n' +
            'Mail: ' + mail + '\n' +
            'Mobil: ' + mobil;
    }

    var btn = form.querySelector('.btn-submit');
    btn.textContent = 'Sender...';
    btn.disabled = true;

    fetch('/api/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product: captionText, body: bodyParts })
    })
    .then(function (res) {
        if (res.ok) return res.text();
        throw new Error('Fejl ved afsendelse');
    })
    .then(function (html) {
        document.body.innerHTML = html;
    })
    .catch(function (err) {
        alert('Kunne ikke sende. Prøv igen.');
        btn.textContent = 'Send forespørgsel';
        btn.disabled = false;
    });
}

document.querySelectorAll('.sign-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
        handleFormSubmit(this, e);
    });
});
