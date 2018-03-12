$(function () {
    $("#post_btn").click(function () {
        var ip = $("#ip").val();

        if (ip.length === 0) {
            alert("必须输入要查询的网段！");
            return false;
        }

        $("#task_result_container").empty();

        $("#shade").removeClass("hide");
        $("#loading").removeClass("hide");

        $.ajax({
            url: "/cmdb_web/search_ip_json.html",
            type: "POST",
            dataType: "JSON",
            traditional: true,
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            data: {"ip": ip},
            success: function (response) {
                if (response.status) {
                    $("#shade").addClass("hide");
                    $("#loading").addClass("hide");
                    var pre_ele = "<pre>";
                    $.each(response.data, function (val, ip) {
                        pre_ele = pre_ele + ip + "<br />";
                    });
                    pre_ele = pre_ele + "</pre>";
                    $("#task_result_container").append(pre_ele);
                } else {
                    $("#shade").addClass("hide");
                    $("#loading").addClass("hide");
                    alert(response.message);
                }
            },
            error: function (response) {

            }
        });
    });
});