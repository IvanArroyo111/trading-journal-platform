// Handles chart switching and renders analytics charts for the reports page

/**
 * Show the selected chart and hide others.
 * @param {string} chartId - The ID of the chart to display ('equity', 'weekday', or 'setup').
 */
function showChart(chartId) {
  document.getElementById('equityChartContainer').style.display = chartId === 'equity' ? 'block' : 'none';
  document.getElementById('weekdayChartContainer').style.display = chartId === 'weekday' ? 'block' : 'none';
  document.getElementById('setupChartContainer').style.display = chartId === 'setup' ? 'block' : 'none';
}

// Equity Curve Chart
const equityDates = JSON.parse(document.getElementById('equity-dates').textContent);
const equityValues = JSON.parse(document.getElementById('equity-values').textContent);
new Chart(document.getElementById('equityChart').getContext('2d'), {
  type: 'line',
  data: {
    labels: equityDates,
    datasets: [{
      label: 'Equity Curve',
      data: equityValues,
      borderColor: '#00e6d0',
      backgroundColor: 'rgba(0,230,208,0.10)',
      fill: true,
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#00e6d0' } },
      tooltip: {
        backgroundColor: '#23232a',
        titleColor: '#00e6d0',
        bodyColor: '#fff',
        borderColor: '#00e6d0',
        borderWidth: 1
      }
    },
    scales: {
      x: { grid: { color: '#23232a' }, ticks: { color: '#00e6d0' } },
      y: { grid: { color: '#23232a' }, ticks: { color: '#00e6d0' } }
    }
  }
});

// PnL by Weekday Bar Chart
const weekdayLabels = JSON.parse(document.getElementById('weekday-labels').textContent);
const weekdayData = JSON.parse(document.getElementById('weekday-data').textContent);
new Chart(document.getElementById('weekdayChart').getContext('2d'), {
  type: 'bar',
  data: {
    labels: weekdayLabels,
    datasets: [{
      label: 'PnL by Weekday',
      data: weekdayData,
      backgroundColor: weekdayData.map(v => v >= 0 ? '#19e37d' : '#ff4d6d'),
      borderColor: '#00e6d0',
      borderWidth: 2,
      borderRadius: 10,
      barPercentage: 0.32,
      categoryPercentage: 0.5,
      hoverBackgroundColor: '#00e6d0',
      hoverBorderColor: '#00e6d0'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#23232a',
        titleColor: '#00e6d0',
        bodyColor: '#fff',
        borderColor: '#00e6d0',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: '#00e6d0', font: { weight: 'bold' } }
      },
      y: {
        grid: { color: '#23232a' },
        ticks: { color: '#00e6d0' }
      }
    }
  }
});

// Trade Setups Pie Chart
const setupLabels = JSON.parse(document.getElementById('setup-labels').textContent);
const setupValues = JSON.parse(document.getElementById('setup-values').textContent);
new Chart(document.getElementById('setupChart').getContext('2d'), {
  type: 'pie',
  data: {
    labels: setupLabels,
    datasets: [{
      data: setupValues,
      backgroundColor: [
        '#00e6d0', // cyan
        '#19e37d', // green
        '#fbbf24', // yellow
        '#ff4d6d', // red
        '#6366f1', // indigo
        '#a78bfa', // purple
        '#f59e42', // orange
        '#14b8a6', // teal
        '#eab308', // gold
        '#64748b'  // slate
      ]
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#00e6d0' } }
    }
  }
});