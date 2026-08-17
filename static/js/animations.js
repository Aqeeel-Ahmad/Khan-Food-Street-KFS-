/* KFS Khan Food Street Animations & Interactivity */

document.addEventListener('DOMContentLoaded', () => {
  // 1. GSAP ScrollReveals
  if (typeof gsap !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Hero elements entry
    gsap.from(".hero-title", {
      duration: 1.2,
      y: 50,
      opacity: 0,
      ease: "back.out(1.7)"
    });

    gsap.from(".hero-subtitle", {
      duration: 1,
      y: 30,
      opacity: 0,
      delay: 0.3,
      ease: "power2.out"
    });

    gsap.from(".hero-mascot", {
      duration: 1.4,
      scale: 0.7,
      opacity: 0,
      delay: 0.4,
      ease: "elastic.out(1, 0.5)"
    });

    // Reveal elements on scroll
    const revealElements = document.querySelectorAll(".gsap-reveal");
    revealElements.forEach((el) => {
      gsap.from(el, {
        scrollTrigger: {
          trigger: el,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        y: 40,
        opacity: 0,
        duration: 0.8,
        ease: "power2.out"
      });
    });
  }

  // 2. Countdown Timer for Friday Kabuli Pulao Special
  initCountdownTimer();

  // 3. 3D Tilt Effect on Food Cards
  initTiltEffect();

  // 4. Gallery Lightbox Modal
  initLightbox();
});

// Friday Special Countdown Timer
function initCountdownTimer() {
  const hoursEl = document.getElementById("cd-hours");
  const minsEl = document.getElementById("cd-mins");
  const secsEl = document.getElementById("cd-secs");

  if (!hoursEl || !minsEl || !secsEl) return;

  let totalSeconds = 14 * 3600 + 45 * 60 + 22; // 14 hours 45 mins countdown seed

  setInterval(() => {
    if (totalSeconds <= 0) {
      totalSeconds = 24 * 3600; // reset loop
    } else {
      totalSeconds--;
    }

    const hours = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;

    hoursEl.textContent = hours < 10 ? '0' + hours : hours;
    minsEl.textContent = mins < 10 ? '0' + mins : mins;
    secsEl.textContent = secs < 10 ? '0' + secs : secs;
  }, 1000);
}

// 3D Card Tilt Effect
function initTiltEffect() {
  const cards = document.querySelectorAll(".tilt-card");
  cards.forEach(card => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -8;
      const rotateY = ((x - centerX) / centerX) * 8;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)";
    });
  });
}

// Gallery Lightbox Modal
function initLightbox() {
  const modal = document.getElementById("lightbox-modal");
  const modalImg = document.getElementById("lightbox-img");
  const modalTitle = document.getElementById("lightbox-title");
  const closeBtn = document.getElementById("lightbox-close");

  if (!modal || !modalImg) return;

  document.querySelectorAll(".gallery-item").forEach(item => {
    item.addEventListener("click", () => {
      const imgSrc = item.dataset.img;
      const title = item.dataset.title || 'KFS Gallery';

      modalImg.src = imgSrc;
      if (modalTitle) modalTitle.textContent = title;
      modal.classList.remove("hidden");
      modal.classList.add("flex");
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
    });
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
    }
  });
}

// WhatsApp Direct Order Helper
function orderOnWhatsApp(itemName, price) {
  const phone = "923442041131";
  const text = encodeURIComponent(`Hi KFS! I want to order "${itemName}" (Rs ${price}). Please confirm my order details!`);
  window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
}
