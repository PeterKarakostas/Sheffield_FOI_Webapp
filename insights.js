document.addEventListener('DOMContentLoaded', () => {
  fetch('/Sheffield_FOI_Webapp/insights_data.json')
    .then(response => response.json())
    .then(data => {
      renderChart('themeChart', 'Theme Distribution', data.themes);
      renderChart('tagChart', 'Tag Distribution', data.tags);
      renderChart('statusChart', 'Status Distribution', data.statuses);
    });

  function renderChart(canvasId, title, dataset) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: Object.keys(dataset),
        datasets: [{
          label: title,
          data: Object.values(dataset),
          backgroundColor: 'rgba(54, 162, 235, 0.6)'
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
});
