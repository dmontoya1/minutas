$(function(){
    $('input[value="dynamic_counter"]').each(function(index){
        $("<span />", {
            text: index + 1,
            "class": "dynamic_counter"
        }).insertAfter(this);
        $(this).remove();
    })    
    $('body').append('<button id="generatePDF">Generar PDF</button>')
    $('#generatePDF').on('click', function(){
        var doc = new jsPDF();
        doc.fromHTML($('body').get(0), 10, 10, {
            'width': 120
        });
        doc.save()
    })
})