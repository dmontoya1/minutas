$(function(){
    $('input[value="dynamic_counter"]').each(function(index){
        $("<span />", {
            text: index + 1,
            "class": "dynamic_counter"
        }).insertAfter(this);
        $(this).remove();
    })    
    $('.pdf-gen').on('click', function(){
        margins = {
            top: 70,
            bottom: 80,
            left: 30,
            width: 550
        };
        var pdf = new jsPDF('p', 'pt', 'a4');
        pdf.setFontSize(18);
        pdf.fromHTML(document.getElementById('content-preview'), 
            margins.left,
            margins.top,
            {
                width: margins.width
            }, 
            function(dispose) {
                headerFooterFormatting(pdf)
            }, 
            margins
        );
            
        pdf.save();

        function headerFooterFormatting(doc) {
            var totalPages  = doc.internal.getNumberOfPages();

            for (var i = totalPages; i >= 1; i--) { 
                doc.setPage(i);  
                header(doc);
                footer(doc, i); 
            }
        };
        function header(doc){
            doc.setFontSize(8);
            doc.text(270, 40, $('#content-preview').data('name'));
        };
        function footer(doc, pageNumber){
            doc.setFontSize(8);
            doc.text(30, 800, String(pageNumber));
        };
    })
})

