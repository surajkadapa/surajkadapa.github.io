document.addEventListener("DOMContentLoaded", function() {
    const commandLine = document.getElementById('command-line');

    // Auto-focus on the input when the page loads
    commandLine.focus();

    // Handle terminal input and redirect
    commandLine.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const value = e.target.value.trim().toLowerCase();
            if (value.includes('blog')) {
                window.location.href = 'blog.html';
            } else if (value.includes('back')) {
                window.location.href = '/';
            } else if (value.includes('contact')) {
                window.location.href = 'contact.html';
            } else {
                alert('Unknown command: ' + value);
            }
        }
    });
});
