document.getElementById('signForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const besked = document.getElementById('besked').value.trim();

    if (!besked) {
        alert('Udfyld venligst din besked.');
        return;
    }

    const emne = encodeURIComponent('Ny forespørgsel: Æresportskilt');
    const body = encodeURIComponent(
        'Ny forespørgsel på æresportskilt\n\n' +
        'Besked: ' + besked + '\n\n' +
        'Pris: 249 kr.'
    );

    window.location.href = 'mailto:info@aeresportskilt.dk?subject=' + emne + '&body=' + body;
});
