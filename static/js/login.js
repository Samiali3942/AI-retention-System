// login.js - Enhanced Login/Signup Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginEmailInput = document.getElementById('loginEmail');
    const loginPasswordInput = document.getElementById('loginPassword');
    const signupNameInput = document.getElementById('signupName');
    const signupEmailInput = document.getElementById('signupEmail');
    const signupPasswordInput = document.getElementById('signupPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const rememberMeCheckbox = document.getElementById('rememberMe');
    const agreeTermsCheckbox = document.getElementById('agreeTerms');
    const loginButton = document.getElementById('loginButton');
    const signupButton = document.getElementById('signupButton');
    const toggleLoginPasswordButton = document.getElementById('toggleLoginPassword');
    const toggleSignupPasswordButton = document.getElementById('toggleSignupPassword');
    const toggleConfirmPasswordButton = document.getElementById('toggleConfirmPassword');
    const loginAlertContainer = document.getElementById('loginAlertContainer');
    const signupAlertContainer = document.getElementById('signupAlertContainer');
    const authSubtitle = document.getElementById('authSubtitle');
    
    // Tab switching functionality
    window.switchTab = function(tab) {
        const loginTab = document.getElementById('loginTab');
        const signupTab = document.getElementById('signupTab');
        const loginSection = document.getElementById('loginSection');
        const signupSection = document.getElementById('signupSection');
        
        if (tab === 'login') {
            // Switch to login
            loginTab.classList.add('active');
            signupTab.classList.remove('active');
            loginSection.classList.add('active');
            signupSection.classList.remove('active');
            authSubtitle.textContent = 'Sign in to your account';
            clearAlert('both');
            loginEmailInput.focus();
        } else if (tab === 'signup') {
            // Switch to signup
            signupTab.classList.add('active');
            loginTab.classList.remove('active');
            signupSection.classList.add('active');
            loginSection.classList.remove('active');
            authSubtitle.textContent = 'Create your account';
            clearAlert('both');
            signupNameInput.focus();
        }
    };
    
    // Toggle password visibility for login
    if (toggleLoginPasswordButton) {
        toggleLoginPasswordButton.addEventListener('click', function() {
            togglePasswordVisibility(loginPasswordInput, this);
        });
    }
    
    // Toggle password visibility for signup
    if (toggleSignupPasswordButton) {
        toggleSignupPasswordButton.addEventListener('click', function() {
            togglePasswordVisibility(signupPasswordInput, this);
        });
    }
    
    // Toggle password visibility for confirm password
    if (toggleConfirmPasswordButton) {
        toggleConfirmPasswordButton.addEventListener('click', function() {
            togglePasswordVisibility(confirmPasswordInput, this);
        });
    }
    
    function togglePasswordVisibility(passwordInput, button) {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = button.querySelector('i');
        if (type === 'text') {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
    
    // Show alert message
    function showAlert(message, type = 'danger', container = 'login') {
        const alertContainer = container === 'login' ? loginAlertContainer : signupAlertContainer;
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        alertContainer.innerHTML = alertHtml;
    }
    
    // Clear alert
    function clearAlert(container = 'both') {
        if (container === 'both' || container === 'login') {
            loginAlertContainer.innerHTML = '';
        }
        if (container === 'both' || container === 'signup') {
            signupAlertContainer.innerHTML = '';
        }
    }
    
    // Set loading state for login
    function setLoginLoadingState(isLoading) {
        const btnText = loginButton.querySelector('.login-btn-text');
        const btnSpinner = loginButton.querySelector('.login-btn-spinner');
        
        if (isLoading) {
            loginButton.disabled = true;
            btnText.classList.add('d-none');
            btnSpinner.classList.remove('d-none');
        } else {
            loginButton.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    }
    
    // Set loading state for signup
    function setSignupLoadingState(isLoading) {
        const btnText = signupButton.querySelector('.signup-btn-text');
        const btnSpinner = signupButton.querySelector('.signup-btn-spinner');
        
        if (isLoading) {
            signupButton.disabled = true;
            btnText.classList.add('d-none');
            btnSpinner.classList.remove('d-none');
        } else {
            signupButton.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    }
    
    // Validate password strength
    function validatePasswordStrength(password) {
        if (password.length < 8) {
            return 'Password must be at least 8 characters long';
        }
        if (!/[A-Z]/.test(password)) {
            return 'Password must contain at least one uppercase letter';
        }
        if (!/[a-z]/.test(password)) {
            return 'Password must contain at least one lowercase letter';
        }
        if (!/\d/.test(password)) {
            return 'Password must contain at least one number';
        }
        return null;
    }
    
    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Clear previous alerts
            clearAlert('login');
            
            // Basic validation
            if (!loginEmailInput.value.trim() || !loginPasswordInput.value) {
                showAlert('Please enter both email and password', 'danger', 'login');
                return;
            }
            
            // Set loading state
            setLoginLoadingState(true);
            
            // Prepare form data
            const formData = {
                email: loginEmailInput.value.trim(),
                password: loginPasswordInput.value,
                remember_me: rememberMeCheckbox.checked
            };
            
            try {
                // Submit login request
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show success message
                    showAlert(data.message, 'success', 'login');
                    
                    // Redirect after a short delay
                    setTimeout(() => {
                        window.location.href = data.redirect_url || '/';
                    }, 1500);
                    
                } else {
                    // Show error message
                    showAlert(data.message, 'danger', 'login');
                    setLoginLoadingState(false);
                }
                
            } catch (error) {
                console.error('Login error:', error);
                showAlert('An unexpected error occurred. Please try again.', 'danger', 'login');
                setLoginLoadingState(false);
            }
        });
    }
    
    // Handle signup form submission
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Clear previous alerts
            clearAlert('signup');
            
            // Basic validation
            if (!signupNameInput.value.trim()) {
                showAlert('Please enter your full name', 'danger', 'signup');
                return;
            }
            
            if (!signupEmailInput.value.trim()) {
                showAlert('Please enter your email address', 'danger', 'signup');
                return;
            }
            
            if (!signupPasswordInput.value) {
                showAlert('Please enter a password', 'danger', 'signup');
                return;
            }
            
            // Validate password strength
            const passwordError = validatePasswordStrength(signupPasswordInput.value);
            if (passwordError) {
                showAlert(passwordError, 'danger', 'signup');
                return;
            }
            
            // Check if passwords match
            if (signupPasswordInput.value !== confirmPasswordInput.value) {
                showAlert('Passwords do not match', 'danger', 'signup');
                return;
            }
            
            // Check if terms are agreed
            if (!agreeTermsCheckbox.checked) {
                showAlert('Please agree to the Terms and Conditions', 'danger', 'signup');
                return;
            }
            
            // Set loading state
            setSignupLoadingState(true);
            
            // Prepare form data
            const formData = {
                name: signupNameInput.value.trim(),
                email: signupEmailInput.value.trim(),
                password: signupPasswordInput.value,
                confirm_password: confirmPasswordInput.value
            };
            
            try {
                // Submit signup request
                const response = await fetch('/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show success message
                    showAlert(data.message, 'success', 'signup');
                    
                    // Redirect to login or dashboard after a short delay
                    setTimeout(() => {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        } else {
                            // Switch to login tab
                            switchTab('login');
                            showAlert('Account created successfully! Please sign in.', 'success', 'login');
                        }
                    }, 1500);
                    
                } else {
                    // Show error message
                    showAlert(data.message, 'danger', 'signup');
                    setSignupLoadingState(false);
                }
                
            } catch (error) {
                console.error('Signup error:', error);
                showAlert('An unexpected error occurred. Please try again.', 'danger', 'signup');
                setSignupLoadingState(false);
            }
        });
    }
    
    // Focus on email field on page load
    if (loginEmailInput) {
        loginEmailInput.focus();
    }
});

// Function to fill demo credentials (updated to use new IDs)
function fillLoginCredentials(email, password) {
    document.getElementById('loginEmail').value = email;
    document.getElementById('loginPassword').value = password;
    document.getElementById('loginButton').focus();
}