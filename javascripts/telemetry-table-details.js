const initTelemetryRowDetails = (root = document) => {
  const detailSpans = root.querySelectorAll('.ktp-metric-detail');
  if (!detailSpans.length) return;

  detailSpans.forEach((span) => {
    const row = span.closest('tr');
    if (!row || row.dataset.ktpBound === 'true') return;

    row.dataset.ktpBound = 'true';
    row.classList.add('ktp-metric-row');

    row.addEventListener('click', (event) => {
      const cell = event.target.closest('td, th');
      if (!cell || !row.contains(cell)) return;

      const next = row.nextElementSibling;
      const isOpen = next && next.classList.contains('ktp-metric-detail-row');

      if (isOpen) {
        next.remove();
        row.classList.remove('is-open');
        return;
      }

      const meso = span.getAttribute('data-meso') || '';
      const macro = span.getAttribute('data-macro') || '';

      const detailRow = document.createElement('tr');
      detailRow.className = 'ktp-metric-detail-row';
      const detailCell = document.createElement('td');
      detailCell.colSpan = row.children.length || 3;
      detailCell.innerHTML = `
        <div class="ktp-metric-detail-card">
          <div><strong>Meso:</strong> ${meso}</div>
          <div><strong>Macro:</strong> ${macro}</div>
        </div>
      `;
      detailRow.appendChild(detailCell);

      row.insertAdjacentElement('afterend', detailRow);
      row.classList.add('is-open');
    });
  });
};

document.addEventListener('DOMContentLoaded', () => {
  initTelemetryRowDetails(document);
});

if (window.document$ && typeof window.document$.subscribe === 'function') {
  window.document$.subscribe(() => {
    initTelemetryRowDetails(document);
  });
}
