axios.defaults.headers.common['Api-Key'] = 'b7b15cc877c0c0c2d8e6aeee4e68296df24656a2'

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
                        type: 'select',
                        id: 'conditional-field',
                        className: 'conditional-select',
                        label: 'Campos disponibles:',
                        items: [],
                        onLoad: function(e){
                            populateDocumentFields();
                        }
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

function populateDocumentFields(){
    object_info = document.querySelector('.object-info');
    filter = '';
    if(object_info){
        filter = 'document_id=' + object_info.dataset.id;
        if(object_info.dataset.model == 'documentsection'){
            url = `/document-manager/document-sections/${object_info.dataset.slug}/section-fields/`
        } else if(object_info.dataset.model == 'document'){
            url = `/api/document-manager/document-fields/?${filter}`
        }
    }    
    axios.get(url)
        .then(function(response) {
            select = document.querySelector('select.conditional-select');
            select.options.length = 0;
            response.data.forEach(element => {
                var opt = document.createElement('option');
                opt.value = `${element.formated_slug}`;
                opt.innerHTML = element.name;
                select.add(opt);
            });
        })
        .catch(function (error) {
            return []
        });
}
