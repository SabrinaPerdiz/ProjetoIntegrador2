window.onload = function() {
    const alertModal = document.getElementById('alert-modal');
    if (alertModal) {
        setTimeout(() => {
            alertModal.classList.remove('show');
            alertModal.style.display = 'none'; // Esconde o modal
        }, 2000); // 3000 milissegundos = 3 segundos
    }
}

function hideModal() {
    const alertModal = document.getElementById('alert-modal');
    alertModal.classList.remove('show');
    alertModal.style.display = 'none'; // Esconde o modal
}