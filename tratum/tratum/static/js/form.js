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
    });

    $(container).find('.input-block select').change(function(e) {
        moveNext(this);
    });

    $(window).on("scroll", function() {
        $(container).find(".input-block").each(function() {
            var etop = $(this).offset().top;
            var diff = etop - $(window).scrollTop();

            if (diff > 100 && diff < 300) {
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
        console.log($(e).parent().parent().next())
        $(e).parent().parent().next().click();
    }

    function movePrev(e) {
        $(e).parent().parent().prev().click();
    }
};

$(".upform").upform();
