const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    try {
        const response = await axios.post('http://localhost:5000/user/create', {
            email,
            password,
            name
        }).then((data) => {
            // console.log(data)
            window.location.reload()
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

signup_btn.addEventListener('click', async(event) => {
    event.preventDefault()
    await signIn()
})
