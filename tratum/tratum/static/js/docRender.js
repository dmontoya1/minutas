$(function(){
    $('.doc-gen').on('click', function(){
        console.log($('#content-preview').html())
        var converted = htmlDocx.asBlob($('#content-preview').html());
        saveAs(converted, 'TratumDocument.docx');
    })
})

