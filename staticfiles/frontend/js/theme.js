// frontend/static/frontend/js/theme.js

// Initialize theme handling
(function() {
    // Get saved theme or use light as default
    const getSavedTheme = () => localStorage.getItem('agroconnect-theme') || 'light';
    
    // Apply theme to document
    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('agroconnect-theme', theme);
        updateThemeIcon(theme);
        console.log('Theme applied:', theme);
    };
    
    // Update theme icon
    const updateThemeIcon = (theme) => {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }
    };
    
    // Create theme toggle button in navbar
    const createThemeToggle = () => {
        const navbar = document.querySelector('.navbar-nav:last-child');
        if (!navbar) return;
        
        // Create the toggle button
        const themeToggle = document.createElement('li');
        themeToggle.className = 'nav-item';
        themeToggle.innerHTML = `
            <button class="nav-link theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                <i class="bi bi-moon-fill" id="theme-icon"></i>
            </button>
        `;
        
        // Insert before language dropdown
        const languageDropdown = navbar.querySelector('[data-bs-toggle="dropdown"]')?.parentElement;
        if (languageDropdown) {
            navbar.insertBefore(themeToggle, languageDropdown);
        } else {
            navbar.appendChild(themeToggle);
        }
        
        // Add click event
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', toggleTheme);
        }
    };
    
    // Toggle theme function
    const toggleTheme = () => {
        const currentTheme = getSavedTheme();
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
    };
    
    // Initialize on DOM ready
    const init = () => {
        const savedTheme = getSavedTheme();
        applyTheme(savedTheme);
        createThemeToggle();
    };
    
    // Apply theme immediately to prevent flash
    const immediateTheme = getSavedTheme();
    document.documentElement.setAttribute('data-theme', immediateTheme);
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Remove preload class after initialization
    window.addEventListener('load', () => {
        document.documentElement.classList.remove('preload');
        document.body.classList.remove('preload');
    });
})();

// Global debug function
window.debugTheme = function() {
    console.log('=== Theme Debug ===');
    console.log('localStorage theme:', localStorage.getItem('agroconnect-theme'));
    console.log('data-theme attribute:', document.documentElement.getAttribute('data-theme'));
    console.log('Body background color:', window.getComputedStyle(document.body).backgroundColor);
    console.log('Body text color:', window.getComputedStyle(document.body).color);
};