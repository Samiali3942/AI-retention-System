// login.js

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const loginButton = document.getElementById('loginButton');
    const fillDemoBtn = document.getElementById('fillDemoBtn');
    const alertContainer = document.getElementById('alertContainer');

    // Demo credentials
    const DEMO_CREDENTIALS = {
        email: 'admin@retentionai.com',
        password: 'admin123'
    };

    // Password toggle functionality
    passwordToggle.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = passwordToggle.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });

    // Fill demo credentials
    fillDemoBtn.addEventListener('click', function() {
        emailInput.value = DEMO_CREDENTIALS.email;
        passwordInput.value = DEMO_CREDENTIALS.password;
        
        // Add visual feedback
        emailInput.classList.add('is-valid');
        passwordInput.classList.add('is-valid');
        
        // Focus on login button
        loginButton.focus();
        
        showAlert('Demo credentials filled successfully!', 'success');
    });

    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Clear previous validation states
        emailInput.classList.remove('is-invalid', 'is-valid');
        passwordInput.classList.remove('is-invalid', 'is-valid');
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailInput.value.trim()) {
            setFieldError(emailInput, 'Email is required');
            isValid = false;
        } else if (!emailRegex.test(emailInput.value)) {
            setFieldError(emailInput, 'Please enter a valid email address');
            isValid = false;
        } else {
            setFieldSuccess(emailInput);
        }
        
        // Password validation
        if (!passwordInput.value.trim()) {
            setFieldError(passwordInput, 'Password is required');
            isValid = false;
        } else if (passwordInput.value.length < 6) {
            setFieldError(passwordInput, 'Password must be at least 6 characters');
            isValid = false;
        } else {
            setFieldSuccess(passwordInput);
        }
        
        return isValid;
    }

    function setFieldError(field, message) {
        field.classList.add('is-invalid');
        const feedback = field.parentElement.parentElement.querySelector('.invalid-feedback');
        feedback.textContent = message;
    }

    function setFieldSuccess(field) {
        field.classList.add('is-valid');
        const feedback = field.parentElement.parentElement.querySelector('.invalid-feedback');
        feedback.textContent = '';
    }

    // Show alert messages
    function showAlert(message, type = 'success') {
        // Remove existing alerts
        alertContainer.innerHTML = '';
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'}`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${message}
        `;
        
        alertContainer.appendChild(alertDiv);
        
        // Auto-remove alert after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Set loading state
    function setLoadingState(isLoading) {
        if (isLoading) {
            loginButton.disabled = true;
            loginButton.classList.add('loading');
            document.querySelector('.btn-text').style.display = 'none';
            document.querySelector('.btn-loader').style.display = 'inline-block';
        } else {
            loginButton.disabled = false;
            loginButton.classList.remove('loading');
            document.querySelector('.btn-text').style.display = 'inline';
            document.querySelector('.btn-loader').style.display = 'none';
        }
    }

    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }
        
        // Set loading state
        setLoadingState(true);
        
        // Get form data
        const formData = {
            email: emailInput.value.trim(),
            password: passwordInput.value,
            remember_me: document.getElementById('rememberMe').checked
        };
        
        try {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Make login request
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                // Show success message
                showAlert('Login successful! Redirecting...', 'success');
                
                // Redirect after a short delay
                setTimeout(() => {
                    window.location.href = result.redirect_url || '/';
                }, 1500);
                
            } else {
                // Show error message
                showAlert(result.message || 'Login failed. Please try again.', 'error');
                setLoadingState(false);
            }
            
        } catch (error) {
            console.error('Login error:', error);
            showAlert('An error occurred. Please try again.', 'error');
            setLoadingState(false);
        }
    });

    // Real-time validation on input
    emailInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailRegex.test(this.value)) {
                setFieldSuccess(this);
            } else {
                setFieldError(this, 'Please enter a valid email address');
            }
        }
    });

    passwordInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            if (this.value.length >= 6) {
                setFieldSuccess(this);
            } else {
                setFieldError(this, 'Password must be at least 6 characters');
            }
        }
    });

    // Clear validation on focus
    emailInput.addEventListener('focus', function() {
        this.classList.remove('is-invalid', 'is-valid');
        const feedback = this.parentElement.parentElement.querySelector('.invalid-feedback');
        feedback.textContent = '';
    });

    passwordInput.addEventListener('focus', function() {
        this.classList.remove('is-invalid', 'is-valid');
        const feedback = this.parentElement.parentElement.querySelector('.invalid-feedback');
        feedback.textContent = '';
    });

    // Handle Enter key press
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !loginButton.disabled) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-focus email field on page load
    setTimeout(() => {
        emailInput.focus();
    }, 500);
});