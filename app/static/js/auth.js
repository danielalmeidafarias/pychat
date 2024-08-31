import jsCookie from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';


const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
        try {
            await axios.post('http://localhost:5000/auth', {
                email,
                password
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
        finally {
            const authCookies = jsCookie.get('Auth');
            await axios.get('http://localhost:5000/auth', {
                headers: {
                    'Auth': authCookies
                }
            })
        }
}

const login_btn = document.getElementById("login_btn")

login_btn.addEventListener('click', async(event) => {
    event.preventDefault()
    await signIn()
})
