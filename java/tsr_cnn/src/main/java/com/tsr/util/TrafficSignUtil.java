package com.tsr.util;

import java.util.HashMap;
import java.util.Map;

public class TrafficSignUtil {
    
    // 交通标志类别映射
    private static final Map<Integer, String> CLASS_NAME_MAP = new HashMap<>();
    
    static {
        // 这里根据实际的交通标志类别进行配置
        // 示例类别，实际项目中需要根据训练数据进行调整
        CLASS_NAME_MAP.put(0, "限速 20km/h");
        CLASS_NAME_MAP.put(1, "限速 30km/h");
        CLASS_NAME_MAP.put(2, "限速 50km/h");
        CLASS_NAME_MAP.put(3, "限速 60km/h");
        CLASS_NAME_MAP.put(4, "限速 70km/h");
        CLASS_NAME_MAP.put(5, "限速 80km/h");
        CLASS_NAME_MAP.put(6, "解除限速 80km/h");
        CLASS_NAME_MAP.put(7, "限速 100km/h");
        CLASS_NAME_MAP.put(8, "限速 120km/h");
        CLASS_NAME_MAP.put(9, "禁止超车");
        CLASS_NAME_MAP.put(10, "大型车辆禁止超车");
        CLASS_NAME_MAP.put(11, "前方路口优先通行");
        CLASS_NAME_MAP.put(12, "路口优先通行");
        CLASS_NAME_MAP.put(13, "让行");
        CLASS_NAME_MAP.put(14, "停车让行");
        CLASS_NAME_MAP.put(15, "禁止通行");
        CLASS_NAME_MAP.put(16, "禁止机动车通行");
        CLASS_NAME_MAP.put(17, "禁止大型客车通行");
        CLASS_NAME_MAP.put(18, "禁止驶入");
        CLASS_NAME_MAP.put(19, "危险");
        CLASS_NAME_MAP.put(20, "道路施工");
        CLASS_NAME_MAP.put(21, "注意交通信号灯");
        CLASS_NAME_MAP.put(22, "注意行人");
        CLASS_NAME_MAP.put(23, "注意儿童");
        CLASS_NAME_MAP.put(24, "注意牲畜");
        CLASS_NAME_MAP.put(25, "注意前方落石");
        CLASS_NAME_MAP.put(26, "注意侧风");
        CLASS_NAME_MAP.put(27, "下坡危险");
        CLASS_NAME_MAP.put(28, "弯道危险");
        CLASS_NAME_MAP.put(29, "连续弯道");
        CLASS_NAME_MAP.put(30, "路面湿滑");
        CLASS_NAME_MAP.put(31, "道路狭窄");
        CLASS_NAME_MAP.put(32, "注意野生动物");
        CLASS_NAME_MAP.put(33, "解除禁止超车");
        CLASS_NAME_MAP.put(34, "解除大型车辆禁止超车");
        CLASS_NAME_MAP.put(35, "直行");
        CLASS_NAME_MAP.put(36, "直行或右转");
        CLASS_NAME_MAP.put(37, "直行或左转");
        CLASS_NAME_MAP.put(38, "右转");
        CLASS_NAME_MAP.put(39, "左转");
        CLASS_NAME_MAP.put(40, "环岛行驶");
        CLASS_NAME_MAP.put(41, "左侧车道行驶");
        CLASS_NAME_MAP.put(42, "右侧车道行驶");
        CLASS_NAME_MAP.put(43, "减速让行");
    }
    
    /**
     * 根据类别 ID 获取类别名称
     */
    public static String getClassName(int classId) {
        return CLASS_NAME_MAP.getOrDefault(classId, "未知类别");
    }
    
    /**
     * 获取所有类别信息
     */
    public static Map<Integer, String> getAllClasses() {
        return CLASS_NAME_MAP;
    }
}
