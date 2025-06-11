// Renders the equity curve chart on the dashboard using Chart.js

document.addEventListener('DOMContentLoaded', function() {
    if (window.Chart) {
        // Parse equity data from DOM
        const equityDates = JSON.parse(document.getElementById('equity-dates').textContent);
        const equityValues = JSON.parse(document.getElementById('equity-values').textContent);

        // Get chart context
        const ctx = document.getElementById('equityChart').getContext('2d');

        // Initialize Chart.js line chart
        const equityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: equityDates,
                datasets: [{
                    label: 'Equity Curve',
                    data: equityValues,
                    borderColor: '#00e6d0',
                    backgroundColor: 'rgba(0,230,208,0.10)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#18181c',
                        titleColor: '#00e6d0',
                        bodyColor: '#e0e6ed'
                    },
                    legend: { display: false }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date',
                            color: '#00e6d0',
                            font: { weight: 'bold' }
                        },
                        ticks: { color: '#b0bac9' },
                        grid: { display: false }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Account Balance',
                            color: '#00e6d0',
                            font: { weight: 'bold' },
                            padding: { top: 0, bottom: 20 }
                        },
                        ticks: { color: '#b0bac9' },
                        grid: {
                            color: '#23232a',
                            borderDash: [4, 4]
                        }
                    }
                }
            }
        });
    }
});