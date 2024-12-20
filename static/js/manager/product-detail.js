const formDelete = document.querySelector('.form-delete')
const buttonDelete = formDelete.querySelector('button')
buttonDelete.addEventListener('click', () => {
  const confirmDelete = confirm('Xóa sản phẩm?')
  if (confirmDelete) {
    formDelete.submit()
  }
})