function initChart() {
    //
    $.ajax({
        url: '/cmdb_web/dashboard_chart1.html',
        type: "GET",
        dataType: "JSON",
        success: function (response) {
            if (response.status) {
                var asset_count = parseInt(response.data.asset_count);
                var idc_count = parseInt(response.data.idc_count);
                var business_unit_count = parseInt(response.data.business_unit_count);
                var tag_count = parseInt(response.data.tag_count);
                var user_count = parseInt(response.data.user_count);

                var chart1; // 全局变量
                chart1 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container-chart1',
                        type: 'column',
                        options3d: {
                            enabled: true,
                            alpha: 10,
                            beta: 25,
                            depth: 75
                        },
                        backgroundColor: null,
                        frame: {
                            bottom: {
                                size: 1,
                                color: 'transparent'
                            },
                            side: {
                                size: 1,
                                color: 'transparent'
                            },
                            back: {
                                size: 1,
                                color: 'transparent'
                            }
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: '总览'
                    },
                    subtitle: {
                        text: ''
                    },
                    plotOptions: {
                        column: {
                            depth: 35
                        }
                    },
                    xAxis: {
                        categories: ['类型']
                    },
                    yAxis: {
                        allowDecimals: true,
                        title: {
                            text: '数量'
                        }
                    },
                    series: [
                        {name: '资产', data: [asset_count]},
                        {name: 'IDC', data: [idc_count]},
                        {name: '业务线', data: [business_unit_count]},
                        {name: '标签', data: [tag_count]},
                        {name: '用户', data: [user_count]}
                    ]
                });
            } else {

            }
        },
        error: function () {

        }
    });

    //
    $.ajax({
        url: '/cmdb_web/dashboard_chart2.html',
        type: "GET",
        dataType: "JSON",
        success: function (response) {
            if (response.status) {
                var hardware_server_count = response.data.hardware_server_count;
                var software_server_count = response.data.software_server_count;
                var switch_device_count = response.data.switch_device_count;
                var firewall_device_count = response.data.firewall_device_count;
                var security_device_count = response.data.security_device_count;

                var chart1; // 全局变量
                chart1 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container-chart2',
                        type: 'column',
                        options3d: {
                            enabled: true,
                            alpha: 10,
                            beta: 25,
                            depth: 70
                        },
                        backgroundColor: null,
                        frame: {
                            bottom: {
                                size: 1,
                                color: 'transparent'
                            },
                            side: {
                                size: 1,
                                color: 'transparent'
                            },
                            back: {
                                size: 1,
                                color: 'transparent'
                            }
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: '设备总览'
                    },
                    subtitle: {
                        text: ''
                    },
                    plotOptions: {
                        column: {
                            depth: 35
                        }
                    },
                    xAxis: {
                        categories: ['设备类型']
                    },
                    yAxis: {
                        allowDecimals: true,
                        title: {
                            text: '数量'
                        }
                    },
                    series: [
                        {name: '硬件服务器', data: [hardware_server_count]},
                        {name: '软件服务器', data: [software_server_count]},
                        {name: '交换机', data: [switch_device_count]},
                        {name: '防火墙', data: [firewall_device_count]},
                        {name: '安全设备', data: [security_device_count]}
                    ]
                });
            } else {

            }
        },
        error: function () {

        }
    });
}