axios.defaults.headers.common['Api-Key'] = document.getElementById('doc-info').dataset.apikey;
axios.defaults.headers.common['X-CSRFToken'] = document.getElementById('doc-info').dataset.csrftoken;


function savePreview() {
    function getGroupFields(form){
        groups = {};
        quantity = {};
        $('.group-fields').each(function(i1, gf){
            group_responses = [];
            regex = $(this).data('regex');
            name = $(this).data('name');
            pk = $(this).data('pk');
            items = $(this).find(`.group-item`).not('.group-fields .group-fields .group-item');
            $(items).each(function(i2, gi){
                fields = $(this).find('input, select');
                regexed_text = regex;
                $(fields).each(function(i3, git){
                    regexed_text = regexed_text.replace($(this).data('name'), $(this).val());
                });

                /* extra_content = null;

                if($(this).children('.group-fields').length > 0){
                    $(this).children('.group-fields').each(function(i1, gf){
                        internal_group_responses = [];
                        internal_regex = $(this).data('regex');
                        internal_name = $(this).data('name');
                        internal_pk = $(this).data('pk');
                        internal_items = $(this).find(`.group-item`);
                        $(internal_items).each(function(i2, gi){
                            internal_fields = $(this).find('input, select');
                            internal_regexed_text = internal_regex;
                            $(internal_fields).each(function(i3, git){
                                internal_regexed_text = internal_regexed_text.replace($(this).data('name'), $(this).val());
                            });
                            internal_group_responses.push(' ' + internal_regexed_text);
                        });
                        extra_content = internal_group_responses
                    });
                }


                if(extra_content != null || extra_content != ""){
                    regexed_text = `${regexed_text}: ${extra_content}`
                } */

                group_responses.push(regexed_text);
            });
            quantity['Q_' + $(this).data('name')] = items.length;
            groups[$(this).data('name')] = group_responses.join('¬ ').toString();
        });
        return form + '&' + $.param(groups) + '&' + $.param(quantity)
    }

    form = $('#document-form').serialize();
    form = getGroupFields(form);

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

    addCounters(femaleCounters, 'a');
    addCounters(maleCounters, 'o');
    addInternalCounters(internalCounters);

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
    length = items.length + 1
    last = $(items).last();
    clone = last.clone();
    inputs = clone.find('input, select')
    $(inputs).each(function(i, element){
        $(element).val('');
        name = $(element).data('name');
        $(element).attr('name', `${name}_${length}`)
        $(element).attr('id', `${name}_${length}`)
    })

    if(clone.find('.deleter').length == 0){
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
        e.preventDefault();
        prev = $(this).parent().prev();
        $(this).parent().remove();
        rescroll(prev);
    })

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

    $(container)
        .find(".input-block:not(.preventForming)")
        .not(".input-block input")
        .on("click", function() {
            rescroll(this);
        });

    $("input").on('keyup', function(e) {
        savePreview();
        if (e.which == 13 || e.which == 9) {
            e.preventDefault()
            if ($(this).hasClass("required") && $(this).val() == "") {
            } else {
                moveNext(this);
            }
        }
        if (e.which == 40) {
            moveNext(this);
        } else if (e.which == 38) {
            movePrev(this);
        }
    });


    // $(container).find('.input-block select').change(function(e) {
    //     savePreview();
    //     moveNext(this);
    // });

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
        $(e).find('[data-toggle="tooltip"]').tooltip('show');
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

    function moveNext(e) {
        $(e).parent().parent().next().click();
    }

    function movePrev(e) {
        $(e).parent().parent().prev().click();
    }

};

form = $(".upform").upform();

$('.modal-trigger').on('click', function() {
    $('#videoModal').modal();
});

$('[data-toggle="tooltip"]').tooltip();

$('.date').attr('placeholder', 'Seleccione una fecha...');

$('.pickadate').pickadate({
    format: 'dd/mm/yyyy',
    formatSubmit: 'dd/mm/yyyy',
    selectYears: 100,
    selectMonths: true,
    max: new Date(2050,7,14)
});

$('.natural').pickadate({
    format: 'dddd, dd mmmm !d!e!l yyyy',
    formatSubmit: 'dddd, dd mmmm !d!e yyyy',
    selectYears: 100,
    selectMonths: true,
    max: new Date(2050,7,14)
});

$('.pricetag').priceFormat({
    prefix: '$',
    centsSeparator: ',',
    thousandsSeparator: '.',
    centsLimit: 0,
    clearOnEmpty: true
});


$('.group-adder').on('click', function(e){
    e.preventDefault();
    cloneGroupItem($(this), true);
})


$('.preview').on('click', function(e){
    e.preventDefault();
    savePreview();
    window.location.href = $(this).attr('href');
})

$('.section-item').on('click', function(e){
    $(`*[data-section="${$(this).attr('name')}"]`).toggle();
})

$('select.dynamic').on('change', function(e){

    field = $(this).attr('name');
    parent = $(this).closest('.input-block');
    value = $(this).find(":selected").text();
    id = $(this).find(":selected").data('id');

    $('[data-question="'+field+'"]').remove();
    if(id){
        axios.get('/api/document-manager/document-options/'+id+'/linked-fields/')
            .then(function(response){
                var element = undefined;
                fields = response.data.fields
                if (fields.length > 0){
                    title = `<h5 class="linked-title" data-parent="${id}" data-question="${field}">Los siguientes campos aparecen por que seleccionaste <strong>${value}</strong></h5>`
                }
                Object.keys(fields).forEach(function(key) {
                    parent.after($(fields[key]));
                    element = $(fields[key]);
                })
                parent.after(title);
                savePreview();

                var y = $(window).scrollTop();  //your current y position on the page
                $(window).scrollTop(y+150);

            })
    }

})

$(function(){
    uuid = $('#doc-info').data('uuid')
    axios.get(`/api/store/user-document/${uuid}/`)
        .then(function (response) {
            answers = response.data.answers
            if(answers){
                Object.keys(answers).forEach(function(key) {
                    if(key.startsWith('Q_')){
                        length = answers[key];
                        key = key.substring(2);
                        group = $(`.group-fields[data-name="${key}"]`);
                        adder = group.find('.group-adder');
                        if(length > 1){
                            c = length - 1;
                            for (i = 0; i < c; i++) {
                                cloneGroupItem(adder, false);
                            }
                        }

                    }
                });
                Object.keys(answers).forEach(function(key) {
                    input = $('#document-form').find(`input[name='${key}']`)
                    if(input.length > 0){
                        input.val(answers[key]);
                        input.prop("checked", true);
                        $(`*[data-section="${$(input).attr('name')}"]`).toggle();
                    } else {
                        input = $('#document-form').find(`select[name='${key}']`)
                        input.find(`option[value='${answers[key]}']`).prop("selected", true);
                    }
                });

                // var y = $(window).scrollTop();  //your current y position on the page
                // $(window).scrollTop(y+50);
            }
        })
    realTimeUpdate();
    $('select.dynamic').trigger('change');
});
