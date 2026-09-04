/**
 * KTP Animated Stats Counter
 * Counts up statistics on scroll with staggered reveal
 * Professional, performant, accessible
 */

class AnimatedStats {
  constructor(container, options = {}) {
    this.container = container;
    this.cards = Array.from(container.querySelectorAll('.ktp-stat-card'));
    this.hasAnimated = false;
    
    this.config = {
      threshold: 0.5, // Trigger when 50% visible
      staggerDelay: 200, // Delay between each card (ms)
      ...options
    };

    // Check for reduced motion preference
    this.respectsReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    this.init();
  }

  init() {
    if (this.respectsReducedMotion) {
      // Show final values immediately for accessibility
      this.cards.forEach(card => {
        const number = card.querySelector('.ktp-stat-number');
        const value = parseInt(card.dataset.value, 10);
        number.textContent = this.formatNumber(value);
        card.style.opacity = '1';
      });

      // Allow keyboard users to focus cards (they already are tabbable) but nothing else is needed
      return;
    }

    this.setupObserver();

    // Support keyboard users: start animation when any stat card receives focus
    this.cards.forEach(card => {
      const startAnimationIfNeeded = () => {
        if (!this.hasAnimated) {
          this.hasAnimated = true;
          this.animateAll();
        }
      };

      card.addEventListener('focus', () => startAnimationIfNeeded(), { once: true });

      // Also start on Enter/Space for keyboard users
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          startAnimationIfNeeded();
        }
      });
    });
  }

  setupObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !this.hasAnimated) {
          this.hasAnimated = true;
          this.animateAll();
          observer.disconnect(); // Only animate once
        }
      });
    }, {
      threshold: this.config.threshold,
      rootMargin: '0px'
    });

    observer.observe(this.container);
  }

  animateAll() {
    this.cards.forEach((card, index) => {
      setTimeout(() => {
        this.animateCard(card);
      }, index * this.config.staggerDelay);
    });
  }

  animateCard(card) {
    const number = card.querySelector('.ktp-stat-number');
    const label = card.querySelector('.ktp-stat-label');
    const sublabel = card.querySelector('.ktp-stat-sublabel');
    const targetValue = parseInt(card.dataset.value, 10);
    const duration = parseInt(card.dataset.duration || 2000, 10);

    // Fade in card
    card.style.opacity = '1';

    // Animate number count-up
    this.animateNumber(number, 0, targetValue, duration, () => {
      // After number completes, fade in labels
      if (label) {
        label.style.opacity = '1';
      }
      if (sublabel) {
        sublabel.style.opacity = '1';
      }
      
      // Pulse effect on completion
      card.classList.add('ktp-stat-card--complete');
    });
  }

  animateNumber(element, start, end, duration, onComplete) {
    const startTime = performance.now();
    const range = end - start;

    const updateNumber = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease-out cubic for natural deceleration
      const easedProgress = this.easeOutCubic(progress);
      const currentValue = Math.floor(start + (range * easedProgress));
      
      element.textContent = this.formatNumber(currentValue);

      if (progress < 1) {
        requestAnimationFrame(updateNumber);
      } else {
        element.textContent = this.formatNumber(end);
        if (onComplete) onComplete();
      }
    };

    requestAnimationFrame(updateNumber);
  }

  easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  formatNumber(num) {
    // Add commas for numbers >= 1000
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  destroy() {
    // Cleanup if needed
    this.cards.forEach(card => {
      card.style.opacity = '1';
    });
  }
}

// Initialize when DOM is ready and also during SPA navigation (Material's document$)
function initStats() {
  const statsContainer = document.querySelector('.ktp-stats-section');
  if (!statsContainer) return;

  // If an instance is already attached, destroy it and create a fresh one to allow re-animation
  if (statsContainer._ktpStatsInstance && typeof statsContainer._ktpStatsInstance.destroy === 'function') {
    statsContainer._ktpStatsInstance.destroy();
    delete statsContainer._ktpStatsInstance;
  }

  statsContainer._ktpStatsInstance = new AnimatedStats(statsContainer);
}

// Run on initial load
document.addEventListener('DOMContentLoaded', initStats);

// Run on MkDocs Material navigation (document$ is exposed by the theme)
if (typeof document !== 'undefined' && typeof document.$ === 'undefined') {
  try {
    if (typeof document$ !== 'undefined' && document$ && typeof document$.subscribe === 'function') {
      document$.subscribe(() => {
        // Small timeout to ensure DOM is fully replaced
        setTimeout(initStats, 20);
      });
    }
  } catch (err) {
    // ignore if document$ isn't available
    // eslint-disable-next-line no-console
    console.warn('AnimatedStats: document$ not available, SPA nav will not reinitialize automatically');
  }
}
