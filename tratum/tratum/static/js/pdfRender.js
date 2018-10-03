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

(function() {
    addCounters(femaleCounters, 'a');
    addCounters(maleCounters, 'o');
    addInternalCounters(internalCounters);
    
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
});

