$(function() {
	//提示框初始化参数
	toastr.options = {
		"closeButton": true, //是否显示关闭按钮
		"debug": false,
		"newestOnTop": false,
		"progressBar": false, //是否显示进度条
		"positionClass": "toast-top-right", //显示位置 顶端右边
		"preventDuplicates": false,
		"onclick": null,
		"showDuration": "300", //显示动作时间 
		"hideDuration": "1000", //隐藏动作时间 
		"timeOut": "5000", //自动关闭超时时间 
		"extendedTimeOut": "1000",
		"showEasing": "swing",
		"hideEasing": "linear",
		"showMethod": "fadeIn",
		"hideMethod": "fadeOut"
    };
    
});
/*弹出层*/
/*
    参数解释：
    title   标题
    url     请求的url
    id      需要操作的数据id
    w       弹出层宽度（缺省调默认值）
    h       弹出层高度（缺省调默认值）
*/
function layui_show(title,url,w,h){
    
    if (title == null || title == '') {
        title=false;
    };
    if (url == null || url == '') {
        url="404.html";
    };
    if (w == null || w == '') {
        //w=($(window).width()*0.9);
        w='800'
    };
    if (h == null || h == '') {
        //h=($(window).height() - 50);
        h='600'
    };
    var area = [$(window).width() > w ? w +'px' : '95%', $(window).height() > w ? h +'px' : '95%'];
    layer.open({
        type: 2, //0（信息框，默认）1（页面层）2（iframe层）3（加载层）4（tips层）
        //area: [w+'px', h +'px'],
        area: area,
        fix: false, //不固定
        maxmin: true,
        moveOut: true,
        shadeClose: true,
        shade: false, //遮罩，使用遮罩更改为shade: 0.4
        title: title,
        content: url,
        zIndex: layer.zIndex,
        skin: 'layui-layer-noborder',
        success: function (layero, index) {
            var that = this;
            //置顶当前窗口
            layer.setTop(layero);
        }
    });
}

/*关闭弹出框口*/
function layui_close(){
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
}

function apiAjax(url, data){
    /*post提交方法,用于添加，编辑操作
    */
    $.ajax({
        url: url,
        type: 'POST',
        dataType: "json",
        data: data,
        success: function (d) {
            if (d.hasOwnProperty("code")) {
                if (d.code == 1) {
                    layui_close()
                    parent.toastr.success("操作成功");
                    parent.$('.btn-refresh').click();

                } else {
                    toastr.error(d.msg);
                }
            } else {
                toastr.error('未知的数据格式!');
            }
        },
        error: function () {
            toastr.error('网络错误，请重试');
        }
    });
}

function fileAjax(url, data){
    /*post提交方法,用于添加，编辑操作
    */
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        async: false,  
        cache: false,  
        contentType: false,  
        processData: false, 
        success: function (d) {
            if (d.hasOwnProperty("code")) {
                if (d.code == 1) {
                    layui_close()
                    parent.toastr.success("操作成功");
                    parent.$('.btn-refresh').click();

                } else {
                    toastr.error(d.msg);
                }
            } else {
                toastr.error('未知的数据格式!');
            }
        },
        error: function () {
            toastr.error('网络错误，请重试');
        }
    });
}

//获取bootstrap-table选择行
function selectedids(table) {
	var options = table.bootstrapTable('getOptions');
	if (options.templateView) {
		return $.map($("input[data-id][name='checkbox']:checked"), function (dom) {
			return $(dom).data("id");
		});
	} else {
		return $.map(table.bootstrapTable('getSelections'), function (row) {
			return row[options.pk];
		});
	}
};

//For getting CSRF token
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
