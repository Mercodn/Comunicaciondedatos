document.addEventListener('DOMContentLoaded', () => {
  fetch('/obtener_reportes')
    .then(r => r.json())
    .then(data => {
      // total
      const total = Array.isArray(data) ? data.length : 0;
      const elTotal = document.getElementById('kpi-total');
      if (elTotal) elTotal.textContent = total;

      // calcular últimos 7 días intentando parsear "dd/mm/YYYY" del backend
      function parseFecha(fechaStr){
        if (!fechaStr) return null;
        const datePart = fechaStr.split(',')[0].trim(); // "dd/mm/YYYY"
        const parts = datePart.split('/');
        if (parts.length < 3) return null;
        const d = parseInt(parts[0],10), m = parseInt(parts[1],10)-1, y = parseInt(parts[2],10);
        return new Date(y, m, d);
      }
      const now = new Date();
      const last7count = data.filter(d=>{
        const dt = parseFecha(d.fecha_hora);
        if (!dt) return false;
        return (now - dt) <= 7*24*3600*1000;
      }).length;
      const elWeek = document.getElementById('kpi-week');
      if (elWeek) elWeek.textContent = last7count;

      // llenar tabla de recientes usuario
      const tbody = document.querySelector('#recentReports tbody');
      if (tbody){
        tbody.innerHTML = data.slice(-10).reverse().map(r=>`<tr><td>${r.tipo}</td><td>${r.fecha_hora}</td><td>${r.municipio}</td></tr>`).join('');
      }

      // llenar tabla admin
      const adminTbody = document.querySelector('#adminReports tbody');
      if (adminTbody){
        adminTbody.innerHTML = data.slice(-15).reverse().map((r,i)=>`<tr><td>${i+1}</td><td>${r.tipo}</td><td>${r.fecha_hora}</td><td>${r.municipio}</td></tr>`).join('');
      }

      // KPIs admin (usuarios no disponible aún)
      const kpireports = document.getElementById('kpi-reports');
      if (kpireports) kpireports.textContent = total;
    })
    .catch(err => {
      console.warn('No se pudieron cargar reportes:', err);
    });
});