//* Done 选择不同输入设备源
// https://developer.mozilla.org/zh-CN/docs/Web/API/MediaDevices/enumerateDevices

/**
 * 返回相机的名称和id（打开摄像头后再调用
 * 如果不支持，则返回null
 * 
 * returns:
 * {
 *     label: 设备名
 *     deviceId: 设备id
 * }
 */
function getDevices () {
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
        log("不支持 enumerateDevices()");
        return null;
        // alert("不支持 enumerateDevices()");
    } else {
        navigator.mediaDevices.enumerateDevices()
            .then(function (devices) {
    
    
                let i = 1;
                let videoDevices = []
                devices.forEach((device) => {
                    if (device.kind == "videoinput") {
                        videoDevices.push({
                            "label": device.label,
                            "deviceId": device.deviceId,
                        })
                        opt.text = i + '. ' + device.label;
                        opt.value = device.deviceId;
                        select.appendChild(opt);
                        log("添加设备 " + i + '. ' + device.kind + ": " + device.label + ",<br>id = " + device.deviceId + ".");
                        i += 1;
                    }
                });
                
                if (DEBUG.add_test_device) {
                    videoDevices.push({
                        "label": "test",
                        "deviceId": "test"
                    })
                }

                return videoDevices;
            })
            .catch(function (err) {
                log("enumerateDevices()时发生错误。" + err);
                return null;
            });
    }
    
}

/**
 * 把相机信息加入到下拉菜单中。
 */
function insertToSelect(videoDevices) {
    let select = document.getElementById("devices");
    videoDevices.forEach((device, index) => {
        let opt = document.createElement("option");
        opt.text = index + '. ' + device.label;
        opt.value = device.deviceId;
        select.appendChild(opt);
        log("添加设备 " + index + '. ' + device.kind + ": " + device.label + ",<br>id = " + device.deviceId + ".");
    })
    
    log("当前设备：" + select.selectedOptions[0].text);
    updateConstraints(select.selectedOptions[0].value);

    // 渲染下拉菜单到页面
    document.getElementById("devicesWrapper").append(select);

}