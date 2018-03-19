var $jq = jQuery.noConflict();
$jq(document).ready(function(){
    $jq('.enable').click(function(e){
        if(confirm('確定要預約嘛') == true){
            start_date = $jq(this).data()['startdate']
            
            if($jq(this).text() == '開放候補'){
                peroid = 'alternate'
                time = '候補'
            }else{
                peroid = $jq(this)[0].className.split('enable ')[1]  //enable後面要有空格否則會錯
                time = $jq(this).text()
            }

            data = {
                'start_date': start_date,
                'peroid': peroid,
                'time': time
            }
            url = document.location.href.replace('reservation', 'update_reservation')

            $jq.ajax({
                type: "post",
                url: url,
                data: data,
                success: function (response) {
                    if (response == 'success'){
                        document.location.reload()
                    }else if(response =='error'){
                        alert('請重新整理，預約失敗')
                    }
                }
            });
        }
    })
})

 