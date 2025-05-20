// Main JavaScript for the student dashboard

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
                    `<input type="checkbox" class="student-checkbox" data-id="${student.id}">`,
                    student.name,
                    student.email,
                    student.national_id,
                    student.company,
                    student.speaking_points,
                    student.total_points,
                    proficiencyBadge,
                    student.instructor,
                    `<button class="btn btn-danger btn-sm btn-delete-student" data-id="${student.id}">Delete</button>`
                ]);
            });
            
            // Redraw the table
            table.draw();
        })
        .catch(error => console.error('Error refreshing table:', error));
}

// Function to refresh the statistics pie charts
function refreshStudentStatsCharts() {
    fetch('/api/student_stats')
        .then(response => response.json())
        .then(data => {
            // Proficiency Pie Chart
            if (window.proficiencyPieChartInstance) {
                window.proficiencyPieChartInstance.data.labels = data.proficiency.labels;
                window.proficiencyPieChartInstance.data.datasets[0].data = data.proficiency.counts;
                window.proficiencyPieChartInstance.update();
            } else {
                const profCtx = document.getElementById('proficiencyPieChart').getContext('2d');
                window.proficiencyPieChartInstance = new Chart(profCtx, {
                    type: 'pie',
                    data: {
                        labels: data.proficiency.labels,
                        datasets: [{
                            data: data.proficiency.counts,
                            backgroundColor: ['#198754', '#0dcaf0'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
            }

            // Instructor Pie Chart
            if (window.instructorPieChartInstance) {
                window.instructorPieChartInstance.data.labels = data.instructor.labels;
                window.instructorPieChartInstance.data.datasets[0].data = data.instructor.counts;
                window.instructorPieChartInstance.update();
            } else {
                const instrCtx = document.getElementById('instructorPieChart').getContext('2d');
                window.instructorPieChartInstance = new Chart(instrCtx, {
                    type: 'pie',
                    data: {
                        labels: data.instructor.labels,
                        datasets: [{
                            data: data.instructor.counts,
                            backgroundColor: ['#fd7e14', '#6f42c1'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
            }
        });
}

// Function to refresh the student table and update stats charts
function refreshTableAndStats() {
    refreshTable();
    refreshStudentStatsCharts();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initial data load
    refreshTableAndStats();

    // Handle select all checkboxes
    $(document).on('change', '#selectAllStudents', function() {
        $('.student-checkbox').prop('checked', this.checked).trigger('change');
    });

    // Enable/disable delete selected button
    $(document).on('change', '.student-checkbox', function() {
        $('#deleteSelectedBtn').prop('disabled', $('.student-checkbox:checked').length === 0);
    });
});

// Handle form submission via AJAX
document.addEventListener('DOMContentLoaded', function() {
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
