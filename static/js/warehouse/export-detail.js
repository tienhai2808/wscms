const buttonSubmit = document.querySelector('.div-button').querySelectorAll('button')
const divForm = document.querySelector('.div-form')
buttonSubmit.forEach((btn) => {
  btn.addEventListener('click', () => {
    if (divForm.classList.contains('d-none')) {
      divForm.classList.remove('d-none')
      const formSubmit = divForm.querySelector('form')
      const buttonForm = formSubmit.querySelector('button')
      buttonForm.addEventListener('click', () => {
        if (formSubmit.querySelector('textarea').value === '') {
          alert('Vui lòng viết ghi chú')
        } else {
          const confirmSubmit = confirm('Xác nhận hành động?')
          if (confirmSubmit) {
            const inputHidden = formSubmit.querySelector('[hidden]')
            inputHidden.value = btn.value
            formSubmit.submit()
          }
        }
      })
    }
  })
})
const btnX = divForm.querySelector('[btn-x]')
btnX.addEventListener('click', () => {
  if(!divForm.classList.contains('d-none')) {
    divForm.classList.add('d-none')
  }
}) 
