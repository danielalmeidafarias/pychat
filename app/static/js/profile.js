// Taking inputs and it's original values
const name = document.getElementById('name')
const nameOriginalValue = name.value

const email = document.getElementById('email')
const emailOriginalValue = email.value

const password = document.getElementById('password')

const picture = document.getElementById('picture')
const profilePicture = document.getElementById('profile-picture')
const originalPictureSrc = profilePicture.src

// Buttons
const editNameBtn = document.getElementById('edit-name')
const editEmailBtn = document.getElementById('edit-email')
const editPasswordBtn = document.getElementById('edit-password')
const editPictureBtn = document.getElementById('edit-picture')
const editPictureIcon = document.getElementById('edit-picture-icon')

const saveChangesBtn = document.getElementById('save-changes-btn')
const deleteAccountBtn = document.getElementById('delete-account-btn')

const passwordEyeIcon = document.getElementById('password-eye-icon')

const form = new FormData()

// Edit/Cancel btn logic
// Turn the input disabled or enabled
// Change button styles
// When canceled, clean the form value
editNameBtn.addEventListener('click', () => {
    if (name.classList.contains('readonly-input')) {
        name.classList.remove('readonly-input')
        name.classList.add('focus-readonly-input')
        name.removeAttribute('readonly')

        editNameBtn.classList.remove('bg-light-green')
        editNameBtn.classList.add('bg-light-red')
        editNameBtn.innerText = 'cancel'
    } else {
        name.classList.remove('focus-readonly-input')
        name.classList.add('readonly-input')
        name.setAttribute('readonly', true)

        name.value = nameOriginalValue

        editNameBtn.classList.add('bg-light-green')
        editNameBtn.classList.add('bg-light-green')
        editNameBtn.classList.remove('bg-light-red')
        editNameBtn.innerText = 'edit'

        form.delete('name')
    }
})

editEmailBtn.addEventListener('click', () => {
    if (email.classList.contains('readonly-input')) {
        email.classList.remove('readonly-input')
        email.classList.add('focus-readonly-input')
        email.removeAttribute('readonly')

        editEmailBtn.classList.remove('bg-light-green')
        editEmailBtn.classList.add('bg-light-red')
        editEmailBtn.innerText = 'cancel'

    } else {
        email.classList.remove('focus-readonly-input')
        email.classList.add('readonly-input')
        email.setAttribute('readonly', true)

        email.value = emailOriginalValue

        editEmailBtn.classList.add('bg-light-green')
        editEmailBtn.classList.remove('bg-light-red')
        editEmailBtn.innerText = 'edit'

        form.delete('email')
    }
})

editPasswordBtn.addEventListener('click', () => {
    if (password.classList.contains('readonly-input')) {
        password.classList.remove('readonly-input')
        password.classList.add('focus-readonly-input')
        password.removeAttribute('readonly')
        password.setAttribute('value', '')

        editPasswordBtn.classList.remove('bg-light-green')
        editPasswordBtn.classList.add('bg-light-red')
        editPasswordBtn.innerText = 'cancel'
    } else {
        password.classList.remove('focus-readonly-input')
        password.classList.add('readonly-input')
        password.setAttribute('readonly', true)

        editPasswordBtn.classList.add('bg-light-green')
        editPasswordBtn.classList.remove('bg-light-red')
        editPasswordBtn.innerText = 'edit'

        form.delete('password')
    }
})

editPictureIcon.addEventListener('click', (e) => {
    e.preventDefault()
    if (editPictureIcon.classList.contains('fa-trash-alt')) {
        profilePicture.src = originalPictureSrc

        editPictureBtn.setAttribute('for', 'picture')

        editPictureIcon.classList.add('fa-pencil-alt')
        editPictureIcon.classList.remove('fa-trash-alt')

        form.delete('picture')
    }
})

// Changing form values
picture.addEventListener('change', (e) => {
    e.preventDefault()
    const [ file ] = picture.files
    if (file) {
        profilePicture.src = URL.createObjectURL(file)

        form.append('picture', file)

        editPictureBtn.removeAttribute('for')

        editPictureIcon.classList.remove('fa-pencil-alt')
        editPictureIcon.classList.add('fa-trash-alt')
    }
})

name.addEventListener('input', (e) => {
    form.delete('name')
    form.append('name', name.value)
})

email.addEventListener('input', (e) => {
    form.delete('email')
    form.append('email', email.value)
})

password.addEventListener('input', (e) => {
    form.delete('password')
    form.append('password', password.value)
})

passwordEyeIcon.addEventListener('click', () => {
    if (password.type == 'password') {
        password.setAttribute('type', 'text')
        passwordEyeIcon.classList.remove('fa-eye');
        passwordEyeIcon.classList.add('fa-eye-slash');
    } else {
        password.setAttribute('type', 'password')
        passwordEyeIcon.classList.remove('fa-eye-slash');
        passwordEyeIcon.classList.add('fa-eye');
    }
})

// Saving changes
saveChangesBtn.addEventListener('click', async (e) => {
    e.preventDefault()
    try {
        await axios.put('http://localhost:5000/user/profile', form)
        window.location.reload()
    } catch (err) {
        console.log(err)
    }
})

// Delete account
deleteAccountBtn.addEventListener('click', async () => {
    try {
        await axios.delete('http://localhost:5000/user/profile')
        window.location.reload()
    } catch (err) {
        console.log(err)
    }
})
