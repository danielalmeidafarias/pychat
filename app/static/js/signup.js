const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const form = new FormData(document.getElementById('signup_form'))

    try {
        // await axios.post('http://localhost:5000/user/create', {
        //     email,
        //     password,
        //     name
        // }).then(async (err) => {
        //     window.location.reload()
        // })
        await axios.post('http://localhost:5000/user/create', form).then(async (err) => {
            window.location.reload()
        })
    } catch (err) {
        if(err.status == 409) {
            BaseResponse(err, "warning")
        } else if(err.status == 400) {
            DataValidationError(err)
        } else {
            BaseResponse(err, "warning")
        }
    }
}

const signup_btn = document.getElementById("signup_btn")

signup_btn.addEventListener('click', async(event) => {
    event.preventDefault()
    await signIn()
})
