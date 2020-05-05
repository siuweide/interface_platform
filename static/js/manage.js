
function SelectInit() {
    console.log('初始化下拉框');
    cmbProject = document.getElementById("projectsList");
    cmbModule = document.getElementById("modulesList");

    var dataList = [];

    // 创建下拉选项
    function addOption(cmb, obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.id;
        console.log('option------->', option)
    }

    // 改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        console.log("项目默认选项的索引", cmbProject.selectedIndex);
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        console.log("这个才是真的项目ID", pid)

        for (var i = 0; i < dataList.length; i++) {
            if (dataList[i].id == pid) {
                var modules = dataList[i].moduleList;
                for (j = 0; j < modules.length; j++) {
                    addOption(cmbModule, modules[j])
                }
            }
        }

    }

    function getSelectData() {
        // 调用获取select数据列表
        $.get("/api/get_select_data/", {},  function (resp) {
            if (resp.status == 10200) {
                dataList = resp.data;
                // 遍历项目
                for (var i = 0; i < dataList.length; i++) {
                    console.log("每一个项目的数据", dataList[i]);
                    addOption(cmbProject, dataList[i]);

                    changeProject()
                    cmbProject.onchange = changeProject;
                }
            }
        })
    }
    getSelectData()
}
