import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";
import jsCookie from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm'
import zod from 'https://cdn.jsdelivr.net/npm/zod@3.23.8/+esm'

const send_button = document.getElementById('send-btn')
const connect_button = document.getElementById('connect-btn')
const disconnect_button = document.getElementById('disconnect-btn')

const received = document.getElementById('received')

const auth_cookies = jsCookie.get('Auth')

const messageSchema = zod.object({
    content: zod.string(),
    chat_id: zod.string().uuid(),
})

const socket = io("http://localhost:5000", {
    extraHeaders: {
        "Auth": auth_cookies
    }
});

send_button.addEventListener('click', () => {
    const content = document.getElementById('content').value
    const chat_id = document.getElementById('chat_id').value

    const message = {
        content,
        chat_id
    }

    try {
        messageSchema.parse(message)
        socket.send(message)
    }
    catch (err) {
        alert("Content must be a string and chat_id must be an valid UUID")
    }


})

connect_button.addEventListener('click', () => {
    socket.connect()
})

disconnect_button.addEventListener('click', () => {
    socket.disconnect()
})

socket.addEventListener('message', (message) => {
    received.value = message.content
})
