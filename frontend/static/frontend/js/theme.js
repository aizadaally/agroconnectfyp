// frontend/static/frontend/js/theme.js

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Theme script loaded');
    
    // Get saved theme or use light as default
    let currentTheme = localStorage.getItem('agroconnect-theme') || 'light';
    
    // Function to apply theme
    function applyTheme(theme) {
        console.log('Applying theme:', theme);
        
        // Remove old theme attribute
        document.documentElement.removeAttribute('data-theme');
        
        // Set new theme
        document.documentElement.setAttribute('data-theme', theme);
        
        // Save to localStorage
        localStorage.setItem('agroconnect-theme', theme);
        
        // Update icon
        updateIcon(theme);
        
        // Force a style recalculation
        document.body.style.display = 'none';
        document.body.offsetHeight; // Trigger reflow
        document.body.style.display = '';
        
        console.log('Theme applied, current data-theme:', document.documentElement.getAttribute('data-theme'));
    }
    
    // Function to update the icon
    function updateIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }
    }
    
    // Create theme toggle button
    function createThemeToggle() {
        const themeToggle = document.createElement('li');
        themeToggle.className = 'nav-item';
        themeToggle.innerHTML = `
            <button class="nav-link theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                <i class="bi bi-sun-fill" id="theme-icon"></i>
            </button>
        `;
        
        // Find the right navbar
        const navbar = document.querySelector('.navbar-nav:last-child');
        const languageDropdown = navbar ? navbar.querySelector('#languageDropdown') : null;
        
        if (navbar && languageDropdown) {
            languageDropdown.closest('li').insertAdjacentElement('beforebegin', themeToggle);
        } else if (navbar) {
            navbar.insertBefore(themeToggle, navbar.firstChild);
        }
        
        // Add click event
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Toggle theme
                currentTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                console.log('Toggling to:', currentTheme);
                
                // Apply new theme
                applyTheme(currentTheme);
            });
        }
    }
    
    // Initialize
    
    createThemeToggle();
    applyTheme(currentTheme);
    
    // Add debug info
    console.log('Theme initialization complete');
    console.log('Current theme:', currentTheme);
    console.log('Data theme attribute:', document.documentElement.getAttribute('data-theme'));
});

// Remove preload class when page is loaded
window.addEventListener('load', function() {
    document.documentElement.classList.remove('preload');
    document.body.classList.remove('preload');
});

// Debug function
window.debugTheme = function() {
    console.log('=== Theme Debug ===');
    console.log('localStorage theme:', localStorage.getItem('agroconnect-theme'));
    console.log('data-theme attribute:', document.documentElement.getAttribute('data-theme'));
    console.log('Body background color:', window.getComputedStyle(document.body).backgroundColor);
    console.log('Body text color:', window.getComputedStyle(document.body).color);
};