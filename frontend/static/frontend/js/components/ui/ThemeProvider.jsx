// In a new file: src/components/ui/ThemeProvider.jsx
import React from 'react';

const ThemeProvider = ({ children }) => {
  // CSS variables for the theme
  React.useEffect(() => {
    document.documentElement.style.setProperty('--primary', '#28a745');
    document.documentElement.style.setProperty('--primary-dark', '#218838');
    document.documentElement.style.setProperty('--secondary', '#4a90e2');
    document.documentElement.style.setProperty('--accent', '#f5a623');
    document.documentElement.style.setProperty('--light', '#f8f9fa');
    document.documentElement.style.setProperty('--gray', '#e9ecef');
    document.documentElement.style.setProperty('--dark', '#6c757d');
    document.documentElement.style.setProperty('--font-main', '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif');
    document.documentElement.style.setProperty('--font-heading', '"Roboto", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif');
  }, []);

  return <>{children}</>;
};

export default ThemeProvider;