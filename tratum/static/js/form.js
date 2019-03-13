axios.defaults.headers.common['Api-Key'] = document.getElementById('doc-info').dataset.apikey;
axios.defaults.headers.common['X-CSRFToken'] = document.getElementById('doc-info').dataset.csrftoken;


function savePreview() {
    function getGroupFields(form){
        groups = {};
        quantity = {};
        name = "";
        $('.group-fields').each(function(i1, gf){
            group_responses = [];
            group_objects = [];
            regex = $(this).data('regex');
            name = $(this).data('name');
            pk = $(this).data('pk');
            items = $(this).find(`.group-item`).not('.group-fields .group-fields .group-item');
            $(items).each(function(i2, gi){
                new_object = {};
                fields = $(this).find('input, select, textarea');
                regexed_text = regex;

                new_object = []
                $(fields).each(function(i3, git){
                    regexed_text = regexed_text.replace($(this).data('name'), $(this).val());
                    //new_object[$(this).data('name')] = $(this).val();
                    new_object += $(this).data('name') + ":" + $(this).val() + "|";
                });
                group_objects.push(new_object);
                group_responses.push(regexed_text);
            });

            groups[name] = group_responses.join('¬ ').toString();
            groups[name+"_vars"] = group_objects.join('¬ ').toString();
            quantity['Q_' + $(this).data('name')] = items.length;
        });

        data = $.param(groups);
        return form + '&' + data + '&' + $.param(quantity)
    }

    function applyRegexInTextAreas(form){
        var groups = {};
        var textareas = $('#document-form').find(`textarea`);
        $(textareas).each(function(i2, gi){
            groups[$(this).attr('name')] = $(this).val().replace(/\r\n|\r|\n/g,"<br />");
        });
        var data = $.param(groups);
        return form + '&' + data
    }
    form = $('#document-form').serialize();
    form = getGroupFields(form);
    form = applyRegexInTextAreas(form);

    axios.post('/api/document-manager/save-preview/', form)
        .then(function(){
            realTimeUpdate();
        })
}

function formatDocument(){
    const units = {
        1: 'Primer',
        2: 'Segund',
        3: 'Tercer',
        4: 'Cuart',
        5: 'Quint',
        6: 'Sext',
        7: 'Séptim',
        8: 'Octav',
        9: 'Noven',
    };
    const tens = {
        10: 'Décim',
        20: 'Vigésim',
        30: 'Trigésim',
        40: 'Cuadragésim',
        50: 'Quincuagésim'
    };

    var femaleCounters = document.querySelectorAll('input[value="dynamic_counter"]');
    var maleCounters = document.querySelectorAll('input[value="dynamic_counter_male"]');
    var internalCounters = document.querySelectorAll('input[value^="section_dynamic_counter"]');
    var numberCounters = document.querySelectorAll('input[value="dynamic_number_counter"]');

    addCounters(femaleCounters, 'a');
    addCounters(maleCounters, 'o');
    addInternalCounters(internalCounters);
    addNumberCounters(numberCounters);

    function addInternalCounters(internalCounters){
        var sections = [];
        for (i = 0; i < internalCounters.length; i++) {
            section = internalCounters[i].value.split('section_dynamic_counter_')
            sections.push(section[1]);
        }

        sections = Array.from(new Set(sections));

        for (i = 0; i < sections.length; i++) {
            var internalCounters = document.querySelectorAll(`input[value="section_dynamic_counter_${sections[i]}"]`);
            addCounters(internalCounters, 'o');
        }
    }

    function addNumberCounters(numberCounters) {
        for (var i=0; i < numberCounters.length; i++){
            var span = document.createElement('span');
            var counter = i + 1;
            span.style.color = '#000';
            span.innerHTML = counter.toString();
            numberCounters[i].parentNode.replaceChild(span, numberCounters[i]);
        }
    }

    function addCounters(dynamic_counters, gender){
        var i;
        for (i = 0; i < dynamic_counters.length; i++) {
            i = i + 1
            if(i.toString().length == 1){
                counter = units[i] + gender;
            } else {
                ten = i.toString()[0] + 0
                ten = tens[ten]
                ten = ten + gender
                unit = i.toString()[1]
                if(unit == 0){
                    counter = ten
                } else {
                    unit = units[unit] + gender
                    counter = ten + ' ' + unit
                }
            }
            var span = document.createElement('span');
            span.style.color = '#000';
            span.innerHTML = counter.toUpperCase();
            if(i != 0){
                i = i - 1;
            }
            dynamic_counters[i].parentNode.replaceChild(span, dynamic_counters[i]);
        }
    }

    setTimeout(function(){
        var x = document.querySelectorAll('p:empty');
        for (i = 0; i < x.length; i++) {
            x[i].remove();
        }

        var x = document.getElementsByTagName('li');
        for (i = 0; i < x.length; i++) {
            if(x[i].innerText == ""){
                x[i].remove();
            }
        }
    }, 200);


    setTimeout(function(){
        var x = document.getElementsByTagName('li');
        for (i = 0; i < x.length; i++) {
            if(x[i].innerText == ""){
                x[i].remove();
            }
        }
    }, 500);
}

function cloneGroupItem(groupAdder, fromGroupAdder){
    items = $('.group-fields').find(`.group-item[data-group='${$(groupAdder).data('group')}']`);
    length = items.length + 1;
    last = $(items).last();
    clone = last.clone();
    title = clone.find('span');
    inputs = clone.find('input, select, textarea');

    if( inputs.length === 1){
        new_text = length + title.text().substring(1);
        title.text(new_text);
    }

    $(inputs).each(function(i, element){
        $(element).val('');
        name = $(element).data('name');
        $(element).attr('name', `${name}_${length}`);
        $(element).attr('id', `${name}_${length}`);
    });

    if(clone.find('.deleter').length === 0){
        clone.append(
            '<a class="deleter" href="#">' +
                'Eliminar' +
            '</a>'
        )
    }

    clone.insertBefore($(groupAdder));

    if(fromGroupAdder==true){
        rescroll(clone);
    }

    $('a.deleter').on('click', function(e){
        if( e.which == 1 ){
            e.preventDefault();
            prev = $(this).parent().prev();
            $(this).parent().remove();
            rescroll(prev);
            savePreview();
        }
    });

    setListeners();

}

function rescroll(e){
    $(window).scrollTo($(e), 200, {
        offset: {
            left: 100,
            top: -200
        },
        queue: false
    });
}

function realTimeUpdate(){
    axios.post(`/api/document-manager/form-preview/`, {'identifier': uuid})
        .then(function (response) {
            content = response.data.document_content
            $('#content-preview').fadeOut(1000, function(){
                $(this).empty().append(content).fadeIn();
                formatDocument();
            });

        })
}



$.fn.upform = function() {
    var $this = $(this);
    var container = $this.find(".upform-main");

    $(document).ready(function() {
        $(container).find(".input-block").first().click();
    });

    $(container).on('click', '.input-block:not(.preventForming)', function(){
        rescroll(this);
    });

    $(window).on("scroll", function(){

        $(container).find(".input-block:not(.preventForming)").each(function() {
            var etop = $(this).offset().top;
            var diff = etop - $(window).scrollTop();

            if (diff > 50 && diff < 300) {
                reinitState(this);
            }
        });

    });

    function reinitState(e) {
        $(container).find(".input-block").removeClass("active");
        $(container).find(".input-block input").each(function() {
            $(this).blur();
        });
        $(e).addClass("active");
        $('[data-toggle="tooltip"]').tooltip('hide');
        //$(e).find('[data-toggle="tooltip"]').tooltip('show');
        $(e).find('input:not(.date)').focus();
    }

    function rescroll(e) {
        $(window).scrollTo($(e), 200, {
            offset: { left: 100, top: -200 },
            queue: false
        });
    }

    function reinit(e) {
        reinitState(e);
        rescroll(e);
    }


};

form = $(".upform").upform();

function rescroll(e) {
    $(window).scrollTo($(e), 200, {
        offset: { left: 100, top: -200 },
        queue: false
    });
}

function moveNext(e) {
    $(e).parent().parent().next().click();
}

function movePrev(e) {
    $(e).parent().parent().prev().click();
}


$('.modal-trigger').on('click', function() {
    $('#videoModal').modal();
});

$('.preview').on('click', function(e){
    e.preventDefault();
    savePreview();
    window.location.href = $(this).attr('href');
});


function setListeners(){

    $('[data-toggle="tooltip"]').tooltip();

    $("#document-form").off('keydown');
    $("#document-form").on('keydown', 'input', function(e){
        if(e.which === 9){
            e.preventDefault();
        }
    });

    $("#document-form").off('keyup');
    $("#document-form").on('keyup', 'input', function(e) {
        savePreview();
        e.preventDefault();
        if($(this).hasClass('pickadate')){
            return;
        }
        if (e.which === 13 || e.which === 9) {
            if (!($(this).hasClass("required") && $(this).val() == "")){
                moveNext(this);
            }
            return
        }
        if (e.which === 38 || e.which === 40) {
            moveNext(this);
        }
    });

    $('#document-form .section-item').off('click');
    $('#document-form .section-item').on('click', function(e){
        $(`*[data-section="${$(this).attr('name')}"]`).toggle();
    })

    $('#document-form .group-adder').off('click');
    $('#document-form .group-adder').on('click', function(e){
        e.preventDefault();
        cloneGroupItem($(this), true);
    });

    $("#document-form .multiple-checkbox-fields").off('change');
    $("#document-form .multiple-checkbox-fields").change(function() {
        var parentName = $(this).data('parent');
        var parent = $("input[name='"+parentName+"']")
        $(parent).val("");
        $(".multiple-checkbox-fields[data-parent='"+parentName+"']").each(function(i, element){
            var ischecked= $(element).is(':checked');
            if(ischecked){
                before = $(parent).val() ;
                if(before==""){
                    $(parent).val($(element).val());
                }else{
                    $(parent).val( before + "¬" + $(element).val() );
                }
            }
        }).promise().done(function(){
            savePreview();
        });
    });

    $('#document-form .date').attr('placeholder', 'Seleccione una fecha...');

    $('#document-form .pickadate').pickadate({
        format: 'dd/mm/yyyy',
        formatSubmit: 'dd/mm/yyyy',
        selectYears: 100,
        selectMonths: true,
        max: new Date(2050,7,14),
        onClose: function() {
            savePreview();
        },
    });
    $('#document-form .natural').pickadate({
        format: 'dd mmmm !d!e!l yyyy',
        formatSubmit: 'dd mmmm !d!e yyyy',
        selectYears: 100,
        selectMonths: true,
        max: new Date(2050,7,14),
        onClose: function() {
            savePreview();
        },
    });

    $('#document-form .pricetag').priceFormat({
        prefix: '$',
        centsSeparator: ',',
        thousandsSeparator: '.',
        centsLimit: 0,
        clearOnEmpty: true,
         onClose: function() {
            savePreview();
        },
    });

    $('#document-form .number').priceFormat({
        prefix: '',
        centsSeparator: ',',
        thousandsSeparator: '.',
        centsLimit: 0,
        clearOnEmpty: false,
         onClose: function() {
            savePreview();
        },
    });

    $('#document-form select:not(.dynamic)').off('change');
    $('#document-form select.dynamic').off('change');

    $('#document-form select:not(.dynamic)').on('change', function(e){
        e.preventDefault();
        savePreview();
    });
    $('#document-form select.dynamic').on('change', function(e, answers=undefined){
        loadDynamicFields($(this), e, answers);
    });

    $("#document-form").off('keyup');
    $("#document-form").on('keyup', 'textarea',function (e) {
        savePreview();
    });

    $('textarea').textAdjust();

}

setListeners();

function removeHtmlFieldsRelatedToParent(parent){
    var select = $('[data-question="'+parent+'"]').find('select');
    select.each(function(index) {
        if( $(this).hasClass('dynamic') ){
            removeHtmlFieldsRelatedToParent( $(this).attr('name') );
        }
    });
    $('[data-question="'+select.attr('name')+'"]').remove();
    $('[data-question="'+parent+'"]').remove();
}

function loadDynamicFields(element, e, answers=undefined){
    var field = element.attr('name');
    var parent = element.closest('.input-block');
    var value = element.find(":selected").text();
    var id = element.find(":selected").data('id');
    var number = parent.data('number');
    var parentNumber = parent.data('parent-number');
    if( parentNumber != 0 && parentNumber != undefined ){
        number = parentNumber.toString() + "." + number.toString();
    }

    var parentField = element;
    var moreDynamics = [];

    if(id){
        axios.get('/api/document-manager/document-options/'+id+'/linked-fields/?number='+number)
            .then(function(response){
                var newBlock = undefined;
                fields = response.data.fields

                // remove related fields
                removeHtmlFieldsRelatedToParent(field);

                if (fields.length > 0){
                    // all elements are added in inverse mode (first add last to first)
                    // create questions elements
                    Object.keys(fields).forEach(function(key) {
                        newBlock = $(fields[key]);
                        $(newBlock).attr('data-question', field);
                        parent.after(newBlock);
                        var newField = newBlock.find('select');
                        if( newField.hasClass('dynamic') ){
                            moreDynamics.push(newField);
                        }
                    });
                    // create title
                    title = `<h5 class="linked-title" data-parent="${id}" data-question="${field}">Los siguientes campos aparecen por que seleccionaste <strong>${value}</strong></h5>`
                    parent.after(title);
                }

                if(answers){

                    loadGroupFields(answers);

                    Object.keys(answers).forEach(function(key) {
                        input = $('#document-form').find(`input[name='${key}']`)
                        if(input.length > 0){
                            input.val(answers[key]);
                            input.prop("checked", true);
                            $(`*[data-section="${$(input).attr('name')}"]`).toggle();
                        } else {
                            input = $('#document-form').find(`select[name='${key}']`)
                            input.find(`option[value='${answers[key]}']`).prop("selected", true);

                            textarea = $('#document-form').find(`textarea[name='${key}']`);
                            textarea.val(answers[key].replace(/<br\s?\/?>/g,"\n"));
                        }
                    });
                    setListeners();
                    if(moreDynamics.length > 0){
                        moreDynamics.forEach(function(element){
                            element.trigger('change', answers);
                        });
                    }
                }else{
                    setListeners();
                    savePreview();
                    var y = $(window).scrollTop();  //your current y position on the page
                    $(window).scrollTop(y+150);
                }

            });
    }
}

function loadGroupFields(answers){
    Object.keys(answers).forEach(function(key) {
        if(key.startsWith('Q_')){
            length = answers[key];
            key = key.substring(2);
            group = $(`.group-fields[data-name="${key}"]`);
            adder = group.find('.group-adder');
            items = $('.group-fields').find(`.group-item[data-group='${$(adder).data('group')}']`);
            if(length > 1 && items.length < length){
                c = length - 1;
                for (i = 0; i < c; i++) {
                    cloneGroupItem(adder, false);
                }
            }

        }
    });
}

$(function(){
    uuid = $('#doc-info').data('uuid')
    axios.get(`/api/store/user-document/${uuid}/`)
        .then(function (response) {
            answers = response.data.answers
            if(answers){

                loadGroupFields(answers);

                Object.keys(answers).forEach(function(key) {
                    input = $('#document-form').find(`input[name='${key}']`);
                    if(input.length > 0){
                        input.attr('value', answers[key])
                        input.prop("checked", true);
                        $(`*[data-section="${$(input).attr('name')}"]`).toggle();
                    } else {
                        input = $('#document-form').find(`select[name='${key}']`)
                        input.find(`option[value='${answers[key]}']`).prop("selected", true);

                        textarea = $('#document-form').find(`textarea[name='${key}']`);
                        textarea.value = answers[key];
                    }


                });
            }
            realTimeUpdate();
            $('#document-form select.dynamic').trigger('change', answers);
        })
});
