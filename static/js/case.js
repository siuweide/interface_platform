
function get_api_info() {
    var url = window.location.href;
    var aid = url.split("/")[5];
    $.get("/api/get_api_info/", {
        aid:aid,
    }, function (resp) {
        if (resp.status == 10200) {
            // name
            document.querySelector('#req_name').value = resp.data.name;
            // url
            document.querySelector('#req_url').value = resp.data.url;
            // 方法
            document.getElementById("req_method").value = resp.data.method;
            // par_type
            if(resp.data.req_type == "form"){
                document.querySelector("#form").setAttribute("checked", "");
            }else if(resp.data.req_type == "json"){
                document.querySelector("#json").setAttribute("checked", "");
            }
            // header
            var header_json = JSON.parse(resp.data.header);
            headersEditor.set(header_json);
            // cookie
            if(resp.data.is_cookie == "yes"){
                document.querySelector("#yes").setAttribute("checked", "");
            }else if(resp.data.is_cookie == "no"){
                document.querySelector("#no").setAttribute("checked", "");
            }
            // body
            var par_json = JSON.parse(resp.data.req_body);
            parameterEditor.set(par_json);
            // assert_type
            if(resp.data.assert_type == "include"){
                document.querySelector("#include").setAttribute("checked", "");
            }else if(resp.data.assert_type == "equal"){
                document.querySelector("#equal").setAttribute("checked", "");
            }
            // assert_body
            document.querySelector('#assert_content').value = resp.data.assert_body;
            // assert_result
            document.getElementById("assert_result").value = resp.data.assert_result;
            // response
            document.getElementById("result").value = resp.data.response_result;
            // 项目
            document.getElementById("projectsList").value = resp.data.project_id;
            // 模块
            document.getElementById("modulesList").value = resp.data.module;
            // 接口用例类型
            if(resp.data.api_type == "1"){
                document.querySelector("#single").setAttribute("checked", "");
            }else if(resp.data.api_type == "2"){
                document.querySelector("#multiple").setAttribute("checked", "");
            }else if(resp.data.api_type == "3") {
                document.querySelector("#common").setAttribute("checked", "");
            }
            //key、value
            if(resp.data.api_key) {
                document.querySelector('#variable_key').value = resp.data.api_key;
            }
            if(resp.data.api_extract_value) {
                document.querySelector('#variable_extract_value').value = resp.data.api_extract_value;
            }
        }
    })
}