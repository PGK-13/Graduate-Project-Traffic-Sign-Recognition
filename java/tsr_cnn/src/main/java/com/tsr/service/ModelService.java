package com.tsr.service;

import com.tsr.util.ImageProcessor;
import com.tsr.util.TrafficSignUtil;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@Service
public class ModelService implements DisposableBean {
    
    private RestTemplate restTemplate;
    
    // Flask 服务地址
    private static final String FLASK_SERVICE_URL = "http://localhost:5001";
    private static final String PREDICT_ENDPOINT = FLASK_SERVICE_URL + "/predict";
    private static final String HEALTH_ENDPOINT = FLASK_SERVICE_URL + "/health";
    
    /**
     * 初始化服务
     */
    public void initialize() {
        restTemplate = new RestTemplate();
        
        // 健康检查
        try {
            Map<String, Object> healthStatus = restTemplate.getForObject(HEALTH_ENDPOINT, Map.class);
            System.out.println("Flask服务健康状态: " + healthStatus);
        } catch (Exception e) {
            System.err.println("Flask服务健康检查失败: " + e.getMessage());
        }
    }
    
    /**
     * 执行模型推理
     */
    public Map<String, Object> predict(BufferedImage image) throws Exception {
        if (restTemplate == null) {
            initialize();
        }
        
        // 将图像转换为字节数组
        byte[] imageBytes = imageToBytes(image);
        
        // 构建文件上传请求
        MultiValueMap<String, Object> params = new LinkedMultiValueMap<>();
        params.add("file", new ByteArrayResource(imageBytes) {
            @Override
            public String getFilename() {
                return "image.jpg";
            }
        });
        
        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        // 创建请求实体
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(params, headers);
        
        // 调用 Flask 服务
        Map<String, Object> response = restTemplate.postForObject(PREDICT_ENDPOINT, requestEntity, Map.class);
        
        // 处理响应
        if (response != null) {
            System.out.println("Flask服务响应: " + response);
            if (response.containsKey("success") && (Boolean) response.get("success")) {
                Map<String, Object> data = (Map<String, Object>) response.get("prediction");
                if (data != null) {
                    System.out.println("原始预测结果: " + data);
                    
                    // 转换字段名称以匹配我们的期望
                    Map<String, Object> transformedData = new HashMap<>();
                    transformedData.put("predictedClass", data.get("class_id"));
                    transformedData.put("className", data.get("class_name"));
                    transformedData.put("confidence", data.get("confidence"));
                    
                    System.out.println("转换后预测结果: " + transformedData);
                    return transformedData;
                } else {
                    System.out.println("预测结果为null");
                }
            } else {
                System.out.println("Flask服务返回失败: " + response.get("error"));
            }
        } else {
            System.out.println("Flask服务响应为null");
        }
        
        // 如果响应失败，抛出异常
        throw new Exception("模型推理失败: " + (response != null ? response.get("error") : "未知错误"));
    }
    
    /**
     * 将 BufferedImage 转换为字节数组
     */
    private byte[] imageToBytes(BufferedImage image) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(image, "jpg", baos);
        return baos.toByteArray();
    }
    
    /**
     * 字节数组资源类，用于文件上传
     */
    private static class ByteArrayResource extends org.springframework.core.io.ByteArrayResource {
        public ByteArrayResource(byte[] byteArray) {
            super(byteArray);
        }
        
        @Override
        public String getFilename() {
            return "image.jpg";
        }
    }
    

    
    /**
     * 销毁资源
     */
    @Override
    public void destroy() {
        // 无需关闭任何资源，RestTemplate 会自动管理
        System.out.println("ModelService 资源已释放");
    }
}
