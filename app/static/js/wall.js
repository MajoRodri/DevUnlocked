document.querySelectorAll('.btn-edit').forEach(btn => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.card');
    card.querySelector('.card-text').style.display = 'none';
    card.querySelector('.edit-form').style.display = 'block';
    card.querySelector('.edit-textarea').focus();
  });
});

document.querySelectorAll('.btn-cancel').forEach(btn => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.card');
    card.querySelector('.card-text').style.display = '';
    card.querySelector('.edit-form').style.display = 'none';
  });
});
