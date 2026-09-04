/**
 * KTP Particle Physics Background
 * Represents digital physics and trust networks visually
 * Professional, performant, accessible
 */

class ParticlePhysics {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.mouse = { x: null, y: null, radius: 180 };
    this.animationId = null;
    
    // Configuration
    this.config = {
      particleCount: options.particleCount || this.getParticleCount(),
      particleColor: options.particleColor || '#88ccee',
      connectionColor: options.connectionColor || '#88ccee',
      connectionDistance: options.connectionDistance || 120,
      particleSize: options.particleSize || 2.5,
      baseSpeed: options.baseSpeed || 0.3,
      mouseInfluence: options.mouseInfluence || 0.05,
      fps: options.fps || 45, // cap frames per second
      ...options
    };

    // Check for reduced motion preference
    this.respectsReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // For throttling
    this.lastFrameTime = 0;
    this.frameInterval = 1000 / this.config.fps;
    
    this.init();
  }

  getParticleCount() {
    const width = window.innerWidth;
    if (width < 640) return 30;
    if (width < 1024) return 50;
    return 70;
  }

  init() {
    this.setCanvasSize();
    this.createParticles();
    this.setupEventListeners();
    
    if (!this.respectsReducedMotion) {
      this.animate();
    } else {
      // Static render for accessibility
      this.renderStatic();
    }
  }

  setCanvasSize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.canvas.style.width = `${rect.width}px`;
    this.canvas.style.height = `${rect.height}px`;
    
    this.ctx.scale(dpr, dpr);
    this.width = rect.width;
    this.height = rect.height;
  }

  createParticles() {
    this.particles = [];
    
    for (let i = 0; i < this.config.particleCount; i++) {
      // Layer system for depth (parallax)
      const layer = Math.random();
      const speedMultiplier = 0.5 + (layer * 0.8);
      
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * this.config.baseSpeed * speedMultiplier,
        vy: (Math.random() - 0.5) * this.config.baseSpeed * speedMultiplier,
        size: this.config.particleSize * (0.6 + layer * 0.6),
        layer: layer,
        opacity: 0.3 + (layer * 0.4)
      });
    }
  }

  setupEventListeners() {
    // Mouse movement
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = e.clientX - rect.left;
      this.mouse.y = e.clientY - rect.top;
    });

    this.canvas.addEventListener('mouseleave', () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });

    // Responsive resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        this.setCanvasSize();
        this.config.particleCount = this.getParticleCount();
        this.createParticles();
      }, 250);
    });

    // IntersectionObserver for performance
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting && this.animationId) {
          cancelAnimationFrame(this.animationId);
          this.animationId = null;
        } else if (entry.isIntersecting && !this.animationId && !this.respectsReducedMotion) {
          this.animate();
        }
      });
    });
    
    observer.observe(this.canvas);

    // Pause when the page is hidden to save CPU
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (this.animationId) {
          cancelAnimationFrame(this.animationId);
          this.animationId = null;
        }
      } else {
        if (!this.animationId && !this.respectsReducedMotion) {
          this.animate();
        }
      }
    });
  }

  updateParticle(particle) {
    // Apply mouse gravity (inverse square law)
    if (this.mouse.x !== null && this.mouse.y !== null) {
      const dx = this.mouse.x - particle.x;
      const dy = this.mouse.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < this.mouse.radius) {
        const force = (1 - distance / this.mouse.radius) * this.config.mouseInfluence;
        particle.vx += (dx / distance) * force * particle.layer;
        particle.vy += (dy / distance) * force * particle.layer;
      }
    }

    // Apply velocity damping
    particle.vx *= 0.99;
    particle.vy *= 0.99;

    // Add subtle random motion (Brownian)
    particle.vx += (Math.random() - 0.5) * 0.02;
    particle.vy += (Math.random() - 0.5) * 0.02;

    // Speed limit
    const speed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
    const maxSpeed = 2;
    if (speed > maxSpeed) {
      particle.vx = (particle.vx / speed) * maxSpeed;
      particle.vy = (particle.vy / speed) * maxSpeed;
    }

    // Update position
    particle.x += particle.vx;
    particle.y += particle.vy;

    // Wrap around edges
    if (particle.x < 0) particle.x = this.width;
    if (particle.x > this.width) particle.x = 0;
    if (particle.y < 0) particle.y = this.height;
    if (particle.y > this.height) particle.y = 0;
  }

  drawParticle(particle) {
    const { ctx, config } = this;
    
    // Glow effect
    const gradient = ctx.createRadialGradient(
      particle.x, particle.y, 0,
      particle.x, particle.y, particle.size * 3
    );
    
    gradient.addColorStop(0, `${config.particleColor}${Math.floor(particle.opacity * 255).toString(16).padStart(2, '0')}`);
    gradient.addColorStop(0.5, `${config.particleColor}${Math.floor(particle.opacity * 128).toString(16).padStart(2, '0')}`);
    gradient.addColorStop(1, `${config.particleColor}00`);
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
    ctx.fill();
    
    // Core particle
    ctx.fillStyle = `${config.particleColor}${Math.floor(particle.opacity * 255).toString(16).padStart(2, '0')}`;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
    ctx.fill();
  }

  drawConnections() {
    const { ctx, particles, config } = this;
    
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < config.connectionDistance) {
          const opacity = (1 - distance / config.connectionDistance) * 0.15;
          
          ctx.strokeStyle = `${config.connectionColor}${Math.floor(opacity * 255).toString(16).padStart(2, '0')}`;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }

  animate(timestamp) {
    // Throttle by FPS cap
    if (!timestamp) timestamp = performance.now();
    const elapsed = timestamp - (this.lastFrameTime || 0);
    if (elapsed >= this.frameInterval) {
      this.lastFrameTime = timestamp - (elapsed % this.frameInterval);

      this.ctx.clearRect(0, 0, this.width, this.height);
      
      // Update and draw connections first (behind particles)
      this.drawConnections();
      
      // Update and draw particles
      this.particles.forEach(particle => {
        this.updateParticle(particle);
        this.drawParticle(particle);
      });
    }
    
    this.animationId = requestAnimationFrame((ts) => this.animate(ts));
  }

  renderStatic() {
    // For users with reduced motion preference
    this.ctx.clearRect(0, 0, this.width, this.height);
    this.drawConnections();
    this.particles.forEach(particle => this.drawParticle(particle));
  }

  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    this.canvas.remove();
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const heroSection = document.querySelector('.md-content');
  
  if (heroSection && window.location.pathname === '/ktp-rfc/' || window.location.pathname === '/') {
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-physics';
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '0';
    
    // Insert canvas
    const contentWrapper = document.querySelector('.md-content__inner');
    if (contentWrapper) {
      contentWrapper.style.position = 'relative';
      contentWrapper.insertBefore(canvas, contentWrapper.firstChild);
      
      // Initialize particle system
      new ParticlePhysics(canvas);
    }
  }
});
