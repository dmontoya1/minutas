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
var head = CKEDITOR.instances.id_content.document.getHead();
var myscript = CKEDITOR.document.createElement( 'script', {
    attributes : {
        type : 'text/javascript',
        'data-cke-saved-src' : '/static/js/documentFormatter.js'
    }
});
head.append( myscript );