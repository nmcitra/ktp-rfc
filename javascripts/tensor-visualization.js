/**
 * Context Tensor 3D Visualization
 * An interactive 7-axis radar chart representing the trust geometry
 * Now includes Risk Deflation visualization
 */

(function() {
  'use strict';

  const DIMENSIONS = [
    {
      key: 'mass',
      label: 'Mass',
      symbol: 'M',
      description: 'Telemetry density and volume — the weight of observed behavior',
      color: '#88ccee',
      weight: 0.15
    },
    {
      key: 'momentum',
      label: 'Momentum',
      symbol: 'P',
      description: 'Rate and direction of trust change — velocity of behavioral shift',
      color: '#44aa99',
      weight: 0.12
    },
    {
      key: 'inertia',
      label: 'Inertia',
      symbol: 'I',
      description: 'Resistance to rapid fluctuation — stability of established patterns',
      color: '#117733',
      weight: 0.13
    },
    {
      key: 'heat',
      label: 'Heat',
      symbol: 'H',
      description: 'Environmental stress and anomaly load — friction from adversarial signals',
      color: '#cc6677',
      weight: 0.18
    },
    {
      key: 'time',
      label: 'Time',
      symbol: 'T',
      description: 'Temporal context and decay — freshness and historical weight',
      color: '#aa4499',
      weight: 0.12
    },
    {
      key: 'observer',
      label: 'Observer',
      symbol: 'O',
      description: 'Attestation coverage and peer visibility — who is watching',
      color: '#882255',
      weight: 0.15
    },
    {
      key: 'soul',
      label: 'Soul',
      symbol: 'S',
      description: 'Constitutional constraints — immutable vetoes that override all else',
      color: '#D4AF37',
      weight: 0.15
    }
  ];

  // Current dimension values (will pulse)
  let values = [0.72, 0.58, 0.85, 0.34, 0.67, 0.79, 0.95];
  let targetValues = [...values];

  // Risk factor (0-1, where 0.25 = 25% risk)
  let riskFactor = 0.18;
  let targetRisk = 0.18;

  // Calculated scores
  let eBase = 0;
  let eTrust = 0;

  // 3D rotation state
  let rotationY = 0;
  let rotationX = 15;
  let autoRotate = true;

  // Hover state
  let hoveredIndex = -1;
  let selectedIndex = -1; // For mobile tap-to-select
  let mouseX = 0;
  let mouseY = 0;
  let tooltipBounds = null; // Track tooltip position for click detection

  // Canvas and context
  let canvas, ctx;
  let centerX, centerY, radius;
  let animationId;

  // DOM elements for score display
  let eBaseEl, eRiskEl, eTrustEl;

  function init() {
    const container = document.getElementById('tensor-viz-container');
    if (!container) return;

    canvas = document.getElementById('tensor-canvas');
    if (!canvas) return;

    ctx = canvas.getContext('2d');

    // Get score display elements
    eBaseEl = document.getElementById('tensor-ebase');
    eRiskEl = document.getElementById('tensor-risk');
    eTrustEl = document.getElementById('tensor-etrust');

    // Set up canvas size
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Mouse events
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseleave', handleMouseLeave);
    canvas.addEventListener('click', handleClick);

    // Start animation
    animate();

    // Start value pulsing
    setInterval(pulseValues, 2000);
  }

  function resizeCanvas() {
    const container = document.getElementById('tensor-viz-container');
    if (!container || !canvas) return;

    const rect = container.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';

    ctx.scale(dpr, dpr);

    centerX = rect.width / 2;
    centerY = rect.height / 2;
    radius = Math.min(rect.width, rect.height) * 0.32;
  }

  function pulseValues() {
    // Generate new target values with slight variations
    targetValues = values.map((v, i) => {
      // Soul dimension stays high (constitutional constraint)
      if (i === 6) return Math.max(0.9, Math.min(1, v + (Math.random() - 0.5) * 0.05));
      // Heat is inverted (lower is better for trust)
      if (i === 3) return Math.max(0.15, Math.min(0.6, v + (Math.random() - 0.5) * 0.15));
      // Other dimensions pulse more
      const delta = (Math.random() - 0.5) * 0.15;
      return Math.max(0.3, Math.min(0.95, v + delta));
    });

    // Pulse risk factor
    targetRisk = Math.max(0.08, Math.min(0.35, riskFactor + (Math.random() - 0.5) * 0.1));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function calculateScores() {
    // Calculate E_base as weighted average of dimensions
    // Note: Heat is inverted (1 - heat) since high heat is bad
    let weightedSum = 0;
    let totalWeight = 0;

    for (let i = 0; i < 7; i++) {
      const dim = DIMENSIONS[i];
      let effectiveValue = values[i];

      // Invert heat (high heat = low trust contribution)
      if (i === 3) {
        effectiveValue = 1 - effectiveValue;
      }

      weightedSum += effectiveValue * dim.weight;
      totalWeight += dim.weight;
    }

    eBase = (weightedSum / totalWeight) * 100;

    // Calculate E_trust with risk deflation
    eTrust = eBase * (1 - riskFactor);
  }

  function updateScoreDisplay() {
    if (eBaseEl) eBaseEl.textContent = eBase.toFixed(0);
    if (eRiskEl) eRiskEl.textContent = (riskFactor * 100).toFixed(0) + '%';
    if (eTrustEl) eTrustEl.textContent = eTrust.toFixed(0);
  }

  function animate() {
    // Interpolate values
    values = values.map((v, i) => lerp(v, targetValues[i], 0.02));
    riskFactor = lerp(riskFactor, targetRisk, 0.02);

    // Calculate scores
    calculateScores();
    updateScoreDisplay();

    // Auto-rotate
    if (autoRotate && hoveredIndex === -1) {
      rotationY += 0.15;
    }

    draw();
    animationId = requestAnimationFrame(animate);
  }

  function project3D(x, y, z) {
    const cosY = Math.cos(rotationY * Math.PI / 180);
    const sinY = Math.sin(rotationY * Math.PI / 180);
    const cosX = Math.cos(rotationX * Math.PI / 180);
    const sinX = Math.sin(rotationX * Math.PI / 180);

    const x1 = x * cosY - z * sinY;
    const z1 = x * sinY + z * cosY;
    const y1 = y * cosX - z1 * sinX;
    const z2 = y * sinX + z1 * cosX;

    const perspective = 500;
    const scale = perspective / (perspective + z2);

    return {
      x: centerX + x1 * scale,
      y: centerY + y1 * scale,
      z: z2,
      scale: scale
    };
  }

  function getAxisPoint(index, value, is3D = true) {
    const angle = (index / 7) * Math.PI * 2 - Math.PI / 2;
    const r = radius * value;

    if (is3D) {
      const x = Math.cos(angle) * r;
      const y = Math.sin(angle) * r;
      const z = Math.sin(angle * 2) * 20;
      return project3D(x, y, z);
    } else {
      return {
        x: centerX + Math.cos(angle) * r,
        y: centerY + Math.sin(angle) * r
      };
    }
  }

  function draw() {
    if (!ctx) return;

    const width = canvas.width / (window.devicePixelRatio || 1);
    const height = canvas.height / (window.devicePixelRatio || 1);

    ctx.clearRect(0, 0, width, height);

    // Draw risk deflation ring (outer)
    drawRiskRing();

    // Draw concentric rings (grid)
    drawGrid();

    // Draw axes
    drawAxes();

    // Draw data polygon (E_base)
    drawDataPolygon();

    // Draw deflated polygon (E_trust) - shows the effect of risk
    drawDeflatedPolygon();

    // Draw axis labels
    drawLabels();

    // Draw tooltip if hovering or selected
    if (hoveredIndex >= 0 || selectedIndex >= 0) {
      drawTooltip();
    } else {
      tooltipBounds = null;
    }
  }

  function drawRiskRing() {
    // Outer ring showing maximum possible (100%)
    const outerRadius = radius * 1.08;

    ctx.beginPath();
    ctx.arc(centerX, centerY, outerRadius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(204, 102, 119, 0.15)';
    ctx.lineWidth = 8;
    ctx.stroke();

    // Risk portion of the ring (shows deflation amount)
    const riskArcLength = Math.PI * 2 * riskFactor;
    ctx.beginPath();
    ctx.arc(centerX, centerY, outerRadius, -Math.PI / 2, -Math.PI / 2 + riskArcLength);
    ctx.strokeStyle = 'rgba(204, 102, 119, 0.6)';
    ctx.lineWidth = 8;
    ctx.stroke();
  }

  function drawGrid() {
    const rings = 5;

    for (let r = 1; r <= rings; r++) {
      const ringRadius = (r / rings);

      ctx.beginPath();
      for (let i = 0; i <= 7; i++) {
        const point = getAxisPoint(i % 7, ringRadius);
        if (i === 0) {
          ctx.moveTo(point.x, point.y);
        } else {
          ctx.lineTo(point.x, point.y);
        }
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(136, 204, 238, ' + (0.08 + r * 0.025) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  function drawAxes() {
    for (let i = 0; i < 7; i++) {
      const endPoint = getAxisPoint(i, 1);

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(endPoint.x, endPoint.y);

      const isHovered = i === hoveredIndex;
      ctx.strokeStyle = isHovered
        ? DIMENSIONS[i].color
        : 'rgba(136, 204, 238, 0.25)';
      ctx.lineWidth = isHovered ? 2 : 1;
      ctx.stroke();
    }
  }

  function drawDataPolygon() {
    // Draw E_base polygon (full performance)
    ctx.beginPath();
    for (let i = 0; i <= 7; i++) {
      const point = getAxisPoint(i % 7, values[i % 7]);
      if (i === 0) {
        ctx.moveTo(point.x, point.y);
      } else {
        ctx.lineTo(point.x, point.y);
      }
    }
    ctx.closePath();

    // Gradient fill
    const gradient = ctx.createRadialGradient(
      centerX, centerY, 0,
      centerX, centerY, radius
    );
    gradient.addColorStop(0, 'rgba(136, 204, 238, 0.35)');
    gradient.addColorStop(0.7, 'rgba(136, 204, 238, 0.12)');
    gradient.addColorStop(1, 'rgba(136, 204, 238, 0.05)');

    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw polygon stroke (E_base)
    ctx.strokeStyle = 'rgba(136, 204, 238, 0.7)';
    ctx.lineWidth = 2;
    ctx.setLineDash([]);
    ctx.stroke();

    // Draw data points
    for (let i = 0; i < 7; i++) {
      const point = getAxisPoint(i, values[i]);
      const isHovered = i === hoveredIndex;
      const pointRadius = isHovered ? 7 : 4;

      if (isHovered) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, pointRadius + 4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(212, 175, 55, 0.3)';
        ctx.fill();
      }

      ctx.beginPath();
      ctx.arc(point.x, point.y, pointRadius, 0, Math.PI * 2);
      ctx.fillStyle = isHovered ? DIMENSIONS[i].color : '#88ccee';
      ctx.fill();

      ctx.beginPath();
      ctx.arc(point.x, point.y, pointRadius * 0.4, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.fill();
    }
  }

  function drawDeflatedPolygon() {
    // Draw E_trust polygon (after risk deflation)
    // This is smaller, showing the gap caused by risk
    const deflationFactor = 1 - riskFactor;

    ctx.beginPath();
    for (let i = 0; i <= 7; i++) {
      const point = getAxisPoint(i % 7, values[i % 7] * deflationFactor);
      if (i === 0) {
        ctx.moveTo(point.x, point.y);
      } else {
        ctx.lineTo(point.x, point.y);
      }
    }
    ctx.closePath();

    // Fill with gold (trust color)
    const gradient = ctx.createRadialGradient(
      centerX, centerY, 0,
      centerX, centerY, radius * deflationFactor
    );
    gradient.addColorStop(0, 'rgba(212, 175, 55, 0.4)');
    gradient.addColorStop(1, 'rgba(212, 175, 55, 0.15)');

    ctx.fillStyle = gradient;
    ctx.fill();

    // Stroke
    ctx.strokeStyle = 'rgba(212, 175, 55, 0.8)';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  function drawLabels() {
    ctx.font = '600 12px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < 7; i++) {
      const point = getAxisPoint(i, 1.15);
      const isHovered = i === hoveredIndex;

      const circleRadius = isHovered ? 14 : 12;

      ctx.beginPath();
      ctx.arc(point.x, point.y, circleRadius, 0, Math.PI * 2);
      ctx.fillStyle = isHovered
        ? DIMENSIONS[i].color
        : 'rgba(26, 31, 54, 0.9)';
      ctx.fill();
      ctx.strokeStyle = isHovered
        ? 'rgba(255, 255, 255, 0.5)'
        : 'rgba(136, 204, 238, 0.25)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = isHovered ? '#ffffff' : '#88ccee';
      ctx.fillText(DIMENSIONS[i].symbol, point.x, point.y);

      if (isHovered) {
        ctx.font = '500 10px Inter, sans-serif';
        ctx.fillStyle = DIMENSIONS[i].color;
        ctx.fillText((values[i] * 100).toFixed(0) + '%', point.x, point.y + 22);
        ctx.font = '600 12px Inter, sans-serif';
      }
    }
  }

  function drawTooltip() {
    const activeIndex = selectedIndex >= 0 ? selectedIndex : hoveredIndex;
    if (activeIndex < 0) return;

    const dim = DIMENSIONS[activeIndex];
    const point = getAxisPoint(activeIndex, values[activeIndex]);

    const tooltipWidth = 220;
    const tooltipHeight = 95;
    const padding = 10;

    const width = canvas.width / (window.devicePixelRatio || 1);
    const height = canvas.height / (window.devicePixelRatio || 1);

    // Center the tooltip in the canvas
    let tooltipX = (width - tooltipWidth) / 2;
    let tooltipY = (height - tooltipHeight) / 2;

    // Store bounds for click detection
    tooltipBounds = { x: tooltipX, y: tooltipY, width: tooltipWidth, height: tooltipHeight, dimIndex: activeIndex };

    ctx.beginPath();
    ctx.roundRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight, 8);
    ctx.fillStyle = 'rgba(16, 16, 16, 0.95)';
    ctx.fill();
    ctx.strokeStyle = dim.color;
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';

    ctx.font = '700 13px Crimson Pro, serif';
    ctx.fillStyle = dim.color;
    ctx.fillText(dim.label + ' (' + dim.symbol + ')', tooltipX + padding, tooltipY + padding);

    ctx.font = '600 11px Inter, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('Current: ' + (values[activeIndex] * 100).toFixed(1) + '%', tooltipX + padding, tooltipY + padding + 18);

    ctx.font = '400 10px Inter, sans-serif';
    ctx.fillStyle = '#a0a8c0';
    wrapText(ctx, dim.description, tooltipX + padding, tooltipY + padding + 35, tooltipWidth - padding * 2, 13);

    // Draw "Tap to explore" link
    ctx.font = '600 11px Inter, sans-serif';
    ctx.fillStyle = '#D4AF37';
    ctx.fillText('Tap to explore →', tooltipX + padding, tooltipY + tooltipHeight - padding - 12);
  }

  function wrapText(context, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = context.measureText(testLine);
      if (metrics.width > maxWidth && n > 0) {
        context.fillText(line.trim(), x, y);
        line = words[n] + ' ';
        y += lineHeight;
      } else {
        line = testLine;
      }
    }
    context.fillText(line.trim(), x, y);
  }

  function handleMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;

    hoveredIndex = -1;
    for (let i = 0; i < 7; i++) {
      const point = getAxisPoint(i, values[i]);
      const labelPoint = getAxisPoint(i, 1.15);

      const distToPoint = Math.sqrt(
        Math.pow(mouseX - point.x, 2) +
        Math.pow(mouseY - point.y, 2)
      );

      const distToLabel = Math.sqrt(
        Math.pow(mouseX - labelPoint.x, 2) +
        Math.pow(mouseY - labelPoint.y, 2)
      );

      if (distToPoint < 15 || distToLabel < 18) {
        hoveredIndex = i;
        canvas.style.cursor = 'pointer';
        break;
      }
    }

    if (hoveredIndex === -1) {
      canvas.style.cursor = 'default';
    }
  }

  function handleMouseLeave() {
    hoveredIndex = -1;
    canvas.style.cursor = 'default';
  }

  function handleClick(e) {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Check if clicking on tooltip (navigate to dimension)
    if (tooltipBounds && selectedIndex >= 0) {
      if (clickX >= tooltipBounds.x && clickX <= tooltipBounds.x + tooltipBounds.width &&
          clickY >= tooltipBounds.y && clickY <= tooltipBounds.y + tooltipBounds.height) {
        // Navigate to dimension
        const dim = DIMENSIONS[tooltipBounds.dimIndex];
        const tabId = dim.label.toLowerCase();
        const tabs = document.querySelectorAll('.md-typeset .tabbed-labels label');
        tabs.forEach(tab => {
          if (tab.textContent.trim().toLowerCase() === tabId) {
            tab.click();
            const section = document.getElementById('dimension-lens');
            if (section) {
              section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }
        });
        selectedIndex = -1;
        tooltipBounds = null;
        return;
      }
    }

    // Check if clicking on a node (show tooltip)
    for (let i = 0; i < 7; i++) {
      const point = getAxisPoint(i, values[i]);
      const labelPoint = getAxisPoint(i, 1.15);

      const distToPoint = Math.sqrt(
        Math.pow(clickX - point.x, 2) +
        Math.pow(clickY - point.y, 2)
      );

      const distToLabel = Math.sqrt(
        Math.pow(clickX - labelPoint.x, 2) +
        Math.pow(clickY - labelPoint.y, 2)
      );

      if (distToPoint < 20 || distToLabel < 22) {
        selectedIndex = i;
        return;
      }
    }

    // Clicking elsewhere dismisses tooltip
    selectedIndex = -1;
    tooltipBounds = null;
  }

  // Polyfill for roundRect
  if (!CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
      if (w < 2 * r) r = w / 2;
      if (h < 2 * r) r = h / 2;
      this.moveTo(x + r, y);
      this.arcTo(x + w, y, x + w, y + h, r);
      this.arcTo(x + w, y + h, x, y + h, r);
      this.arcTo(x, y + h, x, y, r);
      this.arcTo(x, y, x + w, y, r);
      this.closePath();
      return this;
    };
  }

  // Cleanup function for re-initialization
  function destroy() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
    if (canvas) {
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mouseleave', handleMouseLeave);
      canvas.removeEventListener('click', handleClick);
      canvas.removeAttribute('data-initialized');
    }
    window.removeEventListener('resize', resizeCanvas);
    canvas = null;
    ctx = null;
  }

  // Safe initialization that checks if already running
  function safeInit() {
    const container = document.getElementById('tensor-viz-container');
    const canvasEl = document.getElementById('tensor-canvas');

    // Only initialize if container exists and canvas isn't already initialized
    if (container && canvasEl) {
      if (canvasEl.hasAttribute('data-initialized')) {
        return; // Already running
      }
      destroy(); // Clean up any previous instance
      init();
      canvasEl.setAttribute('data-initialized', 'true');
    }
  }

  // Initial load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', safeInit);
  } else {
    safeInit();
  }

  // MkDocs Material instant navigation support
  // Listen for location changes (works with instant navigation)
  let lastUrl = location.href;
  new MutationObserver(function() {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      // Small delay to let MkDocs Material finish rendering
      setTimeout(safeInit, 50);
    }
  }).observe(document, { subtree: true, childList: true });

  // Also handle browser back/forward navigation
  window.addEventListener('popstate', function() {
    setTimeout(safeInit, 50);
  });
})();
