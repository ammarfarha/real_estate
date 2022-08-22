$("#id_is_company").click(function() {
    if($(this).is(":checked")) {
        $("#div_id_company_name").show(300);
        $("#div_id_web_site").show(300);
        $("#div_id_trade_record").show(300);
    } else {
        $("#div_id_company_name").hide(200);
        $("#div_id_web_site").hide(200);
        $("#div_id_trade_record").hide(200);
    }
});