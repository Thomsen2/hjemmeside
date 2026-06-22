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

document.getElementById('signForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var besked = document.getElementById('besked').value.trim();
    var navn = document.getElementById('navn').value.trim();
    var adresse = document.getElementById('adresse').value.trim();
    var mail = document.getElementById('mail').value.trim();
    var mobil = document.getElementById('mobil').value.trim();

    if (!besked || !navn || !adresse || !mail || !mobil) {
        alert('Udfyld venligst alle felter.');
        return;
    }

    var emne = encodeURIComponent('Ny forespørgsel: Æresportskilt');
    var body = encodeURIComponent(
        'Ny forespørgsel på æresportskilt\n\n' +
        'Navn: ' + navn + '\n' +
        'Adresse: ' + adresse + '\n' +
        'Mail: ' + mail + '\n' +
        'Mobil: ' + mobil + '\n' +
        'Besked: ' + besked + '\n\n' +
        'Pris: 199 kr.'
    );

    window.location.href = 'mailto:info@aeresportskilt.dk?subject=' + emne + '&body=' + body;
});
