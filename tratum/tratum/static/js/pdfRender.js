var x = document.querySelectorAll('input[value="dynamic_counter"');
var i;
for (i = 0; i < x.length; i++) {
    var span = document.createElement('span');
    span.innerHTML = i + 1;
    x[i].replaceWith(span);
}