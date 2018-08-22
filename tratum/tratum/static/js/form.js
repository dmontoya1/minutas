axios.defaults.headers.common['Api-Key'] = document.getElementById('doc-info').dataset.apikey;
axios.defaults.headers.common['X-CSRFToken'] = document.getElementById('doc-info').dataset.csrftoken;


function savePreview() {
    function getGroupFields(serializedForm){      
        groups = {};
        $('.group-fields').each(function(i1, gf){  
            group_responses = [];          
            items = $(this).find('.group-item');
            regex = $(this).data('regex');
            $(items).each(function(i2, gi){  
                fields = $(this).find('input, select');
                $(fields).each(function(i3, git){
                    regex = regex.replace($(this).attr('name'), $(this).val());
                    group_responses[i2] = regex;
                });                
            });
            groups[$(this).data('name')] = group_responses.join(', ').toString();
        });
       return $.param(groups)
    }   
    form = $('#document-form').serialize();
    form = form + '&' + getGroupFields();
    axios.post('/api/document-manager/save-preview/', form);
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
});

$('.natural').pickadate({
    format: 'dddd, dd mmmm !d!e!l yyyy',
    formatSubmit: 'dddd, dd mmmm !d!e yyyy',
});


$('.group-adder').on('click', function(e){
    e.preventDefault();
    el = $('.group-fields').find(`[data-group='${$(this).data('group')}']`).first();
    clone = el.clone();
    clone.find('input').val('');
    counter = $('.group-fields').find(`[data-group='${$(this).data('group')}']`).length; 
    clone.find('div.counter span').html(counter);
    clone.append(
        '<a class="deleter" href="#">' +
            'Eliminar' +
        '</a>'
    )
    clone.insertBefore($(this));
    
    rescroll(clone);

    $('a.deleter').on('click', function(e){
        e.preventDefault();
        prev = $(this).parent().prev();        
        $(this).parent().remove();
        rescroll(prev);
    })

    function rescroll(e){
        $(window).scrollTo($(e), 200, {
            offset: {
                left: 100,
                top: -200
            },
            queue: false
        });
    }
})


$('.preview').on('click', function(e){
    e.preventDefault();
    savePreview();
    window.location.href = $(this).attr('href');
})

$(function(){
    uuid = $('#doc-info').data('uuid')
    axios.get(`/api/store/user-document/${uuid}/`)
        .then(function (response) {
            answers = response.data.answers
            Object.keys(answers).forEach(function(key) {
                input = $('#document-form').find(`input[name='${key}']`) 
                if(input.length > 0){
                    input.val(answers[key]);
                } else {
                    input = $('#document-form').find(`select[name='${key}']`)
                    input.find(`option[value='${answers[key]}']`).prop("selected", true);
                }
            });
        })
});
