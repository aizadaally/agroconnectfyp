// Add this to your main.js file or create a new theme.js file

// Theme management
class ThemeManager {
    constructor() {
        this.themeKey = 'agroconnect-theme';
        this.init();
    }

    init() {
        // Check for saved theme preference or default to light
        const savedTheme = localStorage.getItem(this.themeKey) || 'light';
        this.setTheme(savedTheme);
        
        // Create theme toggle button
        this.createThemeToggle();
        
        // Listen for system preference changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!localStorage.getItem(this.themeKey)) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    createThemeToggle() {
        // Add theme toggle to navbar
        const navbar = document.querySelector('.navbar-nav');
        if (navbar) {
            const themeToggle = document.createElement('li');
            themeToggle.className = 'nav-item';
            themeToggle.innerHTML = `
                <button class="nav-link theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                    <i class="bi bi-sun-fill" id="theme-icon"></i>
                </button>
            `;
            
            // Insert before language selector
            const languageDropdown = navbar.querySelector('#languageDropdown');
            if (languageDropdown) {
                languageDropdown.closest('li').insertAdjacentElement('beforebegin', themeToggle);
            } else {
                navbar.insertBefore(themeToggle, navbar.firstChild);
            }
            
            // Add click handler
            const toggleButton = document.getElementById('theme-toggle');
            toggleButton.addEventListener('click', () => this.toggleTheme());
            
            // Set initial icon
            this.updateIcon();
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(this.themeKey, theme);
        this.updateIcon();
        
        // Update Bootstrap classes for theme
        if (theme === 'dark') {
            document.body.classList.add('bg-dark', 'text-light');
        } else {
            document.body.classList.remove('bg-dark', 'text-light');
        }
    }

    updateIcon() {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            const theme = document.documentElement.getAttribute('data-theme') || 'light';
            icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }
    }
}

// Initialize theme manager
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
});


// Create this as frontend/static/frontend/js/theme.js

// Theme management for dark/light mode
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.createElement('li');
    themeToggle.className = 'nav-item';
    themeToggle.innerHTML = `
        <button class="nav-link theme-toggle" id="theme-toggle" aria-label="Toggle theme">
            <i class="bi bi-sun-fill" id="theme-icon"></i>
        </button>
    `;
    
    // Insert theme toggle before language dropdown
    const navbar = document.querySelector('.navbar-nav');
    const languageDropdown = document.querySelector('#languageDropdown');
    if (languageDropdown && navbar) {
        languageDropdown.closest('li').insertAdjacentElement('beforebegin', themeToggle);
    }
    
    // Theme management
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Update icon based on current theme
    updateThemeIcon(currentTheme);
    
    // Toggle theme
    document.getElementById('theme-toggle').addEventListener('click', function() {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Add transition effect
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    });
    
    function updateThemeIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }
    }
    
    // Auto-detect system preference
    if (window.matchMedia && !localStorage.getItem('theme')) {
        const darkMode = window.matchMedia('(prefers-color-scheme: dark)');
        
        darkMode.addListener((e) => {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            updateThemeIcon(newTheme);
        });
        
        if (darkMode.matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
            updateThemeIcon('dark');
        }
    }
});

// Add smooth transitions for theme changes
const style = document.createElement('style');
style.innerHTML = `
    * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
    }
    
    .theme-toggle {
        padding: 0.5rem 0.75rem;
        border: none;
        background: none;
        color: inherit;
    }
    
    .theme-toggle:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .theme-toggle:focus {
        outline: none;
        box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
    }
`;
document.head.appendChild(style);