const labels = document.querySelectorAll('label')
labels.forEach((label) => {
  if (label.textContent === 'Password-based authentication:') {
    label.remove()
  }
})

document.querySelector('#id_usable_password_helptext').remove()
document.querySelector('#id_usable_password').remove()