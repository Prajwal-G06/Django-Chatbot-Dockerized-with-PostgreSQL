async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    const chatBox = document.getElementById("chat-box");

    // Display user message
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    document.getElementById("user-input").value = "";  // Clear input field

    // Send the request to the Django server
    const response = await fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    });

    const data = await response.json();
    chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${data.response}</p>`;

    // Scroll chat to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
