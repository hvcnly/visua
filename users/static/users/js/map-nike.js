// map-nike.js
// Uso: initNikeMap('mapNike', '/static/users/data/comunas.geojson')

function initNikeMap(targetId, geoUrl){
  // --- Datos fijos POR COMUNA (tu reparto) ---
  const ventas = [
    { comuna: "Las Condes",  total: 48, mujeres: 32, hombres: 16,
      detalle: [{mall:"Alto Las Condes", v:27},{mall:"Parque Arauco", v:23},{mall:"Plaza Los Dominicos", v:11}] },
    { comuna: "Ñuñoa",       total: 20, mujeres:  7, hombres: 13,
      detalle: [{mall:"Plaza Egaña", v:4}] },
    { comuna: "Cerrillos",   total:  8, mujeres:  4, hombres:  4,
      detalle: [{mall:"Plaza Oeste", v:1}] },
    { comuna: "Maipú",       total: 10, mujeres:  8, hombres:  2,
      detalle: [{mall:"Arauco Maipú", v:4}] },
    { comuna: "Huechuraba",  total:  7, mujeres:  6, hombres:  1,
      detalle: [{mall:"Plaza Norte", v:4}] },
    { comuna: "La Florida",  total:  8, mujeres:  3, hombres:  5,
      detalle: [{mall:"Plaza Vespucio", v:2},{mall:"Florida Center", v:1}] },
    { comuna: "Providencia", total: 52, mujeres: 20, hombres: 32,
      detalle: [{mall:"Costanera Center", v:8}] },
  ];

  const normalize = s => s?.toString().trim().toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\s+/g,' ') ?? '';
  const ventasByName = new Map(ventas.map(d => [normalize(d.comuna), d]));

  // --- Escala de color ---
  const valores = ventas.map(d => d.total);
  const minV = Math.min(...valores);
  const maxV = Math.max(...valores);
  const ramp = ['#fff7ec','#fdd49e','#fdbb84','#ef6548','#990000'];
  const lerp = (a,b,t) => a + (b-a)*t;
  const hexToRgb = h => { const n=h.replace('#',''); return [parseInt(n.slice(0,2),16),parseInt(n.slice(2,4),16),parseInt(n.slice(4,6),16)];};
  const rgbToHex = (r,g,b) => '#'+[r,g,b].map(x=>x.toString(16).padStart(2,'0')).join('');
  function interpColor(colors, t){
    t = Math.max(0, Math.min(1, t));
    const i = Math.floor(t*(colors.length-1));
    const j = Math.min(colors.length-1, i+1);
    const localT = (t*(colors.length-1)) - i;
    const c1 = hexToRgb(colors[i]), c2 = hexToRgb(colors[j]);
    const r = Math.round(lerp(c1[0], c2[0], localT));
    const g = Math.round(lerp(c1[1], c2[1], localT));
    const b = Math.round(lerp(c1[2], c2[2], localT));
    return rgbToHex(r,g,b);
  }
  function getColor(v){
    if (v == null || maxV === minV) return '#444';
    const t = (v - minV) / (maxV - minV + 1e-9);
    return interpColor(ramp, t);
  }

  // --- Mapa base (tema oscuro) ---
  // evita el error "Cannot redeclare ..." si recargas el script
  if (window.__nikeMap) { try { window.__nikeMap.remove(); } catch(e){} }
  const map = L.map(targetId, { zoomControl: false }).setView([-33.45, -70.65], 11);
  window.__nikeMap = map;

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{
    maxZoom: 19, attribution: '&copy; OpenStreetMap & Carto'
  }).addTo(map);
  L.control.zoom({ position: 'bottomleft' }).addTo(map);

  // --- Estilo de etiquetas ---
  const styleTag = document.createElement('style');
  styleTag.innerHTML = `
    .legend { background:#111;color:#eee;padding:8px 10px;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.4); }
    .legend i { width:14px;height:14px;float:left;margin-right:6px;opacity:.95; }
    .leaflet-tooltip.comuna-label {
      background: transparent; border: none; box-shadow: none;
      color: #ffffff; font-weight: 600; font-size: 12px;
      text-shadow: 0 0 3px rgba(0,0,0,.9), 0 0 8px rgba(0,0,0,.7);
      pointer-events: none;
    }`;
  document.head.appendChild(styleTag);

  // --- Carga GeoJSON y pintado ---
  fetch(geoUrl).then(r => r.json()).then(geo => {
    const getRegion = p => p.NOM_REGION || p.Region || p.REGION || p.NOMBRE_REGI || p.NOM_REG || '';
    const getNombreComuna = p => p.NOM_COMUNA || p.Comuna || p.COMUNA || p.nombre || p.NOM_COM || '';

    // Filtrar Región Metropolitana
    const geoRM = { ...geo, features: geo.features.filter(f => normalize(getRegion(f.properties)).includes('metropolitana')) };

    const capa = L.geoJSON(geoRM, {
      style: f => {
        const d = ventasByName.get(normalize(getNombreComuna(f.properties)));
        return { fillColor: getColor(d?.total), color:'#222', weight:1, fillOpacity:0.85 };
      },
      onEachFeature: (f, layer) => {
        const nombre = getNombreComuna(f.properties);
        const d = ventasByName.get(normalize(nombre));

        const detalleHTML = d?.detalle?.length
          ? `<ul style="margin:6px 0 0 18px;padding:0;">${d.detalle.map(x=>`<li>${x.mall}: <b>${x.v}</b></li>`).join('')}</ul>`
          : '<i>Sin detalle</i>';

        // id seguro para el canvas del popup
        const canvasId = `gender-${normalize(nombre).replace(/\s+/g,'-')}`;

        layer.bindPopup(`
          <div style="min-width:240px;color:#111">
            <div style="font-weight:700">${nombre}</div>
            <div>Total personas: <b>${d?.total ?? 'Sin datos'}</b></div>
            <div style="margin-top:6px;">Malls:</div>${detalleHTML}
            <div style="margin-top:10px;">Género (comuna):</div>
            <canvas id="${canvasId}" width="150" height="150"></canvas>
          </div>
        `);

        layer.on('popupopen', function() {
          // dibuja el donut SOLO con totales de la comuna
          const el = document.getElementById(canvasId);
          if (!el || !window.Chart || !d) return;
          const ctx = el.getContext('2d');
          // pequeña espera para asegurar layout del popup
          setTimeout(() => {
            new Chart(ctx, {
              type: 'doughnut',
              data: {
                labels: ['Mujeres', 'Hombres'],
                datasets: [{
                  data: [d.mujeres || 0, d.hombres || 0],
                  backgroundColor: ['#ff6f00', '#007bff'],
                  borderColor: ['#ffffff', '#ffffff'],
                  borderWidth: 2
                }]
              },
              options: {
                responsive: true,
                plugins: { legend: { position: 'top', labels: { color: '#111' } } },
                aspectRatio: 1
              }
            });
          }, 80);
        });

        layer.on({
          mouseover: e => e.target.setStyle({weight:2, color:'#ff6f00'}),
          mouseout:  e => capa.resetStyle(e.target)
        });

        const center = layer.getBounds().getCenter();
        layer.bindTooltip(nombre, { permanent:true, direction:'center', className:'comuna-label' }).openTooltip();
        layer.getTooltip().setLatLng(center);
      }
    }).addTo(map);

    map.fitBounds(capa.getBounds(), {padding:[12,12]});

    // Leyenda
    const legend = L.control({position:'bottomright'});
    legend.onAdd = function(){
      const div = L.DomUtil.create('div','legend');
      div.innerHTML += '<b>Personas por comuna</b><br>';
      const ticks = 6;
      for (let k=0;k<ticks;k++){
        const t = k/(ticks-1);
        const v = Math.round(minV + t*(maxV - minV));
        div.innerHTML += `<i style="background:${interpColor(ramp,t)}"></i> ${v.toLocaleString('es-CL')}<br>`;
      }
      return div;
    };
    legend.addTo(map);
  }).catch(err => {
    console.error('Error cargando GeoJSON:', err);
    alert('No se pudo cargar el archivo GeoJSON. Revisa la ruta en static().');
  });
}
