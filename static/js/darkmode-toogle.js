/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2023 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
    'use strict'
  
    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)
  
    const getPreferredTheme = () => {
      const storedTheme = getStoredTheme()
      if (storedTheme) {
        return storedTheme
      }
  
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  
    const setTheme = theme => {
      const themeToggle = document.querySelector('.chk');
      const rootElement = document.documentElement;  // o document.body
  
      if (theme === 'dark') {
          rootElement.setAttribute('data-bs-theme', 'dark');
          rootElement.classList.add('dark-theme');
          rootElement.classList.remove('light-theme');
          themeToggle.checked = true;
      } else {
          rootElement.setAttribute('data-bs-theme', 'light');
          rootElement.classList.add('light-theme');
          rootElement.classList.remove('dark-theme');
          themeToggle.checked = false;
      }
  }
  
  
  
    setTheme(getPreferredTheme())
  

  
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = getStoredTheme()
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
      }
    })


    document.querySelector('.chk').addEventListener('change', function() {
      if (this.checked) {
          setStoredTheme('dark');
          setTheme('dark');
      } else {
          setStoredTheme('light');
          setTheme('light');
      }
  });
  
  })()