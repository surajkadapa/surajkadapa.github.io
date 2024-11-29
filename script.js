// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const menuToggle = document.querySelector('.mobile-menu-toggle'); // Changed to querySelector
    const navLinks = document.querySelector('.nav-links'); // Changed to querySelector
    const themeToggle = document.getElementById('themeToggle');
    const themeText = document.getElementById('themeText');
    const contactForm = document.getElementById('contactForm');

    // Set initial theme
    let currentTheme = 'dark';
    document.documentElement.setAttribute('data-theme', 'dark');
    updateThemeUI(currentTheme);

    // Mobile Menu Functionality
    
    if (menuToggle && navLinks) {
        console.log('Menu elements found:', { menuToggle, navLinks });
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
                navLinks.classList.remove('active');
            }
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // Theme Toggle Functionality
    if (themeToggle && themeText) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    function toggleTheme() {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateThemeUI(currentTheme);
    }

    function updateThemeUI(theme) {
        if (themeText) {
            themeText.textContent = theme === 'light' ? 'Light' : 'Dark';
        }
    }

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 70,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Intersection Observer for Fade Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.section, .card').forEach(section => {
        observer.observe(section);
    });

    // Contact Form Handling
    if (contactForm) {
        // Form submission
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isValid = true;
            const formInputs = this.querySelectorAll('input, textarea');
            
            formInputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                const formData = new FormData(this);
                console.log('Form submitted:', Object.fromEntries(formData));
                
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message fade-in';
                successMessage.textContent = 'Message sent successfully!';
                this.appendChild(successMessage);
                
                // Reset form
                this.reset();
                this.querySelectorAll('.form-group').forEach(group => {
                    group.classList.remove('success');
                });
                
                // Remove success message after 3 seconds
                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            }
        });

        // Real-time form validation
        contactForm.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('blur', () => {
                validateInput(input);
            });
            
            input.addEventListener('input', () => {
                if (input.parentElement.classList.contains('error')) {
                    validateInput(input);
                }
            });
        });
    }
});

// Form Validation Helper Functions
function validateInput(input) {
    const value = input.value.trim();
    
    if (value === '') {
        showError(input, `${input.getAttribute('name')} is required`);
        return false;
    }
    
    if (input.type === 'email' && !validateEmail(value)) {
        showError(input, 'Please enter a valid email address');
        return false;
    }
    
    showSuccess(input);
    return true;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}

function showError(input, message) {
    const formGroup = input.parentElement;
    formGroup.classList.remove('success');
    formGroup.classList.add('error');
    
    let errorMessage = formGroup.querySelector('.error-message');
    if (!errorMessage) {
        errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        formGroup.appendChild(errorMessage);
    }
    errorMessage.textContent = message;
}

function showSuccess(input) {
    const formGroup = input.parentElement;
    formGroup.classList.remove('error');
    formGroup.classList.add('success');
    
    const errorMessage = formGroup.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}