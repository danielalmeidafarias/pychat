const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const form = new FormData(document.getElementById('signup_form'))

    try {
        await axios.post('http://localhost:5000/user/create', form).then(async (err) => {
            window.location.reload()
        })
    } catch (err) {
        if (err.status == 409) {
            BaseResponse(err, "warning")
        } else if (err.status == 400) {
            DataValidationError(err)
        } else {
            BaseResponse(err, "warning")
        }
    }
}

const signup_btn = document.getElementById("signup_btn")

signup_btn.addEventListener('click', async (event) => {
    event.preventDefault()
    await signIn()
})

const togglePassword = document.getElementById('toggle-password-visibility');
const passwordInput = document.getElementById('password');

togglePassword.addEventListener('click', function () {
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        togglePassword.classList.remove('fa-eye');
        togglePassword.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = "password";
        togglePassword.classList.remove('fa-eye-slash');
        togglePassword.classList.add('fa-eye');
    }
});
