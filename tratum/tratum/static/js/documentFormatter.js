$(document).ready(function(){  
    $('button[value="dynamic_counter"]').each(function(index) {
        $(this).insertAfter(`<span>${index}. </span>`)
        $(this).remove()
    })        
})