axios.defaults.headers.common['Api-Key'] = document.getElementById('doc-info').dataset.apikey;
axios.defaults.headers.common['X-CSRFToken'] = document.getElementById('doc-info').dataset.csrftoken;


function savePreview() {
    function getGroupFields(form){      
        groups = {};
        quantity = {};
        $('.group-fields').each(function(i1, gf){  
            group_responses = [];          
            items = $(this).find('.group-item');
            regex = $(this).data('regex');
            $(items).each(function(i2, gi){  
                fields = $(this).find('input, select');
                regexed_text = regex;
                $(fields).each(function(i3, git){
                    regexed_text = regexed_text.replace($(this).data('name'), $(this).val());
                });                
                group_responses.push(regexed_text);
            });
            quantity['Q_' + $(this).data('name')] = items.length;
            groups[$(this).data('name')] = group_responses.join('¬ ').toString();
            
        });
        return form + '&' + $.param(groups) + '&' + $.param(quantity)
    }   
    
    form = $('#document-form').serialize();
    form = getGroupFields(form);
    
    axios.post('/api/document-manager/save-preview/', form);
}

function cloneGroupItem(groupAdder, fromGroupAdder){
    items = $('.group-fields').find(`.group-item[data-group='${$(groupAdder).data('group')}']`)
    length = items.length + 1
    last = $(items).last();
    clone = last.clone();
    inputs = clone.find('input, select')
    $(inputs).each(function(i, element){
        $(element).val('');
        name = $(element).data('name')
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

$.fn.upform = function() {
    var $this = $(this);
    var container = $this.find(".upform-main");

    $(document).ready(function() {
        $(container).find(".input-block").first().click();
    });

    $(container)
        .find(".input-block")
        .not(".input-block input")
        .on("click", function() {
            rescroll(this);
        });

    $(container).find(".input-block input").keydown(function(e) {
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
    

    $(container).find('.input-block select').change(function(e) {
        savePreview();
        moveNext(this);
    });

    $(window).on("scroll", function(){
        if($(window).width() > 1025){
            $(container).find(".input-block").each(function() {
                var etop = $(this).offset().top;
                var diff = etop - $(window).scrollTop();
    
                if (diff > 100 && diff < 300) {
                    reinitState(this);
                }
            });   
        }            
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
            }            
        })
});
