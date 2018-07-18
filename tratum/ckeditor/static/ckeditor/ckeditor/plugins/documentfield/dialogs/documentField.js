axios.defaults.headers.common['Api-Key'] = '042c97b1f486c5bde044ba5f10dfd11ad26cb81b'

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
            var dialog = this;

            var abbr = editor.document.createElement('abbr');

            var field_name = document.querySelector('select.document-select')
            var field_name = field_name.options[field_name.selectedIndex].innerHTML;

            abbr.setAttribute( 'title', field_name);
            abbr.setText(dialog.getValueOf('tab-select-field', 'document-field'));

            editor.insertElement(abbr);
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
            url = `/api/documents/document-fields/?${filter}`
        }
    }    
    axios.get(url)
        .then(function(response) {
            select = document.querySelector('select.document-select');
            select.options.length = 0;
            response.data.forEach(element => {
                var opt = document.createElement('option');
                opt.value = `{{${element.formated_slug}}}`;
                opt.innerHTML = element.name;
                select.add(opt);
            });
        })
        .catch(function (error) {
            return []
        });
}