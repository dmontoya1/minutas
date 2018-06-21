CKEDITOR.plugins.add('documentfield', {
    init: function(editor){
        editor.addCommand('addDocumentField', new CKEDITOR.dialogCommand('fieldDialog'));

        editor.ui.addButton('documentfield', {
            label: 'Agregar campo dinámico',
            command: 'addDocumentField',
            icon: 'https://www.orsgroup.com/wp-content/uploads/2014/05/quality-control-icon.png'
        });

        CKEDITOR.dialog.add('fieldDialog', this.path + 'dialogs/documentField.js');
    }
});

CKEDITOR.scriptLoader.load( '/static/js/documentFormatter.js' );