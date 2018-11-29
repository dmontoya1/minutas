CKEDITOR.dialog.add('counterDialog', function(editor){
    return {
        title: 'Agregar contador dinámico',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'tab-select-counter',
                label: 'Seleccionar campo existente',
                elements: [
                    {
                        type: 'select',
                        id: 'dynamic-counter',
                        className: 'dynamic-counter',
                        label: 'Contadores disponibles:',
                        items: [
                            ['Contador dinámico (masculino)'],
                            ['Contador dinámico (femenino)'],
                            ['Contador dinámico para secciones internas (numérico)']
                        ],
                        default: 'Contador dinámico (masculino)',
                    }
                ]
            }
        ],
        onOk: function(){
            var dialog = this;

            var button = editor.document.createElement('input');
            var value = dialog.getValueOf('tab-select-counter', 'dynamic-counter');
            
            if(value == 'Contador dinámico (masculino)'){
                v = 'dynamic_counter_male'
            } else if (value == 'Contador dinámico (femenino)'){
                v = 'dynamic_counter'
            } else {
                v = 'section_dynamic_counter'
            }

            button.setAttribute('type', 'button');
            button.setAttribute('value', v);
            button.setText(value);

            editor.insertElement(button);
        }
    };
});
