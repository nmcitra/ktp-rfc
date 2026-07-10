# AGENTS.md - KTP RFC Style Guidelines

## Writing Style

### Capitalization
- Use "Internet" not "internet" (proper noun)
- Use "Web" not "web" when referring to the World Wide Web

### Terminology
- E_base = Performance (ARQ-derived score)
- E_trust = Final trust score (after risk deflation)
- Context Tensor (not "7-Dim Tensor" - future-proof naming)

## Design Principles

### Mobile-First
- **All diagrams and visualizations must be designed mobile-first**
- Start with single-column, vertical layouts
- Use `min-width` media queries to expand for larger screens
- Test all visual components at 320px width minimum

### CSS Pattern
```css
/* Mobile first - base styles */
.component {
  flex-direction: column;
  padding: 1rem;
}

/* Tablet and up */
@media screen and (min-width: 640px) {
  .component {
    flex-direction: row;
    padding: 1.5rem;
  }
}

/* Desktop */
@media screen and (min-width: 900px) {
  .component {
    padding: 2rem;
  }
}
```

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 899px
- Desktop: 900px+

## Visual Components

### Monograms
- Two-character format: Primary letter large, secondary letter smaller
- Example: `Ma` for Mass, `Mo` for Momentum
- Gold color (#D4AF37) for primary character

### Color Palette
- Primary accent: #88ccee (sky blue)
- Gold/Trust: #D4AF37
- Heat/Warning: #cc6677
- Soul: #D4AF37 (gold)
- Background dark: rgba(26, 31, 54, 0.95)

### Interactive Elements
- All clickable cards need hover states
- Use `transform: translateY(-2px)` for lift effect
- Border color intensifies on hover

## MkDocs Material

### Instant Navigation
- JavaScript must handle page navigation events
- Use MutationObserver for URL change detection
- Clean up previous instances before reinitializing

### Front Matter
- Use `hide: - toc` to hide right sidebar when needed
- Keep left navigation visible for context
