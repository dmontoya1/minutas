
(function() {
    var x = document.querySelectorAll('input[value="dynamic_counter"');
    var i;
    for (i = 0; i < x.length; i++) {
        var span = document.createElement('span');
        span.innerHTML = i + 1;
        span.style.color = '#000';
        x[i].parentNode.replaceChild(span, x[i]);
    }

    var x = document.querySelectorAll('p:empty, li:empty');
    for (i = 0; i < x.length; i++) {
        x[i].remove();
    }
})();