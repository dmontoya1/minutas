$(function(){
    $('input[value="dynamic_counter"]').each(function(index){
        $("<span />", {
            text: index + 1,
            "class": "dynamic_counter"
        }).insertAfter(this);
        $(this).remove();
    })    
    $('body').append('<button id="generatePDF">Generar PDF</button>')
    $('p').each(function(i, e){
        if($(this).css('text-align') == 'center'){

        } else {$(this).css('text-align', 'justify')}
    })
    $('#generatePDF').on('click', function(){
        var doc = new jsPDF();
        doc.fromHTML($('body').get(0), 10, 10, {
            'width': 180
        });
        doc.save()
    })
})

function onRender(){
    var url = '//cdn.mozilla.net/pdfjs/PDF.pdf';
    var pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function(pdf) {
    console.log('PDF loaded');
    
    var pageNumber = 1;
    pdf.getPage(pageNumber).then(function(page) {
            console.log('Page loaded');
            
            var scale = 1.5;
            var viewport = page.getViewport(scale);

            var canvas = document.getElementById('the-canvas');
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            var renderTask = page.render(renderContext);
            renderTask.then(function () {
            console.log('Page rendered');
        });
    });
    }, function (reason) {
        console.error(reason);
    });
}