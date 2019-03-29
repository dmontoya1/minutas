CKEDITOR.plugins.add('documentsection', {
    init: function(editor){
        editor.addCommand('addDocumentSection', new CKEDITOR.dialogCommand('sectionDialog'));

        editor.ui.addButton('documentsection', {
            label: 'Agregar sección dinámica',
            command: 'addDocumentSection',
            icon: 'https://wisdmlabs.com/site/wp-content/uploads/2014/08/documents12.png'
        });

        CKEDITOR.dialog.add('sectionDialog', this.path + 'dialogs/documentSection.js');
    }
});