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

document.querySelectorAll('.sign-photo').forEach(function (img) {
    img.style.cursor = 'pointer';
    img.addEventListener('click', function () {
        window.open(this.src, '_blank');
    });
});
