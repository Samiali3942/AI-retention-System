// static/js/sidebar.js

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const body = document.body;

    // Function to open sidebar
    function openSidebar() {
        if (sidebar) {
            sidebar.classList.add('show');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.add('show');
        }
        body.classList.add('sidebar-open');
        
        // Set focus to close button for accessibility
        if (sidebarClose) {
            setTimeout(() => sidebarClose.focus(), 100);
        }
    }

    // Function to close sidebar
    function closeSidebar() {
        if (sidebar) {
            sidebar.classList.remove('show');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('show');
        }
        body.classList.remove('sidebar-open');
        
        // Return focus to toggle button
        if (sidebarToggle) {
            sidebarToggle.focus();
        }
    }

    // Function to toggle sidebar
    function toggleSidebar() {
        if (sidebar && sidebar.classList.contains('show')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    // Event Listeners
    
    // Toggle sidebar on navbar button click
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleSidebar();
        });
    }

    // Close sidebar on close button click
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeSidebar();
        });
    }

    // Close sidebar on overlay click
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function(e) {
            if (e.target === sidebarOverlay) {
                closeSidebar();
            }
        });
    }

    // Close sidebar on ESC key press
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });

    // Handle navigation links
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    // Set active navigation based on current page
    function setActiveNavigation() {
        const currentPath = window.location.pathname;
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // Check if the link href matches current path
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
        
        // Fallback: if no exact match, check for partial matches
        if (!document.querySelector('.sidebar .nav-link.active')) {
            navLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && href !== '#' && currentPath.includes(href)) {
                    link.classList.add('active');
                }
            });
        }
    }

    // Navigation link click handler
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only prevent default for # links (demo purposes)
            if (href === '#') {
                e.preventDefault();
                
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                
                // Add active class to clicked link
                this.classList.add('active');
                
                // Get page data attribute for demo
                const page = this.getAttribute('data-page');
                console.log('Demo navigation to:', page);
            }
            
            // Close sidebar on mobile after navigation
            if (window.innerWidth <= 768) {
                setTimeout(closeSidebar, 150);
            }
        });
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        // Close sidebar on larger screens if needed
        if (window.innerWidth > 768 && sidebar && sidebar.classList.contains('show')) {
            // You can choose to keep it open or close it
            // closeSidebar();
        }
    });

    // Prevent sidebar from closing when clicking inside it
    if (sidebar) {
        sidebar.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Handle smooth scrolling within sidebar if content overflows
    if (sidebar) {
        sidebar.addEventListener('scroll', function() {
            // Add scroll-based effects here if needed
            const scrollTop = this.scrollTop;
            const header = this.querySelector('.sidebar-header');
            
            if (header) {
                if (scrollTop > 20) {
                    header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
                } else {
                    header.style.boxShadow = 'none';
                }
            }
        });
    }

    // Initialize active navigation on page load
    setActiveNavigation();

    // Handle browser back/forward navigation
    window.addEventListener('popstate', function() {
        setActiveNavigation();
    });

    // Add loading state for navigation links
    function addNavigationLoadingState() {
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                const href = this.getAttribute('href');
                
                if (href && href !== '#' && !href.startsWith('javascript:')) {
                    // Add loading state
                    const icon = this.querySelector('i');
                    if (icon) {
                        const originalClass = icon.className;
                        icon.className = 'fas fa-spinner fa-spin';
                        
                        // Restore original icon after a delay (in case navigation is slow)
                        setTimeout(() => {
                            icon.className = originalClass;
                        }, 2000);
                    }
                }
            });
        });
    }

    // Initialize loading states
    addNavigationLoadingState();

    // Expose functions globally for external use
    window.sidebarControls = {
        open: openSidebar,
        close: closeSidebar,
        toggle: toggleSidebar,
        setActive: setActiveNavigation
    };
});