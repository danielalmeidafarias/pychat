import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";
import jsCookie from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm'
import zod from 'https://cdn.jsdelivr.net/npm/zod@3.23.8/+esm'

const send_button = document.getElementById('send-btn')
const connect_button = document.getElementById('connect-btn')
const disconnect_button = document.getElementById('disconnect-btn')

const received = document.getElementById('received')

const auth_cookies = jsCookie.get('Auth')

const socket = io("http://localhost:5000", {
    autoConnect: false,
    extraHeaders: {
        "Auth": auth_cookies
    }
});

send_button.addEventListener('click', () => {
    const content = document.getElementById('content').value
    const chat_id = document.getElementById('chat_id').value

    const json = {
        content,
        chat_id
    }

    socket.send(json)
})

connect_button.addEventListener('click', () => {
    socket.connect()
})

disconnect_button.addEventListener('click', () => {
    socket.disconnect()
})

socket.addEventListener('message', (message) => {
    received.value = message
})
