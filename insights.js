// Example static insights for testing; later you could fetch JSON dynamically
const insightsData = {
  themes: {"Environment": 10, "Transport": 7, "Education": 5},
  statuses: {"Successful": 15, "Awaiting": 5, "Refused": 3}
};

function buildChart(ctxId, labels, data) {
  new Chart(document.getElementById(ctxId), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: ctxId,
        data: data,
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }]
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  buildChart('themeChart', Object.keys(insightsData.themes), Object.values(insightsData.themes));
  buildChart('statusChart', Object.keys(insightsData.statuses), Object.values(insightsData.statuses));
});
