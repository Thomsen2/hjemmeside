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

document.getElementById('signForm').addEventListener('submit', function (e) {
    e.preventDefault();
    handleFormSubmit(this);
});

document.querySelectorAll('.sign-form').forEach(function (form) {
    if (form.id !== 'signForm') {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            handleFormSubmit(this);
        });
    }
});

function handleFormSubmit(form) {
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

    var bodyParts = 'Ny forespørgsel på æresportskilt.dk\n\n' +
        'Produkt: ' + captionText + '\n' +
        'Besked: ' + besked;

    var ekstra = [];
    if (pickupChecked) ekstra.push('Afhentning i Dragør (gratis)');
    if (shippingChecked) ekstra.push('Skal sendes (55 kr)');
    if (mountingChecked) ekstra.push('Monteringskit (+20 kr)');
    if (testChecked) ekstra.push('test');
    if (ekstra.length > 0) bodyParts += '\n\nTilvalg: ' + ekstra.join(', ');

    if (shippingChecked) {
        var fieldsContainer = form.querySelector('.shipping-fields');
        var navn = fieldsContainer.querySelector('input[type="text"]:nth-of-type(1)').value.trim();
        var adresse = fieldsContainer.querySelector('input[type="text"]:nth-of-type(2)').value.trim();
        var mail = fieldsContainer.querySelector('input[type="email"]').value.trim();
        var mobil = fieldsContainer.querySelector('input[type="tel"]').value.trim();
        bodyParts += '\n\n--- Levering ---\n' +
            'Navn: ' + navn + '\n' +
            'Adresse: ' + adresse + '\n' +
            'Mail: ' + mail + '\n' +
            'Mobil: ' + mobil;
    }

    var emne = encodeURIComponent('Ny forespørgsel: Æresportskilt.dk');
    var body = encodeURIComponent(bodyParts);
    window.location.href = 'mailto:Thomsen2@gmail.com?subject=' + emne + '&body=' + body;
}
