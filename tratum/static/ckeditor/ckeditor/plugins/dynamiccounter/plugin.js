CKEDITOR.plugins.add('dynamiccounter', {
    init: function(editor){
        editor.addCommand('addDynamicCounter', new CKEDITOR.dialogCommand('counterDialog'));

        editor.ui.addButton('dynamiccounter', {
            label: 'Agregar contador dinámico',
            command: 'addDynamicCounter',
            icon: 'https://cdn.iconscout.com/icon/premium/png-256-thumb/alphabet-list-616084.png'
        });

        CKEDITOR.dialog.add('counterDialog', this.path + 'dialogs/dynamiccounter.js');
    }
});
