// Get the chatbox and user input elements
const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('user-input');

// Function to add a message to the chatbox
function addMessage(message, sender) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', sender);
  messageElement.innerText = message;
  chatbox.appendChild(messageElement);
}

// Function to handle user input
function handleUserInput(event) {
  event.preventDefault();
  const userMessage = userInput.value;
  addMessage(userMessage, 'user');
  userInput.value = '';

  // Send the user message to the server for processing
  fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: userMessage
    })
  })
    .then(response => response.json())
    .then(data => {
      const assistantMessage = data.message;
      addMessage(assistantMessage, 'assistant');
      chatbox.scrollTop = chatbox.scrollHeight;
    });
}

// Event listener for the user input form submission
document.getElementById('user-form').addEventListener('submit', handleUserInput);
