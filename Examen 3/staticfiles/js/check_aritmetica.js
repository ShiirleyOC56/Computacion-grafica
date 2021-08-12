
$(document).ready(function(){

    $('#op_aritmeticas').on('change',function(){
        var valor = $(this).val();

        switch (valor){
            case "1":
                $('#bot').children('#const1').show();
                $('#bot').children('#const2').hide();
                $('#bot').children('#const3').hide();
                $('#bot').children('#const4').hide();
                $('#bot').children('#const5').hide();
                break;
            case "2":
                $('#bot').children('#const1').hide();
                $('#bot').children('#const2').hide();
                $('#bot').children('#const3').hide();
                $('#bot').children('#const4').hide();
                $('#bot').children('#const5').show();
                break;
             default:
                console.log('default');
        }

    });

});

