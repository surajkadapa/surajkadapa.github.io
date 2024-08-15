document.addEventListener('DOMContentLoaded', function () {
    const bootSequence = document.getElementById('boot-sequence');
    const terminalBox = document.getElementById('terminal-box');
    const userInput = document.getElementById('user-input');

    // Simulate boot sequence
    setTimeout(() => document.getElementById('boot-line-2').style.display = 'block', 1000);
    setTimeout(() => document.getElementById('boot-line-3').style.display = 'block', 2000);
    setTimeout(() => document.getElementById('boot-line-4').style.display = 'block', 3000);
    setTimeout(() => {
        bootSequence.style.display = 'none';
        terminalBox.style.display = 'block';
    }, 4000);

    userInput.focus()

    // Handle user input
    userInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            const value = e.target.value.trim().toLowerCase();
            if (value.includes('blog')) {
                window.location.href = 'blog.html';
            } else if (value.includes('about')) {
                window.location.href = 'about/index.html';
            } else if (value.includes('contact')) {
                window.location.href = 'contact.html';
            } else {
                alert('Unknown command: ' + value);
            }
        }
    });
});
