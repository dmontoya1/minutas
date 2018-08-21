var x = document.querySelectorAll('input[value="dynamic_counter"');
var i;
for (i = 1; i < x.length; i++) {
    var span = document.createElement('span');
    span.innerHTML = i;
    x[i].replaceWith(span);
}