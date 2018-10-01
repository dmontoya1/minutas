CKEDITOR.dialog.add('conditionalDialog', function(editor){
    return {
        title: 'Agregar condición',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'tab-create-conditional',
                label: 'Crear condición',
                elements: [
                    {
                        type: 'select',
                        id: 'conditional-type',
                        className: 'conditional-typ',
                        label: 'Selecciona el tipo de condición:',
                        items: [
                            ['Si el campo fue seleccionado, entonces...'],
                            ['Si el valor del campo es .., entonces...'],
                            ['Si el campo no fue seleccionado, entonces...']
                        ],
                        default: 'Si el campo fue seleccionado, entonces...',
                    },
                    {
                        type: 'text',
                        id: 'conditional-field',
                        label: 'Identificador del campo a validar'
                    },
                    {
                        type: 'text',
                        id: 'conditional-valueif',
                        label: 'Valor a validar (si aplica)'
                    }
                ]
            }
        ],
        onOk: function(){
            var dialog = this;

            var span = editor.document.createElement('span');
            var type = dialog.getValueOf('tab-create-conditional', 'conditional-type');
            var field = dialog.getValueOf('tab-create-conditional', 'conditional-field');
            var valueif = dialog.getValueOf('tab-create-conditional', 'conditional-valueif');
            
            if(type == 'Si el campo fue seleccionado, entonces...'){
                editor.insertHtml(
                    `{% if ${field} %}` +
                        
                    `{% endif %}`
                );
            } else if (type == 'Si el valor del campo es .., entonces...'){
                editor.insertHtml(
                    `{% if ${field} == "${valueif}" %}` +
                        
                    `{% endif %}`
                );
            } else {
                editor.insertHtml(
                    `{% if not ${field} %}` +
                        
                    `{% endif %}`
                );
            }
        }
    };
});
