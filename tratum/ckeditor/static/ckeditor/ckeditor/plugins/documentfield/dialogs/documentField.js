axios.defaults.headers.common['Api-Key'] = '03a6f7c84a760517a1c0b31e4acf6c180de90d16'

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
            }

            var dialog = this;

            var span = editor.document.createElement('span');

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
                addWindow = window.open("/admin/document_manager/documentfield/add/?_to_field=id&_popup=1", 'Agregar campo','height=350,width=650');
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