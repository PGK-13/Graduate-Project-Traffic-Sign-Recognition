package com.tsr.controller;

import com.tsr.model.RecognitionRecord;
import com.tsr.service.RecognitionService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class ApiController {
    
    private final RecognitionService recognitionService;
    
    public ApiController(RecognitionService recognitionService) {
        this.recognitionService = recognitionService;
    }
    
    /**
     * 上传图像并识别
     */
    @PostMapping("/image/upload")
    public ResponseEntity<Map<String, Object>> uploadImage(
            @RequestParam("file") MultipartFile file,
            HttpServletRequest request) {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // 获取客户端 IP 地址
            String ipAddress = request.getRemoteAddr();
            
            // 处理图像
            Map<String, Object> result = recognitionService.processImage(file, ipAddress);
            
            response.put("success", true);
            response.put("data", result);
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
        }
    }
    
    /**
     * 获取识别记录列表
     */
    @GetMapping("/record/list")
    public ResponseEntity<Map<String, Object>> getRecordList(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // 构建分页参数
            Pageable pageable = PageRequest.of(
                    page, 
                    size, 
                    Sort.by(Sort.Direction.DESC, "uploadTime")
            );
            
            // 获取记录
            Page<RecognitionRecord> records = recognitionService.getRecords(pageable);
            
            response.put("success", true);
            response.put("data", records.getContent());
            response.put("total", records.getTotalElements());
            response.put("page", page);
            response.put("size", size);
            response.put("pages", records.getTotalPages());
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    /**
     * 获取统计概览
     */
    @GetMapping("/statistic/overview")
    public ResponseEntity<Map<String, Object>> getStatisticOverview() {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Map<String, Object> statistics = recognitionService.getOverviewStatistics();
            
            response.put("success", true);
            response.put("data", statistics);
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    /**
     * 获取类别分布
     */
    @GetMapping("/statistic/class-distribution")
    public ResponseEntity<Map<String, Object>> getClassDistribution() {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            List<Map<String, Object>> distribution = recognitionService.getClassDistribution();
            
            response.put("success", true);
            response.put("data", distribution);
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
}
