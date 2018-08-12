$(function(){
    $('.update').on('click', function(){
        window.location.href = $(this).data('href');
    })
    $('.finish').on('click', function(){
        identifier = $('#doc-info').data('uuid')
        render = $('#document-preview').html()
        console.log(render);
        axios.post(`/api/document-manager/finish/`, {identifier: identifier})
            .then(function (response) {
                location.reload(true);
            })
    })
})