document.getElementById('signForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const besked = document.getElementById('besked').value.trim();
    const navn = document.getElementById('navn').value.trim();
    const adresse = document.getElementById('adresse').value.trim();
    const mail = document.getElementById('mail').value.trim();
    const mobil = document.getElementById('mobil').value.trim();

    if (!besked || !navn || !adresse || !mail || !mobil) {
        alert('Udfyld venligst alle felter.');
        return;
    }

    const emne = encodeURIComponent('Ny forespørgsel: Æresportskilt');
    const body = encodeURIComponent(
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
