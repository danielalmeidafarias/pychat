let params = new URLSearchParams(document.location.search)

if (params.get('expired_session') == 'true') {
        ExpiredAccessToken()
} else if(params.get('unauthorized') == 'true') {
        Unauthorized()
}

const signIn = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    await axios.post('http://localhost:5000/auth/signin', {
        email,
        password
    }).then(async (data) => {
        window.location.reload()
    }).catch(async (err) => {
        if(err.status == 401) {
            BaseResponse(err, 'error')
        } else if(err.status == 404){
            BaseResponse(err, 'question')
        } else {
            BaseResponse(err, 'warning')
        }
    });
};

const login_btn = document.getElementById("login_btn");

login_btn.addEventListener('click', async(event) => {
    event.preventDefault();
    await signIn();
});
