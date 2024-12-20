const divMessage = document.querySelector('.div-message')
if (divMessage && !divMessage.classList.contains('d-none')) {
  setTimeout (() => {
    divMessage.classList.add('d-none')
  }, 4000)
}