document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('pointsDistributionChart');
    if (!chartCanvas) return;
    fetch('/api/student_points_distribution')
        .then(res => res.json())
        .then(data => {
            const ctx = chartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Number of Students',
                        data: data.counts,
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)',   // Blue
                            'rgba(255, 206, 86, 1)',   // Yellow
                            'rgba(75, 192, 192, 1)',   // Teal
                            'rgba(153, 102, 255, 1)',  // Purple
                            'rgba(255, 159, 64, 1)',   // Orange
                            'rgba(100, 181, 246, 1)'   // Light Blue
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, stepSize: 1 }
                    }
                }
            });
        });
});
