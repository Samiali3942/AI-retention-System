document.addEventListener('DOMContentLoaded', function() {
    // Initialize navbar functionality
    initNavbar();
});

function initNavbar() {
    // Search functionality
    initSearch();
    
    // Scroll effect
    initScrollEffect();
    
    // Notification handling
    initNotifications();
    
    // Mobile responsiveness
    initMobileHandling();
}

// Search Functionality
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.getElementById('navbarSearch');
    
    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleSearch();
        });
        
        // Real-time search suggestions (optional)
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                showSearchSuggestions(query);
            } else {
                hideSearchSuggestions();
            }
        });
        
        // Close suggestions on click outside
        document.addEventListener('click', function(e) {
            if (!searchForm.contains(e.target)) {
                hideSearchSuggestions();
            }
        });
    }
}

function handleSearch() {
    const searchInput = document.getElementById('navbarSearch');
    const query = searchInput.value.trim();
    
    if (query) {
        // Redirect to customers page with search query
        window.location.href = `/customers?search=${encodeURIComponent(query)}`;
    }
}

function showSearchSuggestions(query) {
    // Create or update search suggestions dropdown
    let suggestionsContainer = document.getElementById('searchSuggestions');
    
    if (!suggestionsContainer) {
        suggestionsContainer = document.createElement('div');
        suggestionsContainer.id = 'searchSuggestions';
        suggestionsContainer.className = 'search-suggestions dropdown-menu show';
        suggestionsContainer.style.position = 'absolute';
        suggestionsContainer.style.top = '100%';
        suggestionsContainer.style.left = '0';
        suggestionsContainer.style.right = '0';
        
        const searchForm = document.querySelector('.search-form');
        searchForm.style.position = 'relative';
        searchForm.appendChild(suggestionsContainer);
    }
    
    // Mock suggestions
    const suggestions = [
        `Customers matching "${query}"`,
        `High-risk customers with "${query}"`,
        `Recent predictions for "${query}"`
    ];
    
    suggestionsContainer.innerHTML = suggestions
        .map(suggestion => `
            <a class="dropdown-item search-suggestion" href="#" data-query="${query}">
                <i class="fas fa-search me-2"></i>${suggestion}
            </a>
        `).join('');
    
    // Add click handlers for suggestions
    suggestionsContainer.querySelectorAll('.search-suggestion').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const query = this.getAttribute('data-query');
            document.getElementById('navbarSearch').value = query;
            handleSearch();
        });
    });
}

function hideSearchSuggestions() {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    if (suggestionsContainer) {
        suggestionsContainer.remove();
    }
}

// Scroll Effect for Navbar
function initScrollEffect() {
    const navbar = document.querySelector('.custom-navbar');
    if (!navbar) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class for styling
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Hide/show navbar on scroll (optional - commented out to prevent issues)
        /*
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        */
        
        lastScrollTop = scrollTop;
    });
}

// Notification Handling
function initNotifications() {
    const notificationDropdown = document.getElementById('notificationDropdown');
    
    if (notificationDropdown) {
        // Mark notifications as read when dropdown is opened
        notificationDropdown.addEventListener('shown.bs.dropdown', function() {
            markNotificationsAsRead();
        });
    }
    
    // Auto-refresh notifications every 30 seconds
    setInterval(refreshNotifications, 30000);
}

function markNotificationsAsRead() {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        // Fade out the badge
        badge.style.opacity = '0.5';
        
        // Make API call to mark as read
        fetch('/api/notifications/mark-read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                badge.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error marking notifications as read:', error);
            badge.style.opacity = '1'; // Restore if failed
        });
    }
}

function refreshNotifications() {
    fetch('/api/notifications/count')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-badge');
            if (badge && data.count !== undefined) {
                if (data.count > 0) {
                    badge.textContent = data.count;
                    badge.style.display = 'flex';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error refreshing notifications:', error);
        });
}

// Mobile Handling
function initMobileHandling() {
    // Close mobile navbar when clicking on a link
    const navbarCollapse = document.getElementById('navbarContent');
    if (!navbarCollapse) return;
    
    const navLinks = navbarCollapse.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                // Use Bootstrap's collapse method if available
                if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            }
        });
    });
    
    // Handle orientation change
    window.addEventListener('orientationchange', function() {
        setTimeout(function() {
            // Recalculate positions if needed
            const navbar = document.querySelector('.custom-navbar');
            if (navbar) {
                navbar.style.height = 'auto';
            }
        }, 100);
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create a toast notification
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                    data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to toast container or create one
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Show the toast if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    } else {
        // Fallback if Bootstrap is not available
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
}

// Export functions for use in other modules
if (typeof window !== 'undefined') {
    window.NavbarUtils = {
        showNotification
    };
}