document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reportForm');
  const btnGet = document.getElementById('btnGetLoc');
  const latInput = document.getElementById('latitud');
  const lngInput = document.getElementById('longitud');
  const msg = document.getElementById('msg');

  btnGet.addEventListener('click', () => {
    msg.textContent = 'Obteniendo ubicación…';
    if (!navigator.geolocation) {
      msg.textContent = 'Geolocalización no soportada en este navegador.';
      return;
    }
    navigator.geolocation.getCurrentPosition(pos => {
      latInput.value = pos.coords.latitude.toFixed(6);
      lngInput.value = pos.coords.longitude.toFixed(6);
      msg.textContent = 'Ubicación obtenida.';
    }, err => {
      msg.textContent = 'Error al obtener ubicación: ' + err.message;
    }, { enableHighAccuracy: true, timeout: 10000 });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    msg.textContent = '';

    const tipo = document.getElementById('tipo').value;
    const descripcion = document.getElementById('descripcion').value.trim();
    const latitud = latInput.value;
    const longitud = lngInput.value;

    if (!tipo || !descripcion || !latitud || !longitud) {
      msg.style.color = '#a00';
      msg.textContent = 'Completa todos los campos y obtén la ubicación.';
      return;
    }

    fetch('/reportar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tipo, descripcion, latitud, longitud })
    })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        msg.style.color = '#a00';
        msg.textContent = 'Error: ' + data.error;
      } else {
        msg.style.color = '#1f7a1f';
        msg.textContent = data.mensaje + (data.municipio ? ` Municipio: ${data.municipio}` : '');
        form.reset();
        latInput.value = '';
        lngInput.value = '';
      }
    })
    .catch(err => {
      msg.style.color = '#a00';
      msg.textContent = 'Error al enviar: ' + err.message;
    });
  });
});
