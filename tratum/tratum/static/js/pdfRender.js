$(function(){
    $('input[value="dynamic_counter"]').each(function(index){
        $("<span />", {
            text: index + 1,
            "class": "dynamic_counter"
        }).insertAfter(this);
        $(this).remove();
    })
})