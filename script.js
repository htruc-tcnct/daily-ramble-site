const messages = [
    "Keep calm and carry on... nhưng mà hơi khó à nha!",
    "Think positive! Today is gonna be amazing... hopefully!",
    "Remember to drink water... and maybe call your mom?",
    "Feeling down? Just dance it out... or maybe just scroll tiếp.",
    "You clicked the button! So brave! What happens next? Ai biết!",
    "Loading... please wait... or don't, I'm not your boss... but maybe wait?",
    "Error 404: Sanity not found... kidding! Try again đi bro!"
];

const dynamicMessageElement = document.getElementById('dynamic-message');
const actionButton = document.getElementById('action-button');

function getRandomMessage() {
    return messages[Math.floor(Math.random() * messages.length)];
}

// Set initial message
dynamicMessageElement.textContent = getRandomMessage();
// Add fade-in animation class dynamically if needed, or handle via CSS load

actionButton.addEventListener('click', () => {
    dynamicMessageElement.style.opacity = 0; // Start fade out
    setTimeout(() => {
        dynamicMessageElement.textContent = getRandomMessage();
        dynamicMessageElement.style.opacity = 1; // Start fade in
    }, 300); // Match transition duration
});

// You could add more complex logic, fetch data from './data/', etc.