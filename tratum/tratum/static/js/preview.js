$(function(){
    $('.link-button').on('click', function(){
        window.location.href = $(this).data('href');
    })
    $('.finish').on('click', function(){
        identifier = $('#doc-info').data('uuid')
        $.confirm({
            theme: 'supervan',
            title: '¿Estás seguro que deseas finalizar la edición del documento?',
            content: 'Una vez finalices, no podrás editarlo. Podrás descargar los archivos durante 10 días, \
            y se te enviará una copia a tu correo electrónico. Pasados los 10 días, el documento dejará de estar disponible.',
            buttons: {
                Confirmar: function () {
                    axios.post(`/api/document-manager/finish/`, {identifier: identifier})
                        .then(function (response) {
                            location.reload(true);
                        })
                },
                Cancelar: function () {
                }
            }
        });
    })
})