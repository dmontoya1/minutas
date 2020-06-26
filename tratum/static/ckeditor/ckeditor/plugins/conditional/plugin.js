CKEDITOR.plugins.add('conditional', {
    init: function(editor){
        editor.addCommand('addCondition', new CKEDITOR.dialogCommand('conditionalDialog'));

        editor.ui.addButton('conditional', {
            label: 'Agregar condición',
            command: 'addCondition',
            icon: 'https://static.thenounproject.com/png/139127-200.png'
        });

        CKEDITOR.dialog.add('conditionalDialog', this.path + 'dialogs/conditional.js');
    }
});
