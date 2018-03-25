var $jq = jQuery.noConflict();

$jq(document).ready(function () {
    $jq('#language').change(function (e) { 
        e.preventDefault();
        val = $jq(this).val()
        if(val == 'en'){
            location.href = 'http://hpe.mingtak.com.tw/en_cover'
        }else if(val == 'ch'){
            location.href = 'http://hpe.mingtak.com.tw/'
        }
    });
});