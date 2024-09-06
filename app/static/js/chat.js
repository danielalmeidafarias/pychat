import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";

document.addEventListener("DOMContentLoaded", () => {
    let chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
});

function deleteAllCookies() {
    document.cookie.split(';').forEach(cookie => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    });
}

const socket = io("http://localhost:5000");

let params = new URLSearchParams(document.location.search)

if (params.get('success_login') == 'true') {
    SuccessfullLogin()
}

const chatMessages = document.getElementById('chat-messages');

const createSendingMessageDOM = (message) => {
    const messageList = document.getElementById('message-list');

    const newMessage = document.createElement('li');
    newMessage.classList.add('mb-2', 'd-flex', 'justify-content-start');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('bg-light-gray', 'text-dark-green', 'p-2', 'rounded');
    messageDiv.textContent = message.content;

    newMessage.appendChild(messageDiv);

    messageList.appendChild(newMessage);

    chatMessages.scrollTop = chatMessages.scrollHeight;
};

const createReceivedMessageDOM = (message) => {
    const messageList = document.getElementById('message-list');

    const newMessage = document.createElement('li');
    newMessage.classList.add('mb-2', 'd-flex', 'justify-content-end');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('bg-dark-green', 'text-white', 'p-2', 'rounded');

    const userNameStrong = document.createElement('strong');
    userNameStrong.textContent = message.user_name + ": " 

    messageDiv.appendChild(userNameStrong);

    const messageContent = document.createTextNode(`${message.content}`);
    messageDiv.appendChild(messageContent);

    newMessage.appendChild(messageDiv);

    messageList.appendChild(newMessage);

    chatMessages.scrollTop = chatMessages.scrollHeight;
};

const sendButton = document.getElementById('send-btn');

sendButton.addEventListener('click', () => {
    const content = document.getElementById('content').value.trim();
    const params = new URLSearchParams(window.location.search);
    const chatId = params.get("id");

    const message = {
        content,
        chat_id: chatId
    };

    socket.send(message);

    createSendingMessageDOM(message)

    document.getElementById('content').value = '';

});

document.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      document.getElementById("send-btn").click();
    }
});

socket.on('message', (message) => {
    createReceivedMessageDOM({
        content: message.content,
        user_name: message.user_name
    })

    chatMessages.scrollTop = chatMessages.scrollHeight;
});

socket.on('disconnect', () => {
    Swal.fire({
  title: "Connection Error",
  text: "Do you want to reload?",
  icon: "warning",
  showCancelButton: true,
  confirmButtonColor: "#3085d6",
  cancelButtonColor: "#d33",
  confirmButtonText: "Reload"
}).then((result) => {
  if (result.isConfirmed) {
    window.location.reload()
  }
});
})
