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

// Helper: check admin password only once per session
function ensureAdminPassword(callback) {
    if (sessionStorage.getItem('isAdmin') === 'true') {
        callback();
        return;
    }
    const input = prompt("Admin only! Please enter the admin password:");
    if (input === "menoo20") { // Or use a variable if you want
        sessionStorage.setItem('isAdmin', 'true');
        // Set the password field for the form if needed
        const pwInput = document.querySelector('#addStudentForm input[name="password"]');
        if (pwInput) pwInput.value = input;
        callback();
    } else if (input !== null) {
        alert("Incorrect password. Action cancelled.");
    }
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

    // Single delete
    $(document).on('click', '.btn-delete-student', function() {
        const studentId = $(this).data('id');
        if (confirm('Are you sure you want to delete this student?')) {
            fetch(`/delete_student/${studentId}`, {method: 'POST'})
                .then(() => {
                    refreshTableAndStats();
                    window.location.reload();
                });
        }
    });

    // Bulk delete
    $(document).on('click', '#deleteSelectedBtn', function() {
        const ids = $('.student-checkbox:checked').map(function() {
            return $(this).data('id');
        }).get();
        if (ids.length && confirm('Delete selected students?')) {
            fetch('/delete_students', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ids})
            }).then(() => {
                refreshTableAndStats();
                window.location.reload();
            });
        }
    });

    // Intercept the "Add New Student" button to prompt for password before showing modal
    const addBtn = document.querySelector('[data-bs-target="#addStudentModal"]');
    if (addBtn) {
        addBtn.addEventListener('click', function(e) {
            e.preventDefault();
            ensureAdminPassword(function() {
                // Set password in hidden field for form submission
                const pwInput = document.querySelector('#addStudentForm input[name="password"]');
                if (pwInput) pwInput.value = "menoo20";
                // Show the modal
                var modal = new bootstrap.Modal(document.getElementById('addStudentModal'));
                modal.show();
            });
        });
    }

    // Add Student Form Submit (protect with password prompt)
    const addStudentForm = document.getElementById('addStudentForm');
    if (addStudentForm) {
        addStudentForm.addEventListener('submit', function(e) {
            if (sessionStorage.getItem('isAdmin') === 'true') {
                // Set password in hidden field for form submission
                const pwInput = document.querySelector('#addStudentForm input[name="password"]');
                if (pwInput) pwInput.value = "menoo20";
                // Allow submit
            } else {
                e.preventDefault();
                ensureAdminPassword(function() {
                    addStudentForm.submit();
                });
            }
        });
    }
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
                    
                    // Refresh data and charts
                    refreshTableAndStats();
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
