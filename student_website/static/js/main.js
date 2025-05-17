// Main JavaScript for the student dashboard

// Function to refresh charts with new data
function refreshCharts(data) {
    // Update proficiency chart
    if (window.proficiencyChart) {
        window.proficiencyChart.data.datasets[0].data = [
            data.proficiency_counts.Beginner || 0,
            data.proficiency_counts.Intermediate || 0
        ];
        window.proficiencyChart.update();
    }
    
    // Update instructor chart
    if (window.instructorChart) {
        window.instructorChart.data.datasets[0].data = [
            data.instructor_counts['Mr. Tawfeek'] || 0,
            data.instructor_counts['Mr. Mohammed Ameen'] || 0
        ];
        window.instructorChart.update();
    }
    
    // Update score distribution chart
    if (window.scoreChart) {
        // Count scores in each range
        const scoreRanges = [
            data.scores.filter(score => score <= 9).length,
            data.scores.filter(score => score >= 10 && score <= 19).length,
            data.scores.filter(score => score >= 20 && score <= 29).length,
            data.scores.filter(score => score >= 30 && score <= 39).length,
            data.scores.filter(score => score >= 40 && score <= 49).length,
            data.scores.filter(score => score >= 50 && score <= 59).length,
            data.scores.filter(score => score >= 60).length
        ];
        
        window.scoreChart.data.datasets[0].data = scoreRanges;
        window.scoreChart.update();
    }
    
    // Update statistics cards
    document.getElementById('totalStudents').textContent = data.total_students;
    document.getElementById('beginnerCount').textContent = data.proficiency_counts.Beginner || 0;
    document.getElementById('intermediateCount').textContent = data.proficiency_counts.Intermediate || 0;
    document.getElementById('avgScore').textContent = data.avg_score.toFixed(1);
}

// Function to refresh the student table
function refreshTable() {
    fetch('/api/students')
        .then(response => response.json())
        .then(data => {
            const table = $('#studentTable').DataTable();
            
            // Clear existing data
            table.clear();
            
            // Add new data
            data.forEach(student => {
                const proficiencyBadge = student.proficiency_level === 'Beginner' 
                    ? `<span class="badge bg-success">${student.proficiency_level}</span>`
                    : `<span class="badge bg-info">${student.proficiency_level}</span>`;
                
                table.row.add([
                    student.name,
                    student.email,
                    student.national_id,
                    student.company,
                    student.speaking_points,
                    student.total_points,
                    proficiencyBadge,
                    student.instructor
                ]);
            });
            
            // Redraw the table
            table.draw();
        })
        .catch(error => console.error('Error refreshing table:', error));
}

// Function to refresh all data
function refreshAllData() {
    // Refresh statistics and charts
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => refreshCharts(data))
        .catch(error => console.error('Error refreshing statistics:', error));
    
    // Refresh table
    refreshTable();
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Store chart references globally for later updates
    const proficiencyCtx = document.getElementById('proficiencyChart').getContext('2d');
    window.proficiencyChart = new Chart(proficiencyCtx, {
        type: 'pie',
        data: {
            labels: ['Beginner', 'Intermediate'],
            datasets: [{
                data: [0, 0], // Will be updated with actual data
                backgroundColor: ['#198754', '#0dcaf0'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    const instructorCtx = document.getElementById('instructorChart').getContext('2d');
    window.instructorChart = new Chart(instructorCtx, {
        type: 'pie',
        data: {
            labels: ['Mr. Tawfeek', 'Mr. Mohammed Ameen'],
            datasets: [{
                data: [0, 0], // Will be updated with actual data
                backgroundColor: ['#fd7e14', '#6f42c1'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    const scoreCtx = document.getElementById('scoreDistributionChart').getContext('2d');
    window.scoreChart = new Chart(scoreCtx, {
        type: 'bar',
        data: {
            labels: ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60+'],
            datasets: [{
                label: 'Number of Students',
                data: [0, 0, 0, 0, 0, 0, 0], // Will be updated with actual data
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Score Range'
                    }
                }
            }
        }
    });
    
    // Initial data load
    refreshAllData();
});

// Handle form submission via AJAX
document.addEventListener('DOMContentLoaded', function() {
    const addStudentForm = document.getElementById('addStudentForm');
    if (addStudentForm) {
        addStudentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(addStudentForm);
            
            fetch('/add_student', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // Close the modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
                    modal.hide();
                    
                    // Reset the form
                    addStudentForm.reset();
                    
                    // Show success message
                    const alertContainer = document.getElementById('alertContainer');
                    alertContainer.innerHTML = `
                        <div class="alert alert-success alert-dismissible fade show" role="alert">
                            Student added successfully!
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    `;
                    
                    // Refresh data
                    refreshAllData();
                } else {
                    throw new Error('Failed to add student');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Show error message
                const alertContainer = document.getElementById('alertContainer');
                alertContainer.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Failed to add student. Please try again.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;
            });
        });
    }
    
    // Preview proficiency level and instructor
    const totalPointsInput = document.getElementById('total_points');
    if (totalPointsInput) {
        totalPointsInput.addEventListener('input', function() {
            const points = parseInt(this.value) || 0;
            const proficiencyPreview = document.getElementById('proficiencyPreview');
            
            let proficiency, instructor, badgeClass;
            
            if (points < 30) {
                proficiency = 'Beginner';
                instructor = 'Mr. Tawfeek';
                badgeClass = 'bg-success';
            } else {
                proficiency = 'Intermediate';
                instructor = 'Mr. Mohammed Ameen';
                badgeClass = 'bg-info';
            }
            
            proficiencyPreview.textContent = `${proficiency} level - ${instructor}`;
            proficiencyPreview.className = `badge ${badgeClass}`;
        });
    }
});
