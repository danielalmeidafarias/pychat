const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    try {
        const response = await axios.post('http://localhost:5000/user', {
            email,
            password,
            name
        })
    } catch (err) {
        Swal.fire({
            title: 'Error!',
            text: 'Do you want to continue',
            icon: 'error',
            confirmButtonText: 'Cool'
        })
        console.log(err)
    }
}

const signup_btn = document.getElementById("signup_btn")

signup_btn.addEventListener('click', async() => await signIn())
