const btnDeletes = document.querySelectorAll('.btn-delete')
const formDelete = document.querySelector('.form-delete')
btnDeletes.forEach((btn) => {
  btn.addEventListener('click', () => {
    const confirmDelete = confirm('Xóa nhà cung cấp này?')
    if (confirmDelete) {
      const inputHidden = formDelete.querySelector('[hidden]')
      inputHidden.value = btn.value
      formDelete.submit()
    }
  })
})