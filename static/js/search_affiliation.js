$(function () {
    $("#post_btn").click(function () {
        var ip = $("#ip").val();

        if (ip.length === 0) {
            alert("必须输入要查询的虚拟机IP！");
            return false;
        }

        $("#task_result_container").empty();

        $.ajax({
            url: "/cmdb_web/search_affiliation.html",
            type: "POST",
            dataType: "JSON",
            traditional: true,
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            data: {"ip": ip},
            success: function (response) {
                if (response.status) {
                    console.log(response.data);
                    $.each(response.data, function (ip, esxi_ip) {
                        var li_ele = "<li>虚拟机IP:" + ip + "</li><pre>匹配到esxi服务器IP:" + esxi_ip + "</pre>";
                        $("#task_result_container").append(li_ele);
                    })
                }
            },
            error: function (response) {

            }
        });
    });
});