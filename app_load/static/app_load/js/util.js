/**
* Start loader
*/
function startloading() {
    $('#loader').css('display', 'block');
    $('#not_loader').css('display', 'none');
};


/**
* Stop loader
*/
function stopLoading() {
    $('#loader').css('display', 'none');
    $('#not_loader').css('display', 'block');
};


/**
* Allow droping failure causes on boxes
* @param  {Event}   ev  Event.
*/
function allowDrop(ev) {
    ev.preventDefault();
};


/**
* Dragging failure causes
* @param  {Event}   ev  Event.
*/
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
};


/**
* Droping failure causes
* @param  {Event} ev  Event.
*/
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");

    if(ev.path[0].id.startsWith("cluster") || ev.path[0].id.startsWith("drop")) {
        ev.path[0].appendChild(document.getElementById(data));
    } else {
        ev.path[1].appendChild(document.getElementById(data));
    };
};


/**
* Mount validation month html string
* @param  {int}    train_size   Selected train size.
* @return {String} s            Mounted html validation month string
*/
function get_months(train_size) {

    var mr = JSON.parse($('#month_list').attr('months'));
    var year = JSON.parse($('#month_list').attr('year'));

    var s = '<div class="row">' +
                '<div class="col-sm-1"><strong>' +
                    year.toString() +
                '</strong></div>' +
                '<div class="col-sm-10>' +
                    '<ul class="list-inline">';

    for(m=0; m < mr.length; m++){

        if(m < train_size){
                s = s +
                    '<li class="list-inline-item selected_month">' +
                        mr[m].toString() +
                    '</li>';

            } else {
                s = s +
                    '<li class="list-inline-item not_selected_month">' +
                        mr[m].toString() +
                    '</li>';
        };

        if(mr[m] == 12 && m < mr.length-1){
            year = year + 1;
            s = s +
                        '</ul>'  +
                    '</div>' +
                '</div>' +
                '<hr/>' +
                '<div class="row">';

            s = s +
                '<div class="col-sm-1"><strong>' +
                    year.toString() +
                '</strong></div>' +
                '<div class="col-sm-10>' +
                    '<ul class="list-inline">';
        };

    };
    s = s +
                '</ul>' +
            '</div>' +
        '</div>';

    return s
};