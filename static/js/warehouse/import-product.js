const addProduct = document.querySelector('[add-product]')
const formImport = document.querySelector('form')
addProduct.addEventListener('click', () => {
  const divImport = formImport.querySelector('.import-detail')
  const elementAdd = divImport.children
  const newDivImport = document.createElement('div')
  newDivImport.classList.add('import-detail', 'new')
  const divButton = document.createElement('div');
  divButton.classList.add('div-close')
  divButton.innerHTML = `<i class="fa-regular fa-circle-xmark close-button"></i>`;
  divButton.querySelector('.close-button').addEventListener('click', () => {
    newDivImport.remove(); 
  });
  newDivImport.appendChild(divButton);
  Array.from(elementAdd).forEach(child => {
    newDivImport.appendChild(child.cloneNode(true));
  });
  divImport.insertAdjacentElement('afterend', newDivImport)
})
