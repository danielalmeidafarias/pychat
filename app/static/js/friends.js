const search_btn = document.getElementById('search-btn')

const send_request_btn = document.getElementsByName('send_request_btn')

for (let element of send_request_btn) {

    const send_btn = document.getElementById(element.id)

    send_btn.addEventListener('click', async(e) => {
        e.preventDefault()

        await axios.post('http://localhost:5000/friendship_request', {
            'receiver_id': element.id
        }
        ).then(response => {
            window.location = window.location.href + `&sent=True`
        }).catch(err => {
            if(err.status == 401) {
                Unauthorized()
        } else if(err.status == 404){
                BaseResponse(err, 'question')
        } else {
                BaseResponse(err, 'warning')
        }
        })

    })
}

search_btn.addEventListener('click', (e) => {
    const name = document.getElementById('name').value

    e.preventDefault()
    if(name){
        document.location = `http://localhost:5000/friendship?name=${name}`
    }
})

const delete_request_btn = document.getElementsByName('delete_request_btn')
console.log(delete_request_btn)

for (let element of delete_request_btn) {
     const delete_btn = document.getElementById(element.id)

    delete_btn.addEventListener('click', async() => {
        await axios.delete(`http://localhost:5000/friendship_request/${element.id}`)
            .then(response => {
            window.location = window.location.href + `&deleted=True`
        }).catch(err => {
            if(err.status == 401) {
                Unauthorized()
        } else if(err.status == 404){
                BaseResponse(err, 'question')
        } else {
                BaseResponse(err, 'warning')
        }
        })
    })

}