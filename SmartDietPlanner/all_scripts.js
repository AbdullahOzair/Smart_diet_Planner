
    function addWaterGlass() {
        console.log('🔵 addWaterGlass() called');
        
        const btn = document.getElementById('addWaterBtn');
        if (!btn) {
            console.error('❌ Button element not found!');
            return;
        }
        
        console.log('✅ Button found, proceeding with API call...');
        
        const originalHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Adding...';
        
        // Make API call with comprehensive error handling
        fetch('/api/add-water-glass', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'  // Include session cookies
        })
        .then(response => {
            console.log(`📊 Response status: ${response.status}`);
            
            if (response.status === 401) {
                throw new Error('Not authenticated - please log in first');
            }
            if (response.status === 500) {
                throw new Error('Server error - please check console logs');
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📦 API Response:', data);
            
            if (data.success) {
                console.log('✅ Success! Water glass added');
                
                // Restore button
                btn.disabled = false;
                btn.innerHTML = originalHTML;
                
                // Show success message
                showNotification('success', `💧 ${data.message}`);
                
                // Update water glass display dynamically without reload
                updateWaterGlassDisplay(data.water_glasses);
                
                // Also update all water displays on the page
                updateAllWaterDisplays(data.water_glasses);
                
            } else {
                throw new Error(data.error || 'Failed to add water glass');
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            btn.disabled = false;
            btn.innerHTML = originalHTML;
            showNotification('error', `❌ Error: ${error.message}`);
        });
    }
    
    function updateWaterGlassDisplay(glassCount) {
        console.log(`🥤 Updating water glass display to ${glassCount} glasses`);
        
        // Update the 8-glass visual indicator in the hydration tracker
        const waterGlasses = document.querySelectorAll('[style*="width: 40px; height: 40px"]');
        console.log(`Found ${waterGlasses.length} glass elements`);
        
        let glassesUpdated = 0;
        waterGlasses.forEach((glass, index) => {
            if (index < 8) {  // Only update the first 8 glasses
                if (index < glassCount) {
                    // Fill glass
                    glass.style.background = 'linear-gradient(135deg, #06b6d4, #22d3ee)';
                    glass.style.color = '#fff';
                    glass.style.boxShadow = '0 4px 12px rgba(6, 182, 212, 0.3)';
                    glass.style.borderColor = '#06b6d4';
                    glassesUpdated++;
                } else {
                    // Empty glass
                    glass.style.background = 'rgba(0,0,0,0.05)';
                    glass.style.color = 'var(--charcoal-400)';
                    glass.style.boxShadow = 'none';
                    glass.style.borderColor = 'rgba(0,0,0,0.1)';
                }
            }
        });
        console.log(`✅ Updated ${glassesUpdated} glasses`);
    }
    
    function updateAllWaterDisplays(glassCount) {
        console.log(`🔄 Updating all water displays on page to: ${glassCount} glasses`);
        
        // Update the main water display (X/8 glasses)
        // First, find the element that shows "X / 8 glasses"
        const waterGlassCountElements = document.querySelectorAll('h4');
        waterGlassCountElements.forEach(element => {
            if (element.textContent.includes('glasses')) {
                // Update only the water count part (before the /)
                const textContent = element.textContent;
                const goalMatch = textContent.match(/\/\s*(\d+)/);
                if (goalMatch) {
                    const goal = goalMatch[1];
                    element.textContent = `${glassCount}/${goal} `;
                    // Re-add the "glasses" span
                    const span = document.createElement('span');
                    span.style.fontSize = '0.7em';
                    span.style.color = 'var(--charcoal-500)';
                    span.innerHTML = `glasses`;
                    element.appendChild(span);
                }
            }
        });
        
        // Update progress bar percentage if it exists
        updateWaterProgressBar(glassCount);
    }
    
    function updateWaterProgressBar(glassCount) {
        // Find and update water progress percentage
        // Assuming 8 glasses is the goal
        const waterGoal = 8;
        const percentage = Math.min((glassCount / waterGoal) * 100, 100);
        console.log(`📊 Water progress: ${glassCount}/${waterGoal} = ${percentage}%`);
        
        // Find all progress bars that might be water-related
        const progressBars = document.querySelectorAll('[style*="background: linear-gradient(90deg"]');
        progressBars.forEach(bar => {
            // Check if this is the water bar (cyan color #06b6d4)
            if (bar.style.background && bar.style.background.includes('06b6d4')) {
                bar.style.width = percentage + '%';
            }
        });
    }
    
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
        
        // Create specific form fields based on section with current values pre-filled
        if (section === 'Personal Information') {
            formFields = `
                <div class="mb-3">
                    <label for="firstName" class="form-label">First Name</label>
                    <input type="text" class="form-control" id="firstName" name="first_name" placeholder="First Name" value="Test" required>
                </div>
                <div class="mb-3">
                    <label for="lastName" class="form-label">Last Name</label>
                    <input type="text" class="form-control" id="lastName" name="last_name" placeholder="Last Name" value="User" required>
                </div>
                <div class="mb-3">
                    <label for="dob" class="form-label">Date of Birth</label>
                    <input type="date" class="form-control" id="dob" name="date_of_birth" value="1990-01-01" required>
                </div>
            `;
        } else if (section === 'Body Metrics') {
            formFields = `
                <div class="mb-3">
                    <label for="height" class="form-label">Height (cm)</label>
                    <input type="number" class="form-control" id="height" name="height" placeholder="Height in cm" step="0.1" value="170.00" required>
                </div>
                <div class="mb-3">
                    <label for="weight" class="form-label">Current Weight (kg)</label>
                    <input type="number" class="form-control" id="weight" name="weight" placeholder="Current Weight" step="0.1" value="70.00" required>
                </div>
                <div class="mb-3">
                    <label for="targetWeight" class="form-label">Target Weight (kg)</label>
                    <input type="number" class="form-control" id="targetWeight" name="target_weight" placeholder="Target Weight" step="0.1" value="" required>
                </div>
            `;
        } else if (section === 'Lifestyle') {
            const currentLevel = "Active";
            formFields = `
                <div class="mb-3">
                    <label for="activityLevel" class="form-label">Activity Level</label>
                    <select class="form-control" id="activityLevel" name="activity_level" required>
                        <option value="Sedentary" ${currentLevel === 'Sedentary' ? 'selected' : ''}>Sedentary</option>
                        <option value="Light" ${currentLevel === 'Light' ? 'selected' : ''}>Light</option>
                        <option value="Moderate" ${currentLevel === 'Moderate' ? 'selected' : ''}>Moderate</option>
                        <option value="Active" ${currentLevel === 'Active' ? 'selected' : ''}>Active</option>
                        <option value="Very Active" ${currentLevel === 'Very Active' ? 'selected' : ''}>Very Active</option>
                    </select>
                </div>
            `;
        } else if (section === 'Dietary Preferences') {
            const currentDiet = "None";
            formFields = `
                <div class="mb-3">
                    <label for="dietPref" class="form-label">Dietary Preference</label>
                    <select class="form-control" id="dietPref" name="dietary_preference" required>
                        <option value="Omnivore" ${currentDiet === 'Omnivore' ? 'selected' : ''}>Omnivore</option>
                        <option value="Vegetarian" ${currentDiet === 'Vegetarian' ? 'selected' : ''}>Vegetarian</option>
                        <option value="Vegan" ${currentDiet === 'Vegan' ? 'selected' : ''}>Vegan</option>
                        <option value="Keto" ${currentDiet === 'Keto' ? 'selected' : ''}>Keto</option>
                        <option value="Halal" ${currentDiet === 'Halal' ? 'selected' : ''}>Halal</option>
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
                    <label for="healthCondition" class="form-label">Medical Conditions (comma-separated)</label>
                    <textarea class="form-control" id="healthCondition" name="health_condition" placeholder="e.g., diabetes, hypertension" rows="2">None</textarea>
                </div>
            `;
        }
        
        document.getElementById('editFormFields').innerHTML = formFields;
        modal.show();
    }
    
    // Save Profile Changes
    function saveProfileChanges(event) {
        event.preventDefault();
        
        const form = document.getElementById('editForm');
        const formData = new FormData(form);
        
        // Prepare data for API call - collect all fields
        let updates = {};
        
        for (let [key, value] of formData.entries()) {
            updates[key] = value.trim();
        }
        
        if (Object.keys(updates).length === 0) {
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
            body: JSON.stringify({ updates: updates })
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
    
    function openWaterGoalModal(litersValue) {
        console.log('🌊 Opening water goal edit modal. Given value:', litersValue);
        
        let currentValue = '2';
        
        // Use the passed value from python backend if valid
        if (litersValue && !isNaN(parseFloat(litersValue))) {
            currentValue = parseFloat(litersValue).toString();
        } else {
            // Fallback to text parsing if needed
            const smallElements = document.querySelectorAll('small');
            for (let el of smallElements) {
                if (el.textContent.includes('Goal:')) {
                    const goalMatch = el.textContent.match(/Goal:\s*(\d+)\s*glasses/);
                    if (goalMatch) {
                        currentValue = (goalMatch[1] / 4).toString();
                        break;
                    }
                }
            }
        }
        
        const modal = new bootstrap.Modal(document.getElementById('waterGoalModal'));
        const inputField = document.getElementById('waterGoalInput');
        inputField.value = currentValue;
        
        // Dispatch input event to update calculations live
        inputField.dispatchEvent(new Event('input'));
        
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
    

    document.addEventListener('DOMContentLoaded', function() {
        const waterGoalInput = document.getElementById('waterGoalInput');
        if (waterGoalInput) {
            waterGoalInput.addEventListener('input', function() {
                const liters = this.value || '8';
                const glasses = Math.floor(liters * 4);
                document.getElementById('currentGoalDisplay').textContent = liters + ' L';
                document.getElementById('goalGlassesDisplay').textContent = glasses + ' glasses';
            });
        }
    });
    

        document.addEventListener('DOMContentLoaded', function() {
            const sidebarToggle = document.getElementById('sidebarToggle');
            const sidebar = document.querySelector('.sidebar');
            
            if (sidebarToggle && sidebar) {
                sidebarToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    sidebar.classList.toggle('show');
                });
                
                // Close sidebar when clicking outside
                document.addEventListener('click', function(e) {
                    if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                        sidebar.classList.remove('show');
                    }
                });
                
                // Close sidebar when navigation link is clicked
                const sidebarLinks = sidebar.querySelectorAll('a');
                sidebarLinks.forEach(link => {
                    link.addEventListener('click', function() {
                        sidebar.classList.remove('show');
                    });
                });
            }
        });
    
