// Small, dependency-free intersection observer to reveal elements with .ktp-animate
(function(){
  function initAnimations(root=document){
    const els = Array.from(root.querySelectorAll('.ktp-animate'));
    if (!els.length) return;

    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = el.getAttribute('data-delay');
          if (delay) el.style.setProperty('--ktp-delay', delay + 'ms');
          el.classList.add('is-visible');
          obs.unobserve(el);
        }
      });
    }, { root: null, rootMargin: '0px 0px -10% 0px', threshold: 0.06 });

    els.forEach(e => io.observe(e));

    // expose a small helper for SPA re-init if needed
    window.ktpInitAnimations = function(){
      // re-run for newly injected content
      const newEls = Array.from(document.querySelectorAll('.ktp-animate:not(.is-visible)'));
      newEls.forEach(e => io.observe(e));
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initAnimations(document));
  } else {
    initAnimations(document);
  }

  // Also try a gentle re-init after 500ms to catch dynamic inits
  setTimeout(() => { if (window.ktpInitAnimations) window.ktpInitAnimations(); }, 500);
})();