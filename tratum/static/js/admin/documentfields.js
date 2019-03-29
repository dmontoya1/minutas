(function($) {

    $(document).ready(function(){

        $('.changer_submit').on('click', function(e){
            e.preventDefault();
            pk = $(this).prev()
            order = $(this).prev().prev()
            $.post("/api/document-manager/change-admin-order/",{ pk: pk.val(), order: order.val() })
                .done(function() {
                    alert("Cambiado exitosamente");
                })
        });

        $('.changer_option_submit').on('click', function(e){
            e.preventDefault();
            pk = $(this).prev()
            order = $(this).prev().prev()
            $.post("/api/document-manager/change-admin-option-order/",{ pk: pk.val(), order: order.val() })
                .done(function() {
                    alert("Cambiado exitosamente");
                })
        });
    })

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };
    if(getUrlParameter('_popup') == 1){
        did = getUrlParameter('document_id');
        opts = $('#id_document').find('option');
    }



})(django.jQuery);
