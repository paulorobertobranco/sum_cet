$(document).ready(function(){

    get_months($('#train_size').val());

    $('#chkbx_auto_cluster').change(function(){
        if(!$(this).prop('checked')) {
            $('#autocluster').css("display", "block");
        } else{
            $('#autocluster').css("display", "none");
        };
    });

    $('#chkbx_validation').change(function(){
        if($(this).prop('checked')) {
            $('#trainsplit').css("display", "block");
        } else{
            $('#trainsplit').css("display", "none");
        };
    });

    $('#train_size').change(function(){
        get_months($(this).val())
    });

    $('#btn_load').click(function(){


//        TODO: finish cluster selection
        console.log($('#drop_fc_box').find('p').length === 0);

//        ################################################
        return;

        $('#loader').css('display', 'block');
        $('#not_loader').css('display', 'none');

        var auto_cluster = false;
        var url = $(this).attr('data-url');

        if($('#chkbx_auto_cluster').prop('checked')) {
            auto_cluster = true
        };

        var data = {
            'train_size': $('#train_size').val(),
            'auto_cluster': auto_cluster,
            'database_name': $('#database_name').html(),
        }

        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: data,
            success: function(data){
                document.location.href = '/';
            },
            failure: function(data){
                console.log(data['status']);
            },
        });

    });

});

function allowDrop(ev) {
    ev.preventDefault();
};

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
};

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");


    if(ev.path[0].id.startsWith("cluster") || ev.path[0].id.startsWith("drop")) {
        ev.path[0].appendChild(document.getElementById(data));
    } else {
        ev.path[1].appendChild(document.getElementById(data));
    };
};

function get_months(size) {

    var mr = JSON.parse($('#month_list').attr('months'));
    var year = JSON.parse($('#month_list').attr('year'));
    var s = '<div class="row"> <div class="col-sm-1"><strong>' + year.toString() + '</strong></div><div class="col-sm-10><ul class="list-inline">';

    for(m=0; m < mr.length; m++){

        if(m < size){
                s = s + '<li class="list-inline-item selected_month">' + mr[m].toString() + '</li>';
            } else {
                s = s + '<li class="list-inline-item not_selected_month">' + mr[m].toString() + '</li>';
        };

        if(mr[m] == 12 && m < mr.length-1){
            year = year + 1;
            s = s + '</ul></div></div><hr/> <div class="row">';
            s = s + '<div class="col-sm-1"><strong>' + year.toString() + '</strong></div><div class="col-sm-10><ul class="list-inline">';
        };

    };
    s = s + '</ul></div></div>';
    $('#ml').html(s);
};