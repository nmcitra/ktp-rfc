// Small, dependency-free intersection observer to reveal elements with .ktp-animate
// Elements start visible (CSS default). JS hides below-fold elements for scroll animation.
(function(){
  let io = null;

  function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
  }

  function initAnimations(){
    // Find elements that haven't been processed yet
    const els = Array.from(document.querySelectorAll('.ktp-animate:not(.is-visible):not(.is-instant):not(.will-animate)'));
    if (!els.length) return;

    // Elements in viewport stay visible (mark as instant so we don't reprocess)
    // Elements below fold get hidden for scroll animation
    els.forEach(el => {
      if (isInViewport(el)) {
        el.classList.add('is-instant', 'is-visible');
      } else {
        el.classList.add('will-animate');
      }
    });

    // Set up observer for elements that will animate
    const scrollEls = Array.from(document.querySelectorAll('.ktp-animate.will-animate:not(.is-visible)'));
    if (!scrollEls.length) return;

    // Create observer if needed
    if (!io) {
      io = new IntersectionObserver((entries, obs) => {
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
    }

    scrollEls.forEach(e => io.observe(e));
  }

  // Expose global helper
  window.ktpInitAnimations = initAnimations;

  // Run on DOMContentLoaded or immediately if ready
  function init() {
    initAnimations();
    setupNavigationListener();
  }

  function setupNavigationListener() {
    // Material for MkDocs instant loading - listen for content swap
    const content = document.querySelector('.md-content');
    if (content && !content._ktpObserving) {
      content._ktpObserving = true;
      const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            requestAnimationFrame(initAnimations);
            break;
          }
        }
      });
      observer.observe(content, { childList: true, subtree: false });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Fallback: location change detection for SPA navigation
  let lastPath = location.pathname;
  setInterval(() => {
    if (location.pathname !== lastPath) {
      lastPath = location.pathname;
      requestAnimationFrame(initAnimations);
    }
  }, 100);
})();

// Scroll progress bar
(function(){
  function initScrollProgress() {
    // Create progress bar elements if not exist
    if (document.querySelector('.scroll-progress')) return;

    const progressContainer = document.createElement('div');
    progressContainer.className = 'scroll-progress';
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress-bar';
    progressContainer.appendChild(progressBar);
    document.body.appendChild(progressContainer);

    function updateProgress() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = progress + '%';
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollProgress);
  } else {
    initScrollProgress();
  }
})();