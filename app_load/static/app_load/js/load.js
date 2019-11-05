$(document).ready(function(){

    $('#ml').html(get_months($('#train_size').val()));

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
        $('#ml').html(get_months($(this).val()))
    });

    $('#btn_load').click(function(){

        startloading();

        var auto_cluster = ($('#chkbx_auto_cluster').prop('checked'));
        var url = $(this).attr('data-url');
        var cl = {};

        if(!auto_cluster) {
            if($('#drop_fc_box').find('p').length != 0) {
                stopLoading();
                showNotification('Por favor, selecione 1 cluster para cada causa de falha.');
                return;
            } else {
                $.each($('.cluster'), function(index, cluster){
                    cl[index] = $.map($(cluster).find('p'), function(obj_p) { return $(obj_p).html(); });
                });
            };
        }

        var data = {
            'auto_cluster': auto_cluster,
            'train_size': $('#train_size').val(),
            'database_name': $('#database_name').val(),
            'clusters': JSON.stringify(cl),
        };

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