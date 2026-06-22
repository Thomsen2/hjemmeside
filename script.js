const text1Input = document.getElementById('text1');
const text2Input = document.getElementById('text2');
const text3Input = document.getElementById('text3');
const signLine1 = document.getElementById('signLine1');
const signLine2 = document.getElementById('signLine2');
const signLine3 = document.getElementById('signLine3');

function updatePreview() {
    signLine1.textContent = text1Input.value.trim() || 'Tillykke';
    signLine2.textContent = text2Input.value.trim() || 'Navn';
    signLine3.textContent = text3Input.value.trim() || '2024';
}

text1Input.addEventListener('input', updatePreview);
text2Input.addEventListener('input', updatePreview);
text3Input.addEventListener('input', updatePreview);

document.getElementById('signForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const navn = text1Input.value.trim();
    const dato = text2Input.value.trim();
    const aarstal = text3Input.value.trim();
    const antal = document.getElementById('antal').value;
    const besked = document.getElementById('besked').value.trim();

    if (!navn || !dato || !aarstal) {
        alert('Udfyld venligst alle felter.');
        return;
    }

    const emne = encodeURIComponent('Ny forespørgsel: Æresportskilt');
    const body = encodeURIComponent(
        'Ny forespørgsel på æresportskilt\n\n' +
        'Linie 1: ' + navn + '\n' +
        'Navn: ' + dato + '\n' +
        'Årstal: ' + aarstal + '\n' +
        'Antal: ' + antal + '\n' +
        'Besked: ' + (besked || '(ingen)') + '\n\n' +
        'Pris: ' + (antal * 249) + ' kr.'
    );

    window.location.href = 'mailto:info@aeresportskilt.dk?subject=' + emne + '&body=' + body;
});
