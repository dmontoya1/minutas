
(function() {
    var x = document.querySelectorAll('input[value="dynamic_counter"');
    var i;
    for (i = 0; i < x.length; i++) {
        var span = document.createElement('span');
        span.innerHTML = i + 1;
        span.style.color = '#000';
        x[i].parentNode.replaceChild(span, x[i]);
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

})();