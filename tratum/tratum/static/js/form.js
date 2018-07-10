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

$(".upform").upform();

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
    $(window).scrollTo($(clone), 200, {
        offset: { left: 100, top: -200 },
        queue: false
    });
    $('a.deleter').on('click', function(e){
        e.preventDefault();
        prev = $(this).parent().prev();        
        $(this).parent().remove();
        rescroll(prev);
    })
})

$('#document-form').on('submit', function(e){
    e.preventDefault();
    fields = []
    form = $(this).serializeArray();
    console.log(form);
    $('#loadingModal').modal();
})