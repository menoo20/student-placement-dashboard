function createPointsDistributionChart(studentData) {
    // Calculate point ranges
    const ranges = {
        '1-15': 0,
        '16-30': 0,
        '31-45': 0,
        '46-60': 0
    };

    studentData.forEach(student => {
        const points = parseInt(student.total_points);
        if (points >= 1 && points <= 15) ranges['1-15']++;
        else if (points <= 30) ranges['16-30']++;
        else if (points <= 45) ranges['31-45']++;
        else if (points <= 60) ranges['46-60']++;
    });

    const ctx = document.getElementById('pointsDistributionChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['1-15', '16-30', '31-45', '46-60'],
            datasets: [{
                label: 'Number of Students',
                data: Object.values(ranges),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Student Points Distribution',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}
