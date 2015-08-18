
function previewImg(input) {
    // 服务器上有的图片位置
    var $pre_a = $(input).prevAll('a');
    // 放置没有上传前的预览图片的位置
    var preview = $(input).prev('div').get(0);
    while (preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }
    if (input.files && input.files[0]) {
        // 如果选择了文件则要移除原有的图片
        $pre_a.remove();

        var reader = new FileReader();

        var img = document.createElement('img');
        reader.onload = function(e) {
            img.setAttribute('src', e.target.result);
            img.style.height = '100%';
            img.style.width = '100%';
            preview.appendChild(img);
        };
        reader.readAsDataURL(input.files[0]);

    } else {
        preview.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = input.value;

    }
    // 本来div是隐藏的， 所以这里要显示预览div
    $(input).prev('div').show();
}

// function previewImg(input) {
//     // 兼容IE、Chrome、FF的图片上传前预览
//     // 参考 http://www.calledt.com/previrew-image-before-upload/
//     var preview = document.getElementById('preview');

//     // while (preview.firstChild) {
//     //     preview.removeChild(preview.firstChild);
//     // }

//     if (input.files && input.files[0]) {
//         var reader = new FileReader();

//         var img = document.createElement('img');
//         reader.onload = function(e) {
//             img.setAttribute('src', e.target.result);
//             img.style.height = '100%';
//             img.style.width = '100%';
//             preview.appendChild(img);
//         };
//         reader.readAsDataURL(input.files[0]);

//     } else {

//         preview.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = input.value;

//     }
// }

