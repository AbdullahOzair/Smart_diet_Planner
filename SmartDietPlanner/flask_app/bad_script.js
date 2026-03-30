
    
    function showNotification(type, message) {
        console.log(`📢 Showing ${type} notification: ${message}`);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        notification.setAttribute('role', 'alert');
        notification.style.position = 'fixed';
        notification.style.top = '80px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        notification.style.borderRadius = '8px';
        notification.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }
    
    // Add Water Glass Function for water tracking page
    function addWaterGlass() {
        fetch('/api/add-water-glass', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('success', '✓ Water glass added! Hydrate well! 💧');
                // Refresh the page after a short delay to see updated data
                setTimeout(() => {
                    location.reload();
                }, 1000);
            } else {
                showNotification('error', '✗ Error adding water: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('error', '✗ Failed to add water');
        });
    }
    
    // Edit Profile Information
    function editProfileSection(section) {
        const modal = new bootstrap.Modal(document.getElementById('editModal'), {});
        document.getElementById('editModalTitle').textContent = `Edit ${section}`;
        
        // Store the section name in a data attribute for later use
        document.getElementById('editForm').dataset.section = section;
        
        let formFields = '';
        
        // Create specific form fields based on section
        if (section === 'Personal Information') {
            formFields = `
                <div class="mb-3">
                    <label for="firstName" class="form-label">First Name</label>
                    <input type="text" class="form-control" id="firstName" name="first_name" placeholder="First Name" required>
                </div>
                <div class="mb-3">
                    <label for="lastName" class="form-label">Last Name</label>
                    <input type="text" class="form-control" id="lastName" name="last_name" placeholder="Last Name" required>
                </div>
                <div class="mb-3">
                    <label for="age" class="form-label">Age (Years)</label>
                    <input type="number" class="form-control" id="age" name="age" placeholder="Age" min="10" max="120" required>
                </div>
            `;
        } else if (section === 'Body Metrics') {
            formFields = `
                <div class="mb-3">
                    <label for="height" class="form-label">Height (cm)</label>
                    <input type="number" class="form-control" id="height" name="height" placeholder="Height in cm" step="0.1" required>
                </div>
                <div class="mb-3">
                    <label for="weight" class="form-label">Current Weight (kg)</label>
                    <input type="number" class="form-control" id="weight" name="weight" placeholder="Current Weight" step="0.1" required>
                </div>
                <div class="mb-3">
                    <label for="goalWeight" class="form-label">Goal Weight (kg)</label>
                    <input type="number" class="form-control" id="goalWeight" name="goal_weight" placeholder="Goal Weight" step="0.1" required>
                </div>
            `;
        } else if (section === 'Lifestyle') {
            formFields = `
                <div class="mb-3">
                    <label for="fitnessLevel" class="form-label">Fitness Level</label>
                    <select class="form-control" id="fitnessLevel" name="fitness_level" required>
                        <option value="Sedentary">Sedentary</option>
                        <option value="Low Activity">Low Activity</option>
                        <option value="Moderate Activity">Moderate Activity</option>
                        <option value="High Activity">High Activity</option>
                        <option value="Very High Activity">Very High Activity</option>
                    </select>
                </div>
            `;
        } else if (section === 'Dietary Preferences') {
            formFields = `
                <div class="mb-3">
                    <label for="dietPref" class="form-label">Dietary Preference</label>
                    <select class="form-control" id="dietPref" name="dietary_preference" required>
                        <option value="Omnivore">Omnivore</option>
                        <option value="Vegetarian">Vegetarian</option>
                        <option value="Vegan">Vegan</option>
                        <option value="Keto">Keto</option>
                        <option value="Halal">Halal</option>
                    </select>
                </div>
            `;
        } else if (section === 'Health & Allergies') {
            formFields = `
                <div class="mb-3">
                    <label for="allergies" class="form-label">Allergies (comma-separated)</label>
                    <textarea class="form-control" id="allergies" name="allergies" placeholder="e.g., peanuts, dairy" rows="2"></textarea>
                </div>
                <div class="mb-3">
                    <label for="medConditions" class="form-label">Medical Conditions (comma-separated)</label>
                    <textarea class="form-control" id="medConditions" name="medical_conditions" placeholder="e.g., diabetes, hypertension" rows="2"></textarea>
                </div>
            `;
        }
        
        document.getElementById('editFormFields').innerHTML = formFields;
        modal.show();
    }
    
    // Save Profile Changes
    function saveProfileChanges(event) {
        event.preventDefault();
        
        const section = document.getElementById('editForm').dataset.section;
        const form = document.getElementById('editForm');
        const formData = new FormData(form);
        
        // Prepare data for API call - just save the first field with a value
        let fieldName = '';
        let fieldValue = '';
        
        for (let [key, value] of formData.entries()) {
            if (value && value.trim()) {
                fieldName = key;
                fieldValue = value.trim();
                break;
            }
        }
        
        if (!fieldName || !fieldValue) {
            showNotification('error', '❌ Please fill in at least one field');
            return;
        }
        
        // Call API to update profile
        fetch('/api/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                field: fieldName,
                value: fieldValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('success', `✓ ${data.message}`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                modal.hide();
                setTimeout(() => {
                    location.reload();
                }, 1000);
            } else {
                showNotification('error', `❌ ${data.error || 'Failed to update'}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('error', '❌ Error updating profile');
        });
    }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('error', 'Failed to update profile');
        });
    }
    
    function openWaterGoalModal() {
        console.log('🌊 Opening water goal edit modal');
        
        // Find all small elements with "Goal:" text
        let currentValue = '8';
        const smallElements = document.querySelectorAll('small');
        for (let el of smallElements) {
            if (el.textContent.includes('Goal:')) {
                const goalMatch = el.textContent.match(/Goal:\s*(\d+)\s*glasses/);
                if (goalMatch) {
                    // Convert glasses to liters (4 glasses = 1 liter)
                    currentValue = (goalMatch[1] / 4).toString();
                    break;
                }
            }
        }
        
        const modal = new bootstrap.Modal(document.getElementById('waterGoalModal'));
        document.getElementById('waterGoalInput').value = currentValue;
        modal.show();
    }
    
    function updateWaterGoal() {
        console.log('💾 Updating water goal');
        
        const waterGoalInput = document.getElementById('waterGoalInput');
        const submitBtn = document.getElementById('updateWaterGoalBtn');
        const waterValue = waterGoalInput.value.trim();
        
        if (!waterValue || isNaN(waterValue)) {
            showNotification('error', '❌ Please enter a valid number');
            return;
        }
        
        const waterGoal = waterValue + ' L';
        console.log(`Sending water goal: ${waterGoal}`);
        
        // Disable button during submission
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';
        
        fetch('/api/update-water-goal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ water_goal: waterGoal })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('✅ Water goal updated:', data);
                showNotification('success', `✅ ${data.message}`);
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('waterGoalModal'));
                modal.hide();
                
                // Update display after 1 second
                setTimeout(() => {
                    location.reload();
                }, 1000);
            } else {
                throw new Error(data.error || 'Failed to update water goal');
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            showNotification('error', `❌ ${error.message}`);
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Update Goal';
        });
    }
    
    // Allow Enter key to submit
    document.addEventListener('DOMContentLoaded', function() {
        const waterGoalInput = document.getElementById('waterGoalInput');
        if (waterGoalInput) {
            waterGoalInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    updateWaterGoal();
                }
            });
        }
    });
    