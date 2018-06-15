if (!$) {
    $ = django.jQuery;
    $(document).ready(function(){
        function maskFields(){
            $('.document-field-oneditor').on('click', function(){
                $(this).remove();
            })
        }
        maskFields();
    })
}