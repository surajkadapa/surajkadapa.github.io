document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const input = userInput.value.trim().toLowerCase();
            // Add functionality for user input, e.g., navigating to posts, searching, etc.
            if (input === 'blog') {
                alert('You typed "blog"'); // Replace this with actual functionality
            } else {
                alert('Command not recognized');
            }
        }
    });
});
