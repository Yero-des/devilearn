// const { default: Swal } = require("sweetalert2");

function confirmEnrollment(url) {
    Swal.fire({
        title: "¿Quieres inscribirte?",
        text: "Podrás acceder a todas las lecciones de este curso.",
        icon: "question",        
        showCancelButton: true,
        confirmButtonText: 'Sí, inscribirme',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
};