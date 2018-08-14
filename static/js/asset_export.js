$(function () {
    $("#asset_export_submit").click(function () {
        var data = {};
        $("#search_conditions").find("select").each(function () {
            data[$(this).attr("name")] = [];
        });
        $("#search_conditions").find("select").each(function () {
            data[$(this).attr("name")].push($(this).val());
        });
        console.log(data);
        $.ajax({
            url: "/cmdb_web/asset_export.html",
            type: "POST",
            dataType: "JSON",
            traditional: true,
            data: data,
            success: function (response) {
                if (response.status) {

                } else {

                }
            },
            error: function () {

            }
        });
    });
});