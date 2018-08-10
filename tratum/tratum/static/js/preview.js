location.reload(true);

$(function(){
    $('.preview, .update').on('click', function(){
        window.location.href = $(this).data('href');
    })
})