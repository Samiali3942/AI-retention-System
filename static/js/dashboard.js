// Dashboard JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded successfully');
    
    // Initialize dashboard components
    initializeSearch();
    initializeNotifications();
    initializeCardInteractions();
    initializeStatsAnimations();
});

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchInput && searchBtn) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
        
        searchBtn.addEventListener('click', function() {
            performSearch(searchInput.value);
        });
    }
}

function performSearch(query) {
    if (query.trim() === '') {
        showNotification('Please enter a search term', 'warning');
        return;
    }
    
    console.log('Searching for:', query);
    // Simulate search functionality
    showNotification(`Searching for: ${query}`, 'info');
    
    // Here you would typically make an API call to search
    // fetch('/api/search', { method: 'POST', body: JSON.stringify({query}) })
}

// Notification system
function initializeNotifications() {
    const notificationIcon = document.querySelector('.notification-icon');
    
    if (notificationIcon) {
        notificationIcon.addEventListener('click', function() {
            toggleNotificationPanel();
        });
    }
}

function toggleNotificationPanel() {
    // Create or toggle notification panel
    let panel = document.querySelector('.notification-panel');
    
    if (panel) {
        panel.remove();
    } else {
        createNotificationPanel();
    }
}

function createNotificationPanel() {
    const panel = document.createElement('div');
    panel.className = 'notification-panel';
    panel.innerHTML = `
        <div class="notification-header">
            <h3>Notifications</h3>
            <button class="close-panel" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
        <div class="notification-list">
            <div class="notification-item">
                <i class="fas fa-exclamation-triangle text-orange"></i>
                <div>
                    <p><strong>High Risk Customer Alert</strong></p>
                    <p>89 customers identified as high churn risk</p>
                    <span class="time">5 minutes ago</span>
                </div>
            </div>
            <div class="notification-item">
                <i class="fas fa-check-circle text-green"></i>
                <div>
                    <p><strong>Model Update Complete</strong></p>
                    <p>AI recommendation model updated successfully</p>
                    <span class="time">1 hour ago</span>
                </div>
            </div>
            <div class="notification-item">
                <i class="fas fa-info-circle text-blue"></i>
                <div>
                    <p><strong>System Maintenance</strong></p>
                    <p>Scheduled maintenance tonight at 2:00 AM</p>
                    <span class="time">3 hours ago</span>
                </div>
            </div>
        </div>
    `;
    
    // Style the panel
    panel.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        width: 350px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 1001;
        max-height: 400px;
        overflow-y: auto;
    `;
    
    document.body.appendChild(panel);
    
    // Add styles for notification items
    const style = document.createElement('style');
    style.textContent = `
        .notification-panel .notification-header {
            padding: 1rem;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .notification-panel .close-panel {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #718096;
        }
        .notification-panel .notification-list {
            padding: 0.5rem;
        }
        .notification-panel .notification-item {
            display: flex;
            gap: 1rem;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            transition: background 0.3s ease;
        }
        .notification-panel .notification-item:hover {
            background: #f7fafc;
        }
        .notification-panel .notification-item i {
            font-size: 1.2rem;
            margin-top: 0.2rem;
        }
        .notification-panel .notification-item .time {
            font-size: 0.8rem;
            color: #a0aec0;
        }
        .text-orange { color: #ed8936; }
        .text-green { color: #48bb78; }
        .text-blue { color: #4299e1; }
    `;
    document.head.appendChild(style);
}

// Card interactions
function initializeCardInteractions() {
    const cards = document.querySelectorAll('.dashboard-card');
    
    cards.forEach((card, index) => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Add click tracking
        card.addEventListener('click', function() {
            const cardType = this.getAttribute('data-card');
            trackCardClick(cardType);
        });
    });
}

function trackCardClick(cardType) {
    console.log(`Card clicked: ${cardType}`);
    
    // Send analytics event
    if (typeof gtag !== 'undefined') {
        gtag('event', 'card_click', {
            'card_type': cardType,
            'timestamp': new Date().toISOString()
        });
    }
}

// Navigation function for feature buttons
function navigateToFeature(featureName) {
    console.log(`Navigating to: ${featureName}`);
    
    // Show loading state
    showLoadingState(featureName);
    
    // Simulate navigation delay
    setTimeout(() => {
        // Navigate to the specific feature page
        window.location.href = `/dashboard/${featureName}`;
    }, 500);
}

function showLoadingState(featureName) {
    const card = document.querySelector(`[data-card="${featureName}"]`);
    const button = card.querySelector('.card-button');
    
    if (button) {
        const originalContent = button.innerHTML;
        button.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            <span>Loading...</span>
        `;
        button.disabled = true;
        
        // Reset after delay
        setTimeout(() => {
            button.innerHTML = originalContent;
            button.disabled = false;
        }, 2000);
    }
}

// Stats animations
function initializeStatsAnimations() {
    const stats = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStatNumber(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    stats.forEach(stat => {
        observer.observe(stat);
    });
}

function animateStatNumber(element) {
    const finalValue = element.textContent;
    const isPercentage = finalValue.includes('%');
    const isCurrency = finalValue.includes('₹');
    const hasPlus = finalValue.includes('+');
    
    let numericValue = parseFloat(finalValue.replace(/[^\d.]/g, ''));
    
    if (isNaN(numericValue)) return;
    
    let currentValue = 0;
    const increment = numericValue / 50; // 50 steps for smooth animation
    const duration = 2000; // 2 seconds
    const stepTime = duration / 50;
    
    element.textContent = '0';
    
    const timer = setInterval(() => {
        currentValue += increment;
        
        if (currentValue >= numericValue) {
            currentValue = numericValue;
            clearInterval(timer);
        }
        
        let displayValue = Math.floor(currentValue);
        
        if (isCurrency) {
            if (finalValue.includes('M')) {
                displayValue = (currentValue / 1000000).toFixed(1) + 'M';
            } else if (finalValue.includes('K')) {
                displayValue = (currentValue / 1000).toFixed(1) + 'K';
            }
            element.textContent = '₹' + displayValue;
        } else if (isPercentage) {
            element.textContent = (hasPlus ? '+' : '') + currentValue.toFixed(1) + '%';
        } else if (finalValue.includes('s')) {
            element.textContent = currentValue.toFixed(1) + 's';
        } else if (finalValue.includes(',')) {
            element.textContent = displayValue.toLocaleString();
        } else {
            element.textContent = displayValue;
        }
    }, stepTime);
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1002;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 300px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-times-circle'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        'info': '#4299e1',
        'success': '#48bb78',
        'warning': '#ed8936',
        'error': '#e53e3e'
    };
    return colors[type] || colors.info;
}

// Add required CSS animations
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        opacity: 0.8;
        transition: opacity 0.3s ease;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
`;
document.head.appendChild(animationStyles);

// Mobile menu toggle
function toggleMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const searchContainer = document.querySelector('.search-container');
    
    if (window.innerWidth <= 768) {
        if (searchContainer.style.display === 'flex') {
            searchContainer.style.display = 'none';
        } else {
            searchContainer.style.display = 'flex';
            searchContainer.style.position = 'absolute';
            searchContainer.style.top = '100%';
            searchContainer.style.left = '0';
            searchContainer.style.right = '0';
            searchContainer.style.background = 'white';
            searchContainer.style.padding = '1rem';
            searchContainer.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        }
    }
}

// Add event listener for menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleMobileMenu);
    }
});

// Real-time data updates (simulated)
function startRealTimeUpdates() {
    setInterval(() => {
        updateDashboardStats();
    }, 30000); // Update every 30 seconds
}

function updateDashboardStats() {
    const stats = [
        { selector: '.dashboard-card[data-card="ai-recommendations"] .stat-number', 
          baseValue: 247, variance: 5 },
        { selector: '.dashboard-card[data-card="customer-segmentation"] .stat-number', 
          baseValue: 12, variance: 1 },
        { selector: '.dashboard-card[data-card="ekyc-issues"] .stat-number', 
          baseValue: 23, variance: 3 },
        { selector: '.dashboard-card[data-card="feedback-support"] .stat-number', 
          baseValue: 156, variance: 10 }
    ];
    
    stats.forEach(stat => {
        const element = document.querySelector(stat.selector);
        if (element) {
            const newValue = stat.baseValue + Math.floor(Math.random() * stat.variance * 2) - stat.variance;
            element.textContent = newValue;
            
            // Add a subtle flash effect
            element.style.color = '#48bb78';
            setTimeout(() => {
                element.style.color = '#667eea';
            }, 1000);
        }
    });
}

// Initialize real-time updates
setTimeout(startRealTimeUpdates, 5000); // Start after 5 seconds

// Export functions for use in other modules
window.dashboardFunctions = {
    navigateToFeature,
    showNotification,
    trackCardClick
};