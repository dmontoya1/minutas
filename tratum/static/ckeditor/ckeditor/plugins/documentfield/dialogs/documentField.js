axios.defaults.headers.common['Api-Key'] = 'b7b15cc877c0c0c2d8e6aeee4e68296df24656a2'

CKEDITOR.dialog.add( 'fieldDialog', function(editor){
    return {
        title: 'Agregar campo dinámico',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'tab-select-field',
                label: 'Seleccionar campo existente',
                elements: [
                    {
                        type: 'select',
                        id: 'document-field',
                        className: 'document-select',
                        label: 'Campos disponibles para el documento:',
                        items: [],
                        onLoad: function(e){
                            populateDocumentFields();
                        }
                    },
                    {
                        type: 'select',
                        id: 'filter-field',
                        className: 'filter-select',
                        label: 'Añadir filtro:',
                        items: [
                            ['Convertir número a texto'],
                            ['Convertir texto a mayúscula inicial'],
                            ['Convertir texto a mayúscula sostenida'],
                            ['Convertir texto a minúscula sostenida'],
                            ['Agrupar grupo de campos por comas'],
                            ['Agrupar grupo de campos por listado'],
                            ['Añadir item a lista existente'],
                            ['Ocultar variable en el documento'],
                        ]
                    }
                ]
            },
            {
                id: 'tab-create-field',
                label: 'Crear campo',
                elements: [
                    {
                        type: 'html',
                        html: '<p>Crea un nuevo campo en la ventana emergente.</p>'
                    }
                ]
            }
        ],
        onOk: function(){
            filter_map = {
                'Convertir número a texto': 'num_to_text',
                'Convertir texto a mayúscula inicial': 'capfirst',
                'Convertir texto a mayúscula sostenida': 'upper',
                'Convertir texto a minúscula sostenida': 'lower',
                'Agrupar grupo de campos por comas': 'retain_comma',
                'Agrupar grupo de campos por listado': 'comma_sep_to_ul',
                'Añadir item a lista existente': 'comma_sep_to_li',
                'Ocultar variable en el documento': 'hidden',
            }

            var dialog = this;

            var span = editor.document.createElement('span');
            span.setAttribute('class', 'variable_tag');

            field_value = dialog.getValueOf('tab-select-field', 'document-field')
            filter_value = dialog.getValueOf('tab-select-field', 'filter-field')

            text = `{{${field_value}}}`

            if(filter_value){
                text = `{{${field_value}|${filter_map[filter_value]}}}`
            }

            span.setText(text);

            editor.insertElement(span);
        },
        onShow: function(){
            existingLinks = document.querySelector('a.link')

            if(existingLinks){
                existingLinks.remove()
            }

            documentSelect = document.querySelector('select.document-select');
            addNewButton = document.querySelector('[id^="cke_tab-create-field_"]');
            updateDocumentsLink = document.createElement('a');
            updateDocumentsLinkText = document.createTextNode("Recargar");
            updateDocumentsLink.appendChild(updateDocumentsLinkText);
            updateDocumentsLink.title = 'Recargar';
            updateDocumentsLink.className += "link";

            document.querySelector('.cke_dialog_ui_labeled_label').append(updateDocumentsLink);

            addNewButton.addEventListener("click", function(e){
                e.preventDefault();
                object_info = document.querySelector('.object-info');
                filter = ''
                if(object_info){
                    filter = 'document_id=' + object_info.dataset.id;
                }
                addWindow = window.open("/admin/document_manager/documentfield/add/?_to_field=id&_popup=1" + `&${filter}`, 'Agregar campo','height=550,width=950');
                if(window.focus){
                    addWindow.focus();
                }
                addWindow.onbeforeunload = function(){
                    document.querySelector('[id^="cke_tab-select-field_"]').click();
                    populateDocumentFields();
                }
            })

            updateDocumentsLink.addEventListener("click", function(e){
                populateDocumentFields();
            })

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
            select = document.querySelector('select.document-select');
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