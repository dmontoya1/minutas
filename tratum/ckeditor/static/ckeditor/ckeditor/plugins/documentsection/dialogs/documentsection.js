CKEDITOR.dialog.add( 'sectionDialog', function(editor){
    return {
        title: 'Agregar sección/claúsula dinámico',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'tab-select-section',
                label: 'Seleccionar sección existente',
                elements: [
                    {
                        type: 'select',
                        id: 'document-section',
                        className: 'document-section',
                        label: 'Secciones/cláusulas disponibles para el documento:',
                        items: [],
                        onLoad: function(e){
                            populateDocumentSections();
                        }
                    }
                ]
            },
            {
                id: 'tab-create-section',
                label: 'Crear sección',
                elements: [
                    {
                        type: 'html',
                        html: '<p>Crea una nueva sección en la ventana emergente.</p>'
                    }
                ]
            }
        ],
        onOk: function(){
            var dialog = this;

            var field_value = dialog.getValueOf('tab-select-section', 'document-section')
            var content = axios.get(`/document-manager/document-sections/${field_value}/`)
                .then(function(response) {
                    editor.insertHtml(
                        `{% if ${field_value} %}` +
                            response.data.content +
                        `{% endif %}`
                    );
                })
                .catch(function (error) {
                    alert('Ocurrió un error')
                });            
        },
        onShow: function(){
            existingLinks = document.querySelector('a.link')

            if(existingLinks){
                existingLinks.remove()
            }

            documentSelect = document.querySelector('select.document-section');
            addNewButton = document.querySelector('[id^="cke_tab-create-section_"]');
            updateDocumentsLink = document.createElement('a');
            updateDocumentsLinkText = document.createTextNode("Recargar");
            updateDocumentsLink.appendChild(updateDocumentsLinkText);
            updateDocumentsLink.title = 'Recargar'
            updateDocumentsLink.className += "link"; 

            document.querySelector('.cke_dialog_ui_labeled_label').append(updateDocumentsLink);

            addNewButton.addEventListener("click", function(e){
                e.preventDefault();
                addWindow = window.open("/admin/document_manager/documentsection/add/?_to_field=id&_popup=1", 'Agregar sección','height=750, width=950');
                if(window.focus){
                    addWindow.focus();
                }
                addWindow.onbeforeunload = function(){
                    document.querySelector('[id^="cke_tab-select-section_"]').click();
                    populateDocumentSections();
                }
            })

            updateDocumentsLink.addEventListener("click", function(e){
                populateDocumentSections();
            })

        }
    };
});

function populateDocumentSections(){
    object_id = document.querySelector('.object-info');
    filter = '';
    if(object_id){
        filter = 'document_id=' + object_id.dataset.id;
    }
    axios.get(`/document-manager/document-sections/?${filter}`)
        .then(function(response) {
            select = document.querySelector('select.document-section');
            select.options.length = 0;
            response.data.forEach(element => {
                var opt = document.createElement('option');
                opt.value = element.formated_slug;
                opt.innerHTML = element.name;
                select.add(opt);
            });
        })
        .catch(function (error) {
            return []
        });
}