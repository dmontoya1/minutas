$(function(){

    $('.doc-gen').on('click', function(){
        var converted = htmlDocx.asBlob($('#content-preview').html());
        saveAs(converted, 'TratumDocument.doc');
    })
})

