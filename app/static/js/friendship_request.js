const accept_btn = document.getElementsByName('accept-btn')
const refuse_btn = document.getElementsByName('refuse-btn')
const delete_btn = document.getElementsByName('delete-btn')

for (let element of accept_btn) {
    const btn = document.getElementById(element.id)

    btn.addEventListener('click', async (e) => {
        e.preventDefault()

        const request_id = element.id.substring(7)

        await axios.put(`http://localhost:5000/friendship_request/${request_id}`, {
            status: "accepted"
        }).then(() => {
            window.location.reload()
        }).catch(err => {
            console.log(err)
        })

    })
}

for (let element of [...refuse_btn, ...delete_btn]) {
    element.addEventListener('click', async (e) => {
        e.preventDefault()

        const request_id = element.id.substring(7)
        console.log(request_id)

        await axios.delete(`http://localhost:5000/friendship_request/${request_id}`)
            .then(response => {
                window.location = window.location.href + '?canceled=true'
            }).catch(err => {
                if (err.status == 401) {
                    Unauthorized()
                } else if (err.status == 404) {
                    BaseResponse(err, 'question')
                } else {
                    BaseResponse(err, 'warning')
                }
            })
    })
}

// for (let element of delete_btn) {
//
//     const delete_btn = document.getElementById(element.id)
//
//     delete_btn.addEventListener('click', async (e) => {
//         e.preventDefault()
//
//         const request_id = element.id.substring(7)
//         console.log(request_id)
//
//         await axios.delete(`http://localhost:5000/friendship_request/${request_id}`)
//             .then(response => {
//                 window.location = window.location.href + `&deleted=True`
//             }).catch(err => {
//                 if (err.status == 401) {
//                     Unauthorized()
//                 } else if (err.status == 404) {
//                     BaseResponse(err, 'question')
//                 } else {
//                     BaseResponse(err, 'warning')
//                 }
//             })
//     })
//
// }
