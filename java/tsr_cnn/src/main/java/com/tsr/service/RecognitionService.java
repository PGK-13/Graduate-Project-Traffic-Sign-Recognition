package com.tsr.service;

import com.tsr.model.RecognitionRecord;
import com.tsr.repository.RecognitionRecordRepository;
import com.tsr.util.FileUtil;
import com.tsr.util.ImageProcessor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
public class RecognitionService {
    
    private final ModelService modelService;
    private final RecognitionRecordRepository repository;
    
    @Value("${app.image.storage-path}")
    private String storagePath;
    
    public RecognitionService(ModelService modelService, RecognitionRecordRepository repository) {
        this.modelService = modelService;
        this.repository = repository;
    }
    
    /**
     * 处理图像上传和识别
     */
    public Map<String, Object> processImage(MultipartFile file, String ipAddress) throws Exception {
        // 验证文件
        if (!FileUtil.isValidImageFile(file)) {
            throw new IllegalArgumentException("无效的图像文件");
        }
        
        // 读取图像
        BufferedImage image = ImageIO.read(file.getInputStream());
        
        // 验证图像
        if (!ImageProcessor.isValidImage(image)) {
            throw new IllegalArgumentException("无效的图像");
        }
        
        // 执行模型推理
        Map<String, Object> prediction = modelService.predict(image);
        
        // 保存图像
        String fileName = FileUtil.generateUniqueFileName(file.getOriginalFilename());
        
        // 使用绝对路径
        File uploadDir = new File(System.getProperty("user.dir"), storagePath);
        if (!uploadDir.exists()) {
            uploadDir.mkdirs();
        }
        
        File filePath = new File(uploadDir, fileName);
        
        // 保存文件
        file.transferTo(filePath);
        
        // 保存识别记录
        RecognitionRecord record = new RecognitionRecord();
        record.setImagePath(fileName);
        
        // 获取预测类别
        Object predictedClassObj = prediction.get("predictedClass");
        Integer predictedClass = null;
        if (predictedClassObj instanceof Integer) {
            predictedClass = (Integer) predictedClassObj;
        } else if (predictedClassObj instanceof String) {
            try {
                predictedClass = Integer.parseInt((String) predictedClassObj);
            } catch (NumberFormatException e) {
                System.out.println("预测类别转换失败: " + e.getMessage());
            }
        }
        System.out.println("预测类别: " + predictedClass);
        record.setPredictedClass(predictedClass != null ? predictedClass : 0);
        
        // 优先通过 TrafficSignUtil 获取中文类别名称
        String className = null;
        if (predictedClass != null) {
            className = com.tsr.util.TrafficSignUtil.getClassName(predictedClass);
            System.out.println("通过 TrafficSignUtil 获取的中文类别名称: " + className);
        }
        
        // 如果没有获取到，再使用 Flask 服务返回的名称
        if (className == null || "未知类别".equals(className)) {
            className = (String) prediction.get("className");
            System.out.println("使用 Flask 服务返回的类别名称: " + className);
        }
        
        String finalClassName = className != null ? className : "未知类别";
        System.out.println("最终类别名称: " + finalClassName);
        record.setClassName(finalClassName);
        
        // 获取置信度
        Object confidenceObj = prediction.get("confidence");
        Double confidence = null;
        if (confidenceObj instanceof Double) {
            confidence = (Double) confidenceObj;
        } else if (confidenceObj instanceof Float) {
            confidence = ((Float) confidenceObj).doubleValue();
        } else if (confidenceObj instanceof String) {
            try {
                confidence = Double.parseDouble((String) confidenceObj);
            } catch (NumberFormatException e) {
                System.out.println("置信度转换失败: " + e.getMessage());
            }
        }
        System.out.println("置信度: " + confidence);
        Double finalConfidence = confidence != null ? confidence : 0.0;
        System.out.println("最终置信度: " + finalConfidence);
        record.setConfidence(finalConfidence);
        
        LocalDateTime now = LocalDateTime.now();
        System.out.println("上传时间: " + now);
        record.setUploadTime(now);
        
        System.out.println("IP地址: " + ipAddress);
        record.setIpAddress(ipAddress);
        
        System.out.println("准备保存记录: " + record);
        try {
            repository.save(record);
            System.out.println("记录保存成功");
        } catch (Exception e) {
            System.out.println("记录保存失败: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
        
        // 更新预测结果中的类别名称为中文
        prediction.put("className", finalClassName);
        // 添加图像路径到结果
        prediction.put("imagePath", storagePath + fileName);
        prediction.put("recordId", record.getId());
        
        return prediction;
    }
    
    /**
     * 获取识别记录列表
     */
    public Page<RecognitionRecord> getRecords(@NonNull Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    /**
     * 获取类别分布统计
     */
    public List<Map<String, Object>> getClassDistribution() {
        return repository.getClassDistribution();
    }
    
    /**
     * 获取统计概览
     */
    public Map<String, Object> getOverviewStatistics() {
        return repository.getOverviewStatistics();
    }
}
