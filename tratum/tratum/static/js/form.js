axios.defaults.headers.common['Api-Key'] = document.getElementById('doc-info').dataset.apikey;
axios.defaults.headers.common['X-CSRFToken'] = document.getElementById('doc-info').dataset.csrftoken;

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
        $(e).find('input').focus();
        savePreview();
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

    function savePreview() {
        serializedForm = $('#document-form').serialize();
        axios.post('/api/document-manager/save-preview/', serializedForm)
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
    }
};

form = $(".upform").upform();

$('.modal-trigger').on('click', function() {
    $('#videoModal').modal();
});

$('[data-toggle="tooltip"]').tooltip(); 

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

$('#document-form').on('submit', function(e){
    e.preventDefault();
    submitFields = []
    formFields = $(this).serializeArray();
    submitFields.push(formFields);
    $('#loadingModal').modal();
    $('.group-fields').each(function(i, fd){
        console.log($(fd));
        expression = $(this).data('expression');
        ex_fields = expression.match('{{(.*?)}}')
        $(this).find('.group-item').each(function(i, it){
            console.log($(it));           
            submitFields.push(ex_fields.replace($(this).value()).match(ex_fields))
        });
    });

    $(this).unbind('submit').submit();
})

$(function(){
    uuid = $('#doc-info').data('uuid')
    axios.get(`/api/store/user-document/${uuid}/`)
        .then(function (response) {
            answers = response.data.answers
            Object.keys(answers).forEach(function(key) {
                input = $('#document-form').find(`input[name='${key}']`)
                if(input){
                    input.val(answers[key]);
                }
            });
        })
});
