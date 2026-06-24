// ---------- Scroll reveal animations ----------
document.addEventListener("DOMContentLoaded", () => {
  const revealEls = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealEls.forEach((el) => observer.observe(el));

  initCountdown();
  initLangToggle();
  initMusicToggle();
  initGalleryLightbox();
  initQrToggle();
  initRsvpForm();
  initAddToCalendar();
});

// ---------- Countdown ----------
function initCountdown() {
  const root = document.getElementById("countdown");
  if (!root) return;
  const targetDate = new Date(root.dataset.target);
  const dayEl = document.getElementById("cd-days");
  const hourEl = document.getElementById("cd-hours");
  const minEl = document.getElementById("cd-mins");
  const secEl = document.getElementById("cd-secs");

  function toKhmerDigits(num) {
    const map = ["០", "១", "២", "៣", "៤", "៥", "៦", "៧", "៨", "៩"];
    return String(num)
      .split("")
      .map((d) => (map[d] !== undefined ? map[d] : d))
      .join("");
  }

  function tick() {
    const now = new Date();
    let diff = Math.max(0, targetDate - now);
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const mins = Math.floor((diff / (1000 * 60)) % 60);
    const secs = Math.floor((diff / 1000) % 60);
    if (dayEl) dayEl.textContent = toKhmerDigits(days);
    if (hourEl) hourEl.textContent = toKhmerDigits(hours);
    if (minEl) minEl.textContent = toKhmerDigits(mins);
    if (secEl) secEl.textContent = toKhmerDigits(secs);
  }
  tick();
  setInterval(tick, 1000);
}

// ---------- KM / EN toggle ----------
function initLangToggle() {
  const btn = document.getElementById("lang-toggle");
  if (!btn) return;
  let lang = "km";
  btn.addEventListener("click", () => {
    lang = lang === "km" ? "en" : "km";
    document.querySelectorAll("[data-km]").forEach((el) => {
      const text = lang === "km" ? el.dataset.km : el.dataset.en || el.dataset.km;
      el.textContent = text;
    });
    btn.textContent = lang === "km" ? "EN" : "ខ្មែរ";
  });
}

// ---------- Background music ----------
function initMusicToggle() {
  const audio = document.getElementById("bg-music");
  const btn = document.getElementById("music-toggle");
  if (!audio || !btn) return;
  let playing = false;
  btn.addEventListener("click", () => {
    if (playing) {
      audio.pause();
      btn.textContent = "♪ Play";
    } else {
      audio.play().catch(() => {});
      btn.textContent = "❙❙ Pause";
    }
    playing = !playing;
  });
}

// ---------- Gallery lightbox ----------
function initGalleryLightbox() {
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  if (!lightbox || !lightboxImg) return;
  document.querySelectorAll(".gallery-grid img").forEach((img) => {
    img.addEventListener("click", () => {
      lightboxImg.src = img.src;
      lightbox.classList.add("open");
    });
  });
  lightbox.addEventListener("click", () => {
    lightbox.classList.remove("open");
    lightboxImg.src = "";
  });
}

// ---------- KHQR toggle ----------
function initQrToggle() {
  const usdBtn = document.getElementById("qr-usd-btn");
  const khrBtn = document.getElementById("qr-khr-btn");
  const img = document.getElementById("qr-image");
  if (!usdBtn || !khrBtn || !img) return;
  const usdSrc = img.dataset.usd;
  const khrSrc = img.dataset.khr;

  usdBtn.addEventListener("click", () => {
    img.src = usdSrc;
    usdBtn.classList.add("active");
    khrBtn.classList.remove("active");
  });
  khrBtn.addEventListener("click", () => {
    img.src = khrSrc || usdSrc;
    khrBtn.classList.add("active");
    usdBtn.classList.remove("active");
  });
}

// ---------- RSVP (static site: no server, so this opens a pre-filled email) ----------
function initRsvpForm() {
  const form = document.getElementById("rsvp-form");
  if (!form) return;
  const attendBtn = document.getElementById("rsvp-attend");
  const declineBtn = document.getElementById("rsvp-decline");
  const statusInput = document.getElementById("rsvp-status");
  const errorEl = document.getElementById("rsvp-error");
  const contactEmail = form.dataset.contactEmail || "";

  let status = "attend";
  attendBtn.classList.add("selected", "attend");

  attendBtn.addEventListener("click", () => {
    status = "attend";
    statusInput.value = status;
    attendBtn.classList.add("selected", "attend");
    declineBtn.classList.remove("selected", "decline");
  });
  declineBtn.addEventListener("click", () => {
    status = "decline";
    statusInput.value = status;
    declineBtn.classList.add("selected", "decline");
    attendBtn.classList.remove("selected", "attend");
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    errorEl.textContent = "";
    const name = form.querySelector("[name='name']").value.trim();
    const message = form.querySelector("[name='message']").value.trim();
    if (!name || !message) {
      errorEl.textContent = "សូមបញ្ចូលឈ្មោះ និងសារជូនពរ";
      return;
    }
    const statusLabel = status === "attend" ? "ចូលរួម (Attending)" : "បដិសេធ (Not attending)";
    const subject = encodeURIComponent("RSVP - " + name);
    const body = encodeURIComponent(
      `ឈ្មោះ / Name: ${name}\nស្ថានភាព / Status: ${statusLabel}\n\nសារ / Message:\n${message}`
    );
    window.location.href = `mailto:${contactEmail}?subject=${subject}&body=${body}`;
    appendWish({ name, message });
    form.reset();
    statusInput.value = status;
  });
}

function appendWish(msg) {
  const wall = document.getElementById("wishes-wall");
  const emptyState = document.getElementById("empty-wishes");
  if (emptyState) emptyState.remove();
  if (!wall) return;
  const div = document.createElement("div");
  div.className = "wish-item";
  div.innerHTML = `<span class="wish-name">${escapeHtml(msg.name)}</span><div class="wish-text">${escapeHtml(
    msg.message
  )}</div>`;
  wall.prepend(div);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---------- Add to calendar ----------
function initAddToCalendar() {
  const btn = document.getElementById("add-calendar");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const iso = btn.dataset.datetime;
    if (!iso) return;
    const start = new Date(iso);
    const end = new Date(start.getTime() + 2 * 60 * 60 * 1000);
    const fmt = (d) => d.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    const title = encodeURIComponent(btn.dataset.title || "Wedding");
    const location = encodeURIComponent(btn.dataset.location || "");
    const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${fmt(
      start
    )}/${fmt(end)}&location=${location}`;
    window.open(url, "_blank");
  });
}
