const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log(document.cookie)

    await axios.post('http://localhost:5000/auth/signin', {
        email,
        password
    }).then((data) => {
        window.location.reload()
    }).catch((err) => {
        Swal.fire({
            title: 'Error!',
            text: 'Do you want to continue',
            icon: 'error',
            confirmButtonText: 'Cool'
        });
    });
};

const login_btn = document.getElementById("login_btn");

login_btn.addEventListener('click', async(event) => {
    event.preventDefault();
    await signIn();
});
