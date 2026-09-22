document.querySelectorAll("[data-t0]").forEach((el) => {
  const t0 = new Date(el.dataset.t0);
  const pad = (n) => String(n).padStart(2, "0");

  const tick = () => {
    const diff = t0 - Date.now();
    if (diff <= 0) {
      el.textContent = gettext("T-0 has arrived 🚀");
      return;
    }
    const days = Math.floor(diff / 86400000);
    const hours = Math.floor(diff / 3600000) % 24;
    const minutes = Math.floor(diff / 60000) % 60;
    const seconds = Math.floor(diff / 1000) % 60;
    el.textContent = interpolate(gettext("T-%(days)sd %(time)s"), {
      days: days,
      time: `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`,
    }, true);
    setTimeout(tick, 1000);
  };

  tick();
});
