// 🗺️ Inicializar el mapa centrado en Sabana Centro
const map = L.map('map', {
  minZoom: 12,
  maxZoom: 24, // 🔍 zoom alto permitido
  maxBounds: [
    [5.2, -73.9],  // Norte-Este aproximado
    [4.6, -74.3]   // Sur-Oeste aproximado
  ],
  maxBoundsViscosity: 1.0 // 🔒 impide salir de Sabana Centro
}).setView([4.916, -74.031], 18); // 🎯 vista inicial centrada

// 🌍 Capa base de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors',
  maxZoom: 24
}).addTo(map);

// ⚙️ Variables globales
let ubicacionManual = false;
let marcador = null;
let userLat = null;
let userLng = null;

// 📍 Intentar obtener ubicación automática
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat = pos.coords.latitude;
      userLng = pos.coords.longitude;
      marcador = L.marker([userLat, userLng]).addTo(map);
      map.setView([userLat, userLng], 20);
      document.getElementById('latitud').value = userLat;
      document.getElementById('longitud').value = userLng;
    },
    (err) => {
      console.warn("Error de geolocalización:", err);
      alert("⚠️ No se pudo obtener tu ubicación. Usa la opción manual.");
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
} else {
  alert("⚠️ Tu navegador no soporta geolocalización. Usa la opción manual.");
}

// 🖱️ Permitir seleccionar manualmente en el mapa
map.on('click', (e) => {
  if (ubicacionManual) {
    const { lat, lng } = e.latlng;
    if (marcador) map.removeLayer(marcador);
    marcador = L.marker([lat, lng]).addTo(map);
    map.setView([lat, lng], 20);
    document.getElementById('latitud').value = lat;
    document.getElementById('longitud').value = lng;
    ubicacionManual = false;
    alert(`📍 Ubicación seleccionada: ${lat.toFixed(5)}, ${lng.toFixed(5)}`);
  }
});

// 🔘 Botón “Seleccionar ubicación manualmente”
function activarModoManual() {
  ubicacionManual = true;
  alert("🗺️ Haz clic en el mapa para establecer la ubicación del incidente.");
}

// 🧾 Manejar el formulario
const form = document.getElementById('formularioAlerta');
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const tipo = document.getElementById('tipo').value;
  const latitud = parseFloat(document.getElementById('latitud').value);
  const longitud = parseFloat(document.getElementById('longitud').value);
  const descripcion = document.getElementById('descripcion').value;

  if (!latitud || !longitud) {
    alert("⚠️ Debes seleccionar una ubicación antes de reportar.");
    return;
  }

  const nuevoReporte = { tipo, latitud, longitud, descripcion };

  const res = await fetch('/reportar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(nuevoReporte)
  });

  if (res.ok) {
    alert('✅ Incidente reportado con éxito');
    L.marker([latitud, longitud])
      .addTo(map)
      .bindPopup(`⚠️ <b>${tipo}</b><br>${descripcion}`);
    form.reset();
  } else {
    alert('❌ Error al enviar el reporte');
  }
});
