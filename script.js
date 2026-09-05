'use strict';

/* ============================================================================
   HAMZA OCEAN SEAFOOD — script.js
   ============================================================================
   BUILD STAGE 3 OF 3 (FINAL). HTML and CSS are approved — this file only
   adds behaviour, it does not rely on anything that isn't already in the
   markup/stylesheet.

   PLACEHOLDERS TO REPLACE BEFORE LAUNCH:
   • WHATSAPP_NUMBER (below)         → real WhatsApp number, digits only
   • WEB3FORMS_ACCESS_KEY (below)    → real Web3Forms access key
     (the contact form already carries its own access_key hidden field in
     index.html — this constant is only used to submit the newsletter form,
     which has no backend of its own.)

   TABLE OF CONTENTS
   01. Constants & small utilities
   02. Current year (footer)
   03. Mobile drawer navigation
   04. Scroll effects (header state, back-to-top, light hero parallax)
   05. Active section highlighting (scrollspy)
   06. Scroll-reveal animations (fade up / left / right / scale)
   07. Button ripple micro-interaction
   08. Product quantity selectors (custom qty toggle)
   09. Product "Order on WhatsApp" buttons
   10. Contact form (Web3Forms)
   11. Newsletter form (Web3Forms)
   12. Vimeo video players (hero background + process section)
   13. Bootstrap
   ============================================================================ */

/* ============================================================================
   01. CONSTANTS & SMALL UTILITIES
   ============================================================================ */
const WHATSAPP_NUMBER = '92XXXXXXXXXX'; // TODO: replace with real number (no +, no spaces)
const WEB3FORMS_ACCESS_KEY = 'YOUR_WEB3FORMS_ACCESS_KEY'; // TODO: replace — used for the newsletter form only
const WEB3FORMS_ENDPOINT = 'https://api.web3forms.com/submit';
const HERO_VIMEO_VIDEO_ID = '1223735891' // TODO: replace with real Vimeo video ID for the hero background

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/** Fires a GA4 event if gtag is present; silently does nothing otherwise. */
function trackEvent(eventName, params) {
  if (typeof gtag === 'function') {
    gtag('event', eventName, params || {});
  }
}

/** Shows a success/error message in one of the form feedback paragraphs. */
function showFormMessage(el, message, isError) {
  if (!el) return;
  el.textContent = message;
  el.hidden = false;
  el.classList.toggle('is-error', Boolean(isError));
}

/* ============================================================================
   02. CURRENT YEAR (FOOTER)
   ============================================================================ */
function initCurrentYear() {
  const el = document.getElementById('currentYear');
  if (el) el.textContent = new Date().getFullYear();
}

/* ============================================================================
   03. MOBILE DRAWER NAVIGATION
   ============================================================================ */
function initMobileDrawer() {
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const drawer = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('drawerOverlay');
  const closeBtn = document.getElementById('drawerCloseBtn');

  if (!hamburgerBtn || !drawer || !overlay) return;

  const drawerLinks = drawer.querySelectorAll('a');

  function openDrawer() {
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    overlay.hidden = false;
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('no-scroll');
    if (closeBtn) closeBtn.focus();
  }

  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    overlay.hidden = true;
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('no-scroll');
  }

  hamburgerBtn.addEventListener('click', () => {
    const isOpen = drawer.classList.contains('is-open');
    if (isOpen) {
      closeDrawer();
      hamburgerBtn.focus();
    } else {
      openDrawer();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      closeDrawer();
      hamburgerBtn.focus();
    });
  }

  overlay.addEventListener('click', () => {
    closeDrawer();
    hamburgerBtn.focus();
  });

  // Tapping any link inside the drawer (nav links + WhatsApp CTA) closes it,
  // letting the anchor's own navigation/smooth-scroll proceed normally.
  drawerLinks.forEach((link) => {
    link.addEventListener('click', closeDrawer);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && drawer.classList.contains('is-open')) {
      closeDrawer();
      hamburgerBtn.focus();
    }
  });

  // Minimal focus trap while the drawer is open
  drawer.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab' || !drawer.classList.contains('is-open')) return;
    const focusable = drawer.querySelectorAll('a[href], button:not([disabled])');
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
}

/* ============================================================================
   04. SCROLL EFFECTS (header shadow/solid state, back-to-top, light parallax)
   ============================================================================ */
function initScrollEffects() {
  const header = document.getElementById('siteHeader');
  const backToTopBtn = document.getElementById('backToTopBtn');
  const heroImage = document.querySelector('.hero-bg-image');
  const hero = document.querySelector('.hero');

  const HEADER_THRESHOLD = 60;
  const BACK_TO_TOP_THRESHOLD = 480;
  const PARALLAX_STRENGTH = 0.15;

  let heroHeight = hero ? hero.offsetHeight : 0;
  let ticking = false;

  function update() {
    const scrollY = window.scrollY;

    if (header) {
      header.classList.toggle('is-scrolled', scrollY > HEADER_THRESHOLD);
    }
    if (backToTopBtn) {
      backToTopBtn.hidden = scrollY < BACK_TO_TOP_THRESHOLD;
    }
    if (heroImage && !prefersReducedMotion && scrollY < heroHeight) {
      heroImage.style.transform = `translateY(${scrollY * PARALLAX_STRENGTH}px)`;
    }
    ticking = false;
  }

  function requestUpdate() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', () => {
    heroHeight = hero ? hero.offsetHeight : 0;
  }, { passive: true });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    });
  }

  update(); // set correct state immediately (e.g. on a mid-page reload)
}

/* ============================================================================
   05. ACTIVE SECTION HIGHLIGHTING (SCROLLSPY)
   ============================================================================ */
function initActiveNavHighlight() {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  if (!sections.length || !navLinks.length || !('IntersectionObserver' in window)) return;

  function setActive(hash) {
    navLinks.forEach((link) => {
      link.classList.toggle('is-active', link.getAttribute('href') === hash);
    });
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActive(`#${entry.target.id}`);
        }
      });
    },
    { rootMargin: '-40% 0px -55% 0px', threshold: 0 }
  );

  sections.forEach((section) => observer.observe(section));
}

/* ============================================================================
   06. SCROLL-REVEAL ANIMATIONS
   ============================================================================
   Classes are added here at runtime (not present in the static HTML), so
   with JavaScript disabled every element simply renders at full opacity —
   no broken/invisible content, just no entrance animation.
*/
function initScrollReveal() {
  const revealMap = [
    { selector: '.section-header', className: 'reveal' },
    { selector: '.products-grid .product-card', className: 'reveal' },
    { selector: '.products-note', className: 'reveal' },
    { selector: '.values-grid .value-card', className: 'reveal' },
    { selector: '.process-video-card', className: 'reveal-scale' },
    { selector: '.process-timeline .process-step', className: 'reveal' },
    { selector: '.faq-item', className: 'reveal' },
    { selector: '.about-media', className: 'reveal-left' },
    { selector: '.about-content', className: 'reveal-right' },
    { selector: '.contact-info', className: 'reveal-left' },
    { selector: '.contact-form-wrap', className: 'reveal-right' },
    { selector: '.reviews-inner', className: 'reveal-scale' },
    { selector: '.newsletter-inner', className: 'reveal-scale' },
  ];

  const elements = [];
  revealMap.forEach(({ selector, className }) => {
    document.querySelectorAll(selector).forEach((el) => {
      el.classList.add(className);
      elements.push(el);
    });
  });

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    elements.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
  );

  elements.forEach((el) => observer.observe(el));
}

/* ============================================================================
   07. BUTTON RIPPLE MICRO-INTERACTION
   ============================================================================ */
function initButtonRipple() {
  if (prefersReducedMotion) return;

  document.addEventListener('click', (event) => {
    const btn = event.target.closest('.btn');
    if (!btn) return;

    const rect = btn.getBoundingClientRect();
    btn.style.setProperty('--ripple-x', `${event.clientX - rect.left}px`);
    btn.style.setProperty('--ripple-y', `${event.clientY - rect.top}px`);

    btn.classList.remove('is-rippling');
    void btn.offsetWidth; // force reflow so the animation restarts on rapid clicks
    btn.classList.add('is-rippling');

    btn.addEventListener('animationend', () => btn.classList.remove('is-rippling'), { once: true });
  });
}

/* ============================================================================
   08. PRODUCT QUANTITY SELECTORS
   ============================================================================ */
function initQuantitySelectors() {
  document.addEventListener('change', (event) => {
    const select = event.target.closest('.qty-select');
    if (!select) return;

    const card = select.closest('.product-card');
    if (!card) return;

    const customField = card.querySelector('.custom-qty-field');
    const customInput = customField ? customField.querySelector('input') : null;
    const isCustom = select.value === 'custom';

    if (customField) customField.hidden = !isCustom;
    if (customInput) {
      customInput.required = isCustom;
      if (isCustom) customInput.focus();
      else customInput.value = '';
    }
  });
}

/* ============================================================================
   09. PRODUCT "ORDER ON WHATSAPP" BUTTONS
   ============================================================================ */
function buildOrderMessage(productName, quantity, notes) {
  const lines = [
    'Hi Hamza Ocean Seafood! I\u2019d like to place an order:',
    '',
    `Product: ${productName}`,
    `Quantity: ${quantity}`,
  ];
  if (notes) {
    lines.push(`Special Instructions: ${notes}`);
  }
  lines.push('', 'Please confirm availability and total price. Thank you!');
  return lines.join('\n');
}

function initProductOrderButtons() {
  document.addEventListener('click', (event) => {
    const orderBtn = event.target.closest('.btn-order-whatsapp');
    if (!orderBtn) return;

    const card = orderBtn.closest('.product-card');
    if (!card) return;

    const productName = orderBtn.dataset.productName || card.querySelector('.product-name')?.textContent || 'Product';
    const qtySelect = card.querySelector('[data-product-qty]');
    const customInput = card.querySelector('[data-product-custom-qty]');
    const notesField = card.querySelector('[data-product-notes]');

    let quantity = '1 kg';
    if (qtySelect) {
      if (qtySelect.value === 'custom') {
        if (customInput && !customInput.value.trim()) {
          customInput.focus();
          if (customInput.reportValidity) customInput.reportValidity();
          return; // stop here — let the native validation bubble guide the user
        }
        quantity = `${customInput.value} kg`;
      } else {
        quantity = `${qtySelect.value} kg`;
      }
    }

    const notes = notesField ? notesField.value.trim() : '';
    const message = buildOrderMessage(productName, quantity, notes);
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;

    window.open(url, '_blank', 'noopener,noreferrer');
    trackEvent('whatsapp_order_click', { product_name: productName, quantity });
  });
}

/* ============================================================================
   09b. FAQ ACCORDION
   ============================================================================ */
function initFaqAccordion() {
  const toggles = document.querySelectorAll('.faq-toggle');
  if (!toggles.length) return;

  toggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const item = toggle.closest('.faq-item');
      const answer = document.getElementById(toggle.getAttribute('aria-controls'));
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';

      // Close any other open item (remove this block for a multi-open accordion)
      document.querySelectorAll('.faq-toggle[aria-expanded="true"]').forEach((openToggle) => {
        if (openToggle !== toggle) {
          openToggle.setAttribute('aria-expanded', 'false');
          openToggle.closest('.faq-item')?.classList.remove('is-open');
          const openAnswer = document.getElementById(openToggle.getAttribute('aria-controls'));
          if (openAnswer) openAnswer.hidden = true;
        }
      });

      toggle.setAttribute('aria-expanded', String(!isOpen));
      item?.classList.toggle('is-open', !isOpen);
      if (answer) answer.hidden = isOpen;
    });
  });
}

/* ============================================================================
   10 & 11. FORMS — shared Web3Forms submit handler
   ============================================================================ */
async function submitToWeb3Forms(form, successEl, options) {
  const opts = options || {};
  const formData = new FormData(form);

  // Honeypot: if a bot filled this hidden field, drop the submission quietly
  if (formData.get('botcheck')) return;

  if (opts.extraFields) {
    Object.entries(opts.extraFields).forEach(([key, value]) => formData.append(key, value));
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  const originalLabel = submitBtn ? submitBtn.textContent : '';
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = opts.loadingLabel || 'Sending\u2026';
  }

  try {
    const endpoint = form.getAttribute('action') || WEB3FORMS_ENDPOINT;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: formData,
    });
    const result = await response.json();

    if (result.success) {
      showFormMessage(successEl, opts.successMessage || 'Thank you!', false);
      form.reset();
      trackEvent(opts.eventName || 'form_submit', { form_id: form.id });
    } else {
      throw new Error(result.message || 'Submission failed.');
    }
  } catch (err) {
    showFormMessage(
      successEl,
      opts.errorMessage || 'Something went wrong \u2014 please try again, or message us on WhatsApp.',
      true
    );
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = originalLabel;
    }
  }
}

/* ---- 10. Contact form ---- */
function initContactForm() {
  const form = document.getElementById('contactForm');
  const successEl = document.getElementById('formSuccessMessage');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    submitToWeb3Forms(form, successEl, {
      successMessage: "Thank you! Your message has been sent \u2014 we'll get back to you shortly.",
      eventName: 'contact_form_submit',
    });
  });
}

/* ---- 11. Newsletter form ----
   The HTML newsletter form has no backend fields of its own, so the
   access key / subject / from_name are appended here at submit time. */
function initNewsletterForm() {
  const form = document.getElementById('newsletterForm');
  const successEl = document.getElementById('newsletterSuccess');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    submitToWeb3Forms(form, successEl, {
      successMessage: "You're subscribed! Welcome to Hamza Ocean Seafood.",
      loadingLabel: 'Subscribing\u2026',
      eventName: 'newsletter_signup',
      extraFields: {
        access_key: WEB3FORMS_ACCESS_KEY,
        subject: 'New Newsletter Subscriber \u2014 Hamza Ocean Seafood',
        from_name: 'Hamza Ocean Seafood Newsletter',
      },
    });
  });
}

/* ============================================================================
   12. VIMEO VIDEO PLAYERS (hero background + process section)
   ============================================================================
   Both players share one lazily-loaded copy of the Vimeo Player SDK so it's
   only fetched once even though two players use it. */
let vimeoSDKPromise = null;

/** Injects the Vimeo Player SDK <script> once and resolves when window.Vimeo is ready. */
function loadVimeoSDK() {
  if (vimeoSDKPromise) return vimeoSDKPromise;
  vimeoSDKPromise = new Promise((resolve, reject) => {
    if (window.Vimeo && window.Vimeo.Player) {
      resolve(window.Vimeo);
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://player.vimeo.com/api/player.js';
    script.async = true;
    script.onload = () => resolve(window.Vimeo);
    script.onerror = () => reject(new Error('Failed to load Vimeo Player SDK'));
    document.head.appendChild(script);
  });
  return vimeoSDKPromise;
}

/** Hero background video: muted autoplay loop, lazy-loaded once the hero
    scrolls into view, with a sound toggle button and an image fallback that
    stays visible (and takes over) if the video can't load or play. */
function initHeroVideo() {
  const heroSection = document.getElementById('home');
  const videoWrap = document.getElementById('heroVideoWrap');
  const fallbackImage = document.getElementById('heroFallbackImage');
  const soundToggle = document.getElementById('heroSoundToggle');
  if (!heroSection || !videoWrap || !HERO_VIMEO_VIDEO_ID || HERO_VIMEO_VIDEO_ID === 'HERO_VIMEO_VIDEO_ID') {
    return; // no placeholder ID set yet — keep showing the static fallback image
  }

  let player = null;

  const setupPlayer = () => {
    loadVimeoSDK()
      .then((Vimeo) => {
        player = new Vimeo.Player(videoWrap, {
          id: HERO_VIMEO_VIDEO_ID,
          background: true, // strips Vimeo UI, forces muted + loop + autoplay
          autoplay: true,
          muted: true,
          loop: true,
          dnt: true,
          // NOTE: deliberately no "responsive: true" here — it fights with
          // background:true and makes Vimeo set its own inline iframe size,
          // which is what caused the video to only fill the top-left corner.
          // Sizing/cropping is handled entirely by the CSS on
          // .hero-video-wrap iframe instead (see style.css).
        });
        player.ready().then(() => {
          videoWrap.classList.add('is-ready');
          if (fallbackImage) fallbackImage.style.opacity = '0';
          if (soundToggle) soundToggle.hidden = false;
        });
      })
      .catch(() => {
        // SDK or video failed — the fallback image (still in the DOM) remains visible.
      });
  };

  // Lazy-load: only start pulling the SDK/iframe once the hero is actually in view.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setupPlayer();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.1 }
    );
    observer.observe(heroSection);
  } else {
    setupPlayer();
  }

  if (soundToggle) {
    soundToggle.addEventListener('click', () => {
      if (!player) return;
      const isMuted = soundToggle.getAttribute('aria-pressed') === 'false';
      player.setMuted(!isMuted).then(() => {
        soundToggle.setAttribute('aria-pressed', String(isMuted));
        soundToggle.setAttribute('aria-label', isMuted ? 'Mute background video' : 'Unmute background video');
        soundToggle.querySelector('.icon-muted').hidden = isMuted;
        soundToggle.querySelector('.icon-unmuted').hidden = !isMuted;
      });
    });
  }
}

/** Process section video: standard (non-background) Vimeo embed with fully
    custom Play/Pause and Mute/Unmute buttons, built on the Vimeo Player SDK. */
function initProcessVideo() {
  const wrap = document.getElementById('processVideoWrap');
  const controls = document.getElementById('processVideoControls');
  const playPauseBtn = document.getElementById('processPlayPauseBtn');
  const muteBtn = document.getElementById('processMuteBtn');
  if (!wrap) return;

  const videoId = wrap.dataset.vimeoId;
  if (!videoId || videoId === 'PROCESS_VIMEO_VIDEO_ID') return; // placeholder not set yet

  loadVimeoSDK()
    .then((Vimeo) => {
      const player = new Vimeo.Player(wrap, {
        id: videoId,
        muted: true,
        loop: true,
        controls: false, // we render our own controls below
        dnt: true,
      });

      let isPlaying = false;
      let isMuted = true;

      player.ready().then(() => {
        if (controls) controls.hidden = false;
      });

      if (playPauseBtn) {
        playPauseBtn.addEventListener('click', () => {
          const action = isPlaying ? player.pause() : player.play();
          action.then(() => {
            isPlaying = !isPlaying;
            playPauseBtn.querySelector('.icon-play').hidden = isPlaying;
            playPauseBtn.querySelector('.icon-pause').hidden = !isPlaying;
            playPauseBtn.setAttribute('aria-label', isPlaying ? 'Pause video' : 'Play video');
          });
        });
      }

      if (muteBtn) {
        muteBtn.addEventListener('click', () => {
          player.setMuted(!isMuted).then(() => {
            isMuted = !isMuted;
            muteBtn.querySelector('.icon-muted').hidden = !isMuted;
            muteBtn.querySelector('.icon-unmuted').hidden = isMuted;
            muteBtn.setAttribute('aria-label', isMuted ? 'Unmute video' : 'Mute video');
          });
        });
      }
    })
    .catch(() => {
      // SDK/video failed to load — video-wrapper background stays black; no crash.
    });
}

/* ============================================================================
   13. BOOTSTRAP
   ============================================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initCurrentYear();
  initMobileDrawer();
  initScrollEffects();
  initActiveNavHighlight();
  initScrollReveal();
  initButtonRipple();
  initQuantitySelectors();
  initProductOrderButtons();
  initFaqAccordion();
  initContactForm();
  initNewsletterForm();
  initHeroVideo();
  initProcessVideo();
});
