const formAction = document.querySelector('.form-action')
const buttons = formAction.querySelectorAll('button')
const inputHidden = formAction.querySelector('[hidden]')
buttons.forEach((btn) => {
  btn.addEventListener('click', () => {
    const confirmAction = confirm('Xác nhận hành động')
    if (confirmAction) {
      inputHidden.value = btn.value
      formAction.submit()
    }
  })
})