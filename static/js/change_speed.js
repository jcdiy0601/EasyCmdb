$(function () {

    // 打开模态对话框
    $(".change-speed").click(function () {
        // 清空input标签内容
        $("#inputspeed").val("");
        // 清空input标签后错误提示
        $("#error-tag").html("");
        nid = $(this).attr("nid");
        $("#change-speed-div").css("display", "block");

    });

    // 关闭模态对话框
    $("#close").click(function () {
        $("#change-speed-div").css("display", "none");
    });

    // 发送ajax请求
        $("#confirm").click(function () {
            // 获取输入
            var new_speed = $("#inputspeed").val();
            if (isNaN(new_speed)){
                $("#error-tag").html("必须为数字");
                return false;
            }
            $.ajax({
                url: "/cmdb_web/asset_detail_update_speed.html",
                type: "POST",
                dataType: "JSON",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                data: {"nid": nid, "new_speed": new_speed},
                success: function (response) {
                    if (response.status) {
                        window.location.reload()
                    } else {
                        $("#error-tag").html(response.message);
                    }
                },
                error: function () {

                }
            });
        });

});