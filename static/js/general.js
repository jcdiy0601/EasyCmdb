(function (jq) {
    // 向后台发送请求的url
    var requestURL;
    // 删除数据的url
    var deleteURL;
    // 更新数据的url
    var updateURL;

    // 用于保存当前作用域内的全局变量
    var GENERAL_GLOBAL_DICT = {};

    if (typeof String.prototype.startsWith != "function") {
        String.prototype.startsWith = function (prefix) {
            return this.slice(0, prefix.length) === prefix;
        };
    }


    // 为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    // CSRF配置
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // 全局Ajax中添加请求头X-CSRFToken，用于跨过CSRF验证
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
            }
        }
    });

    // 页面初始化（获取数据，绑定事件）
    function initialize(pager) {
        // 显示遮罩层和等待图片
        $.Show("#shade,#loading");
        // 将查询条件字典转成字符串
        var conditions = JSON.stringify(aggregationSearchCondition());
        var $body = $("#tableBody");
        $.ajax({
            url: requestURL,
            type: "GET",
            traditional: true,
            data: {"condition": conditions, "pager": pager},
            dataType: "JSON",
            success: function (response) {
                // 隐藏遮罩层
                $.Hide("#shade,#loading");
                // 如果返回正确
                if (response.status) {
                    // 初始化全局变量
                    initGlobal(response.data.global_dict);
                    // 初始化表标题
                    initTableHeader(response.data.table_config);
                    // 初始化表内容
                    initTableBody(response.data.page_info.page_start, response.data.data_list, response.data.table_config);
                    // 初始化页码
                    initPager(response.data.page_info.page_str);
                    // 初始化搜索条件
                    initSearchCondition(response.data.condition_config);
                    // 绑定点击CheckBox事件
                    $.BindDoSingleCheck("#tableBody", null, null);
                } else{
                    alert(response.message);
                }
            },
            error: function () {
                $.Hide("#shade, #loading");
            }
        });
    }

    // 初始化全局变量
    function initGlobal(globalDict) {
        /*
        {
            'asset_type_list': self.asset_type_list,
            'business_unit_list': self.business_unit_list,
            'idc_list': self.idc_list,
            'asset_status_list': self.asset_type_list
        }
        */
        $.each(globalDict, function (key, value) {
            GENERAL_GLOBAL_DICT[key] = value;
        });
    }

    // 初始化表格的头部
    function initTableHeader(tableConfig) {
        var $header = $("#tableHead");
        // 删除tableHead下面的所有th标签
        $header.find("th").remove();
        // 创建选择列
        var ck = document.createElement("th");
        ck.innerHTML = "选择";
        $header.find("tr").append(ck);
        // 创建序号列
        var num = document.createElement("th");
        num.innerHTML = "序号";
        $header.find("tr").append(num);
        // 创建标题
        /*
        [
            {'q': 'id', 'title': 'ID', 'display': 0, 'text': {'content': '{n}', 'kwargs': {'n': '@id'}}, 'attr': {}},
            {'q': 'asset_type', 'title': '资产类型', 'display': 1, 'text': {'content': '{n}', 'kwargs': {'n': '@@asset_type_list'}}, 'attr': {}},
        ]
        */
        $.each(tableConfig, function (key, value) {
            if (value.display){
                var tag = document.createElement("th");
                tag.innerHTML = value.title;
                $header.find("tr").append(tag);
            }
        })
    }

    // 初始化表格的内容
    function initTableBody(startNum, dataList, tableConfig) {
        var $body = $("#tableBody");
        // 清空body中的内容
        $body.empty();
        // 创建内容
        /*
        [
            {'id': 1, 'business_unit_id': None, 'asset_status': 'online', 'asset_type': 'server', 'idc_id': 1, 'server_title': 'ytd13'},
            {'id': 2, 'business_unit_id': None, 'asset_status': 'online', 'asset_type': 'server', 'idc_id': None, 'server_title': 'CentOS-01'}
        ]
        [
            {'q': 'id', 'title': 'ID', 'display': 0, 'text': {'content': '{n}', 'kwargs': {'n': '@id'}}, 'attr': {}},
            {'q': 'asset_type', 'title': '资产类型', 'display': 1, 'text': {'content': '{n}', 'kwargs': {'n': '@@asset_type_list'}}, 'attr': {}},
        ]
         */
        $.each(dataList, function (k1, row) {
            // row表示从数据获取的每行字典信息 {'id': 1, 'business_unit_id': None, 'asset_status': 'online', 'asset_type': 'server', 'idc_id': 1, 'server_title': 'ytd13'}
            var tr = document.createElement("tr");
            $(tr).attr("nid", row["id"]);
            $(tr).attr("num", startNum + k1 + 1);
            // 创建每行的CheckB
            var tagTd = document.createElement("td");
            var tagCheckBox = document.createElement("input");
            tagCheckBox.type = "checkbox";
            tagCheckBox.value = row["id"];
            $(tagTd).append(tagCheckBox);
            $(tr).append(tagTd);
            // 创建每行的序号
            var tagNum = document.createElement("td");
            tagNum.innerHTML = startNum + k1 + 1;
            $(tr).append(tagNum);
            // 创建每行的内容
            $.each(tableConfig, function (k2, config) {
                if (config.display){
                    var td = document.createElement("td");
                    // 创建td内容
                    var kwargs = {};
                    $.each(config.text.kwargs, function (key, value) {
                        if (value.startsWith("@@")) {
                            var global_name = value.substring(2, value.length);
                            if (getNameByGlobalList(global_name, row[config.q]) === null){
                                kwargs[key] = "";
                            } else {
                                kwargs[key] = getNameByGlobalList(global_name, row[config.q]);
                            }
                        } else if (value.startsWith("@")) {
                            if (row[value.substring(1, value.length)] === null){
                                kwargs[key] = "";
                            } else {
                                kwargs[key] = row[value.substring(1, value.length)];
                            }
                        } else {
                            kwargs[key] = value;
                        }
                    });
                    td.innerHTML = config.text.content.format(kwargs);
                    // 创建td属性
                    $.each(config.attr, function (key, value) {
                        if (value.startsWith("@")){
                            $(td).attr(key, row[value.substring(1, value.length)]);
                        } else {
                            $(td).attr(key, value);
                        }
                    });
                    $(tr).append(td);
                }
            });
            $body.append(tr);
        });
    }

    // 初始化分页内容
    function initPager(pageStr) {
        var $pager = $("#pager");
        $pager.empty();
        $pager.append(pageStr);
    }

    // 初始化搜索条件
    function initSearchCondition(config) {
        var $serach_condition = $("#search_condition");
        if ($serach_condition.attr("init") === "true"){
            return;
        }
        /*
        [
            {'name': 'asset_type', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'asset_type_list'},
            {'name': 'asset_status', 'text': '资产状态', 'condition_type': 'select', 'global_name': 'asset_status_list'},
            {'name': 'idc_id', 'text': 'IDC机房', 'condition_type': 'select', 'global_name': 'idc_list'},
            {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'business_unit_id', 'text': '所属业务线', 'condition_type': 'select', 'global_name': 'business_unit_list'}
        ]
         */
        if (config.length > 0) {
            var first_item = config[0];
            initDefaultSearchCondition(first_item);
        }
        $.each(config, function (key, value) {
            var condition_type = value["condition_type"];
            var tag = document.createElement("li");
            var a = document.createElement("a");
            a.innerHTML = value["text"];
            $(tag).append(a);
            $(tag).attr("name", value["name"]);
            $(tag).attr("condition-type", condition_type);
            if (condition_type === "select"){
                $(tag).attr("global-name", value["global_name"]);
            }
            $serach_condition.find("ul").append(tag);
        });
        $serach_condition.attr("init", "true");
    }
    
    // 初始化第一个默认的查询条件
    function initDefaultSearchCondition(item) {
        /*
        {'name': 'asset_type', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'asset_type_list'}
        or
        {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
         */
        var tag;
        if (item.condition_type === 'input'){
            tag = $.CreateInput(
                {
                    "is-condition": "true",
                    "class": "form-control",
                    "name": item.name,
                    "placeholder": "逗号分割多条件"
                },
                {}
            );
        } else if (item.condition_type === 'select'){
            tag = $.CreateSelect(
                {
                    "is-condition": "true",
                    "class": "form-control",
                    "name": item.name
                },
                {},
                GENERAL_GLOBAL_DICT[item.global_name],
                null,
                "id",
                "name"
            );
        }
        var $current = $("#search_condition");
        $current.children().first().text(item.text);
        $current.after(tag);
    }
    
    // 聚合查询条件
    function aggregationSearchCondition() {
        var ret = {};
        $("#search_conditions").children().each(function () {
            var $condition = $(this).find("input[is-condition='true'],select[is-condition='true']");
            var name = $condition.attr("name");
            var value = $condition.val();
            // 如果查询条件不是select标签，也就是input标签的时候进行模糊查找
            if (!$condition.is("select")) {
                name = name + "__contains";
            }
            // 如果有值则先对值进行处理，如何查询条件已经存在就将新加入的查询条件合并
            if (value) {
                var valueList = $condition.val().trim().replace("，", ",").split(",");
                if (ret[name]) {
                    ret[name] = ret[name].concat(valueList);
                } else {
                    ret[name] = valueList;
                }
            }
        });
        return ret;
    }

    // 根据ID从全局变量中获取其对应的内容
    function getNameByGlobalList(globalName, itemId) {
        var result;
        $.each(GENERAL_GLOBAL_DICT[globalName], function (key, value) {
            if (value.id === itemId){
                result = value.name;
                return false;
            }
        });
        return result;
    }

    // 进入编辑模式
    function DoTrIntoEdit($tr, specialInEditFunc) {
        $tr.find("td[edit-enable='true']").each(function () {
            ExecuteTdIntoEdit($(this), specialInEditFunc);
        });
    }

    // 执行进入编辑模式
    function ExecuteTdIntoEdit($td, specialInEditFunc) {
        var editType = $td.attr("edit-type");
        if (editType === "input") {
            var text = $td.text();
            $td.addClass("padding-3");
            var htmlTag = $.CreateInput({"value": text, "class": "padding-tb-5 form-control"}, {"width": "100%"});
            $td.empty().append(htmlTag);
        } else if (editType === "select"){
            var globalName = $td.attr("global-name");
            var selectedID = $td.attr("id");
            if (specialInEditFunc){
                specialInEditFunc($td, globalName, selectedID);
            } else {
                $td.addClass("padding-3");
                var htmlTag = $.CreateSelect({"class": "padding-tb-5 form-control"}, {"width": "100%"}, GENERAL_GLOBAL_DICT[globalName], selectedID, "id", "name");
                $td.empty().append(htmlTag);
            }
        }
    }

    // 跳出编辑模式
    function DoTrOutEdit($tr, specialOutEditFunc) {
        $tr.find("td[edit-enable='true']").each(function () {
            ExecuteTdOutEdit($(this), specialOutEditFunc)
        });
    }

    // 执行跳出编辑模式
    function ExecuteTdOutEdit($td, specialOutEditFunc) {
        var editType = $td.attr("edit-type");
        if (editType === "input"){
            var text = $td.children().first().val();
            $td.removeClass("padding-3");
            $td.empty().text(text);
        } else if (editType === "select"){
            var globalName = $td.attr("global-name");
            if (specialOutEditFunc){
                specialOutEditFunc($td, globalName);
            } else {
                $td.removeClass("padding-3");
                var selecting_val = $td.children().first().val();
                var selecting_text = $td.children().first().find("option[value='" + selecting_val + "']").text();
                $td.empty().html(selecting_text);
                $td.attr("id", selecting_val);
            }
        }
    }
    
    // 绑定头部按钮事件
    function bindMenuFunction() {
        // 点击进入编辑模式按钮
        $("#edit_mode_target").click(function () {
            $.TableEditMode(this, "#tableBody", null, null);
        });
        // 点击全选按钮
        $("#check_all").click(function () {
            $.CheckAll("#tableBody", null);
        });
        // 点击取消按钮
        $("#check_cancel").click(function () {
            $.UnCheckAll("#tableBody", null);
        });
        // 点击反选按钮
        $("#check_reverse").click(function () {
            $.ReverseCheck("#tableBody", null, null);
        });
        // 点击删除按钮
        $("#do_delete").click(function () {
            $.Show("#shade, #modal_delete");
        });
        // 点击确认删除按钮
        $("#do_delete_confirm").click(function () {
            deleteData();
        });
        // 点击刷新按钮
        $("#do_refresh").click(function () {
            refreshData();
        });
        // 点击保存按钮
        $("#do_save").click(function () {
            saveData();
        });
    }

    // 删除数据
    function deleteData() {
        var id_list = [];
        $("#tableBody").find(":checkbox").each(function () {
            if ($(this).prop("checked")){
                id_list.push($(this).val());
            }
        });
        $.ajax({
            url: deleteURL,
            type: "POST",
            dataType: "JSON",
            data: {"id_list": id_list},
            traditional: true,
            success: function (response) {
                if (response.status){
                    SuccessHandleStatus(response.message);
                } else {
                    alert(response.message);
                }
                $.Hide("#shade, #modal_delete");
                refreshData();
            },
            error: function () {
                $.Hide("#shade, #modal_delete");
                alert("请求异常")
            }
        });
    }

    // 资产删除或更新成功，显示信息
    function SuccessHandleStatus(content) {
        var $handle_status = $("#handle_status");
        $handle_status.attr("style", "display: block");
        $handle_status.popover("destroy");
        var msg = "<i class='fa-check'></i>" + content;
        $handle_status.empty().removeClass("btn-danger").addClass("btn-success").html(msg);
        setTimeout(function () {
            $handle_status.empty().removeClass("btn-success btn-danger").attr("style", "display: none");
        }, 5000);
    }

    // 刷新数据
    function refreshData() {
        $("#tableBody").undelegate(":checkbox", "click");
        var currentPage = $("#pager").find("li[class='active']").text();
        initialize(currentPage);
    }
    
    // 保存数据
    function saveData() {
        // 退出编辑模式
        if ($("#edit_mode_target").hasClass("btn-warning")){
            $.TableEditMode("#edit_mode_target", "#tableBody", null, null);
        }
        // 获取被修改的数据
        var updateData = [];
        // this为tableBody下的每个tr标签
        $("#tableBody").children().each(function () {
            var rows = {};
            var nid = $(this).attr("nid");
            var num = $(this).attr("num");
            var flag = false;
            // this为每个tr标签下可以被编辑的td标签
            $(this).children("td[edit-enable='true']").each(function () {
                // 原始值
                var origin = $(this).attr("origin");
                if (origin === undefined){
                    origin = "";
                }
                var name = $(this).attr("name");
                var newer;
                // td标签edit-type属性为input
                if ($(this).attr("edit-type") === "input"){
                    newer = $(this).text();
                    if (newer === undefined){
                        newer = "";
                    }
                // td标签edit-type属性为select
                } else if ($(this).attr("edit-type") === "select"){
                    newer = $(this).attr("id");
                    if (newer === undefined){
                        newer = "";
                    }
                }
                // 值与原始值不相等
                if (origin !== newer){
                    rows[name] = newer;
                    flag = true;
                }
            });
            if (flag) {
                rows["nid"] = nid;
                rows["num"] = num;
                updateData.push(rows);
            }
        });
        // 如果更新列表中无数据，则不执行后面的ajax提交
        if (updateData.length < 1) {
            return;
        }
        updateData = JSON.stringify(updateData);
        $.ajax({
            url: updateURL,
            type: "POST",
            dataType: "JSON",
            data: {"update_list": updateData},
            success: function (response) {
                if (response.status) {
                    SuccessHandleStatus(response.message);
                } else {
                    ErrorHandleStatus(response.message, response.error);
                }
                refreshData();
            },
            error: function () {
                alert("请求异常");
            }
        });
    }

    // 资产更新失败，显示错误信息
    function ErrorHandleStatus(content, errorList) {
        var $handle_status = $("#handle_status");
        $handle_status.attr("style", "display: block");
        $handle_status.attr("data-toggle", "popover");
        var errorStr = "";
        $.each(errorList, function (key, value) {
            errorStr = errorStr + value.num + "." + value.message + "</br>"
        });
        $handle_status.attr("data-content", errorStr);
        $handle_status.popover();
        var msg = "<i class='fa fa-info-circle'></i>>" + "&nbsp;" + content;
        $handle_status.empty().removeClass("btn-success").addClass("btn-danger").html(msg);
    }
    
    // 绑定搜索条件事件
    function bindSearchCondition() {
        // 绑定修改条件之后的事件
        bindChangeSearchCondition();
        // 绑定提交搜索事件
        bindSubmitSearchCondition();
    }
    
    // 绑定修改条件之后的事件
    function bindChangeSearchCondition() {
        $("#search_condition").find("ul").delegate("li", "click", function () {
            var name = $(this).attr("name");
            var text = $(this).text();
            var condition_type = $(this).attr("condition-type");
            var global_name = $(this).attr("global-name");
            var tag;
            if (condition_type === "input"){
                tag = $.CreateInput(
                    {
                        "is-condition": "true",
                        "class": "form-control",
                        "name": name,
                        "placeholder": "逗号分割多条件"
                    },
                    {}
                );
            } else if (condition_type === "select"){
                tag = $.CreateSelect(
                    {
                        "is-condition": "true",
                        "class": "form-control",
                        "name": name
                    },
                    {},
                    GENERAL_GLOBAL_DICT[global_name],
                    null,
                    "id",
                    "name"
                );
            }
            var $current = $(this).parent().parent();
            $current.children().first().text(text);
            $current.next().remove();
            $current.after(tag);
        });
    }

    // 绑定搜索提交按钮
    function bindSubmitSearchCondition() {
        $("#search_condition_submit").click(function () {
            $("#tableBody").undelegate(":checkbox", "click");
            initialize(1);
        });
    }

    // 监听是否已经按下control键
    window.globalCtrlKeyPress = false;
    window.onkeydown = function (event) {
        if (event && event.keyCode == 17) {
            window.globalCtrlKeyPress = true;
        }
    };

    window.onkeyup = function (event) {
        if (event && event.keyCode == 17) {
            window.globalCtrlKeyPress = false;
        }
    };

    // 按下Control，联动表格中正在编辑的select
    function bindMultiSelect() {
        $('#tableBody').delegate('select', 'change', function () {
            if (window.globalCtrlKeyPress) {
                var index = $(this).parent().index();
                var value = $(this).val();
                $(this).parent().parent().nextAll().find("td input[type='checkbox']:checked").each(function () {
                    $(this).parent().parent().children().eq(index).children().val(value);
                });
            }
        });
    }

    jq.extend({
        // 显示等待特效
        "Show": function (target) {
            $(target).removeClass("hide");
        },

        // 隐藏等待特效
        "Hide": function (target) {
            $(target).addClass("hide");
        },

        // 创建input标签
        "CreateInput": function (attrs, csses) {
            var obj = document.createElement("input");
            $.each(attrs, function (key, value) {
                $(obj).attr(key, value);
            });
            $.each(csses, function (key, value) {
                $(obj).css(key, value);
            });
            return obj;
        },

        // 创建select标签
        "CreateSelect": function (attrs, csses, globalData, currentValue, keyValue, keyText) {
            var sel = document.createElement("select");
            $.each(attrs, function (key, value) {
                $(sel).attr(key, value);
            });
            $.each(csses, function (key, value) {
                $(sel).css(key, value);
            });
            /*
            [{'id': 'online', 'name': '在线'}, {'id': 'offline', 'name': '离线'}]
             */
            $.each(globalData, function (key, value) {
                var opt = document.createElement("option");
                var opt_text = value[keyText];
                var opt_value = value[keyValue];
                if (opt_value === parseInt(currentValue)) {
                    $(opt).text(opt_text).attr("value", opt_value).attr("text", opt_text).appendTo($(sel));
                    $(opt).prop("selected", true);

                } else if (opt_value === null){
                    opt_value = "";
                    opt_text = "";
                    $(opt).text(opt_text).attr("value", opt_value).attr("text", opt_text).appendTo($(sel));
                    $(opt).prop("selected", true);
                } else if (opt_value === currentValue) {
                    $(opt).text(opt_text).attr("value", opt_value).attr("text", opt_text).appendTo($(sel));
                    $(opt).prop("selected", true);
                } else {
                    $(opt).text(opt_text).attr("value", opt_value).attr("text", opt_text).appendTo($(sel));
                }
            });
            return sel;
        },

        // 绑定点击CheckBox事件，targetContainer表格中body选择器对象，specialInEditFunc，specialOutEditFunc
        "BindDoSingleCheck": function (tableBody, specialInEditFunc, specialOutEditFun) {
            $(tableBody).delegate(":checkbox", "click", function () {
                var $tr = $(this).parent().parent();
                if ($(this).prop("checked")){
                    if ($(tableBody).attr("edit-mode") === "true"){
                        // 进入编辑模式
                        $tr.addClass("success");
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                } else {
                    if ($(tableBody).attr("edit-mode") === "true"){
                        // 跳出编辑模式
                        $tr.removeClass("success");
                        DoTrOutEdit($tr, specialOutEditFun);
                    }
                }
            });
        },

        // 表格进入编辑模式，ths表示点击按钮，body表格中的body选择器对象
        "TableEditMode": function (ths, body, specialInEditFunc, specialOutEditFunc) {
            // 处于编辑模式点击退出
            if ($(ths).hasClass("btn-warning")) {
                $(ths).removeClass("btn-warning").find("span").text("进入编辑模式");
                $(body).attr("edit-mode", "false");
                $(body).children().removeClass("success");
                $(body).find(":checkbox").each(function () {
                    var check = $(this).prop("checked");
                    var $tr = $(this).parent().parent();
                    if (check){
                        $tr.removeClass("success");
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }
                });
            // 处于非编辑模式点击进入
            } else {
                $(ths).addClass("btn-warning").find("span").text("退出编辑模式");
                $(body).attr("edit-mode", "true");
                $(body).find(":checkbox").each(function () {
                    var check = $(this).prop("checked");
                    var $tr = $(this).parent().parent();
                    if (check){
                        $tr.addClass("success");
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                });
            }
        },

        // 全选
        "CheckAll": function (tableBody, specialInEditFunc) {
            // 处于编辑模式
            if ($(tableBody).attr("edit-mode") === "true"){
                $(tableBody).find(":checkbox").each(function () {
                    var check = $(this).prop("checked");
                    var disabled = $(this).prop("disabled");
                    var $tr = $(this).parent().parent();
                    if (!check && !disabled){
                        $tr.addClass("success");
                        $(this).prop("checked", true);
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                });
            // 处于非编辑模式
            } else {
                $(tableBody).find(":checkbox").each(function () {
                    var disabled = $(this).prop("disabled");
                    if (!disabled){
                        $(this).prop("checked", true);
                    }
                });
            }
        },
        
        // 取消
        "UnCheckAll": function (tableBody, specialOutEditFunc) {
            // 处于编辑模式
            if ($(tableBody).attr("edit-mode") === "true"){
                $(tableBody).find(":checkbox").each(function () {
                    var check = $(this).prop("checked");
                    var $tr = $(this).parent().parent();
                    if (check){
                        $tr.removeClass("success");
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }
                });
            }
            $(tableBody).find(":checkbox").prop("checked", false);
        },

        // 反选
        "ReverseCheck": function (tableBody, specialInEditFunc, specialOutEditFunc) {
            $(tableBody).find(":checkbox").each(function () {
                var check = $(this).prop("checked");
                var disabled = $(this).prop("disabled");
                var $tr = $(this).parent().parent();
                // 选中的CheckBox
                if (check){
                    $(this).prop("checked", false);
                    // 处于编辑模式
                    if ($(tableBody).attr("edit-mode") === "true"){
                        $tr.removeClass("success");
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }
                // 未选中的CheckBox
                } else {
                    if (!disabled){
                        $(this).prop("checked", true);
                    }
                    // 处于编辑模式
                    if ($(tableBody).attr("edit-mode") === "true" && !disabled){
                        $tr.addClass("success");
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                }
            });
        },

        // 搜索插件 -> 添加搜索条件 ths:点击的当前对象
        "AddSearchCondition": function (ths) {
            var $duplicate = $(ths).parent().parent().clone(true);
            $duplicate.find(".im-plus").addClass("im-minus").removeClass("im-plus");
            $duplicate.find("a[onclick='$.AddSearchCondition(this)']").attr("onclick", "$.RemoveSearchCondition(this)");
            $duplicate.appendTo($(ths).parent().parent().parent());
        },

        // 搜索插件 -> 移除当前搜索条件 ths:点击的当前对象
        "RemoveSearchCondition": function (ths) {
            $(ths).parent().parent().remove();
        },

        // 自执行函数
        "GeneralData": function (request_url, delete_url, update_url) {
            requestURL = request_url;
            deleteURL = delete_url;
            updateURL = update_url;
            // 初始化
            initialize(1);
            // 绑定菜单
            bindMenuFunction();
            // 绑定联动
            bindMultiSelect();
            // 绑定搜索
            bindSearchCondition();
        },

        // 分页
        "changePage": function (pageNum) {
            $("#tableBody").undelegate(":checkbox", "click");
            initialize(pageNum);
        }
    });
})(jQuery);