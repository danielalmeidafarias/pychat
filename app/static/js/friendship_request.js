const accept_btn = document.getElementsByName('accept-btn')
const refuse_btn = document.getElementsByName('refuse-btn')
const delete_btn = document.getElementsByName('delete-btn')

console.log(accept_btn)

for (let element of accept_btn) {
    const btn = document.getElementById(element.id)

    btn.addEventListener('click', async(e) => {
        e.preventDefault()

        const request_id = element.id.substring(7)
        console.log(request_id)

        await axios.put(`http://localhost:5000/friendship_request/${request_id}`, {
            status: "accepted"
        }).then(() => {
            window.location.reload()
        }).catch(err => {
            console.log(err)
        })

    })
}

for (let element of refuse_btn) {
    const btn = document.getElementById(element.id)

    btn.addEventListener('click', async(e) => {
        e.preventDefault()

        const request_id = element.id.substring(7)
        console.log(request_id)

        await axios.put(`http://localhost:5000/friendship_request/${request_id}`, {
            status: "refused"
        }).then(() => {
            window.location.reload()
        }).catch(err => {
            console.log(err)
        })

    })
}

