CKEDITOR.plugins.add('documentfield', {
    init: function(editor){
        editor.addCommand('addDocumentField', new CKEDITOR.dialogCommand('fieldDialog'));

        editor.ui.addButton('documentfield', {
            label: 'Agregar campo dinámico',
            command: 'addDocumentField',
            icon: 'https://cdn3.iconfinder.com/data/icons/box-and-shipping-supplies-icons/436/Compliance_Clipboard-512.png'
        });

        CKEDITOR.dialog.add('fieldDialog', this.path + 'dialogs/documentField.js');
    }
});
