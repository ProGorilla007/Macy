document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.slider');
    var instances = M.Slider.init(elems, 900);

    var dropdownOptions = {
        'coverTrigger': false,
        'autoTrigger': true,
        'constrainWidth': false,
    }
    var dropdown = document.querySelectorAll('.dropdown-trigger');
    var drop_down_menu = M.Dropdown.init(dropdown, dropdownOptions);
});