(function () {
  const container = document.getElementById("spots-map");
  const data = document.getElementById("map-points");
  if (!container || !data || typeof L === "undefined") return;

  const points = JSON.parse(data.textContent);
  if (!points.length) return;

  const map = L.map(container);
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    maxZoom: 19,
    subdomains: "abcd",
    detectRetina: true,
    attribution:
      '&copy; участники <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, ' +
      'тайлы &copy; <a href="https://carto.com/attributions">CARTO</a>',
  }).addTo(map);

  const markers = points.map((point) => {
    const link = document.createElement("a");
    link.href = point.url;
    link.textContent = point.title;
    return L.marker([point.lat, point.lng]).bindPopup(link);
  });

  const group = L.featureGroup(markers).addTo(map);
  map.fitBounds(group.getBounds().pad(0.3), { maxZoom: 12 });
})();
