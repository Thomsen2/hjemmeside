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

    var besked = document.getElementById('besked').value.trim();
    var shippingChecked = this.querySelector('.shipping-toggle').checked;
    var pickupChecked = this.querySelector('.pickup-toggle').checked;

    if (!besked) {
        alert('Udfyld venligst din besked.');
        return;
    }

    var bodyParts = 'Ny forespørgsel på æresportskilt\n\n' +
        'Besked: ' + besked + '\n' +
        'Pris: 199 kr.';

    if (pickupChecked) {
        bodyParts += '\n\nAfhentning: Dragør';
    }
    if (shippingChecked) {
        var navn = document.getElementById('navn').value.trim();
        var adresse = document.getElementById('adresse').value.trim();
        var mail = document.getElementById('mail').value.trim();
        var mobil = document.getElementById('mobil').value.trim();
        bodyParts += '\n\n--- Levering ---\n' +
            'Navn: ' + navn + '\n' +
            'Adresse: ' + adresse + '\n' +
            'Mail: ' + mail + '\n' +
            'Mobil: ' + mobil + '\n' +
            'Fragt: 55 kr.';
    }

    var emne = encodeURIComponent('Ny forespørgsel: Æresportskilt');
    var body = encodeURIComponent(bodyParts);
    window.location.href = 'mailto:info@aeresportskilt.dk?subject=' + emne + '&body=' + body;
});
