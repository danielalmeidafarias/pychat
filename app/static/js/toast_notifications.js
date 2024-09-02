const Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      iconColor: 'white',
      customClass: {
        popup: 'colored-toast',
      },
      showConfirmButton: false,
      timerProgressBar: true,
      timer: 3000,
      showCloseButton: true
})

const DataValidationError = async (response) => {
    let errors = ''
    let error_counter = 0
    for (let error in response.response.data.errors){
        errors = errors + `\n ${error_counter = error_counter + 1}. ${err.response.data.errors[error]}`
    }
    await Toast.fire({
        icon: 'warning',
        title: err.response.data.message,
        text: errors
    })
}

const ExpiredAccessToken = async () => {
    await Toast.fire({
        icon: 'error',
        title: 'Expired Session',
    })
}

const Unauthorized = async () => {
    await Toast.fire({
        icon: 'error',
        title: 'Unauthorized!',
    })
}

const SuccessfulLogin = async () => {
    await Toast.fire({
        icon: 'success',
        title: 'Successful login!',
    })
}

const BaseResponse = async(response, icon) => {
    await Toast.fire({
        icon: icon,
        title: response.response.data.message
    })
}

