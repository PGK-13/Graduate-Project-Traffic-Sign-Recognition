package com.tsr.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "recognition_record")
public class RecognitionRecord {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "image_path", nullable = false)
    private String imagePath;
    
    @Column(name = "predicted_class", nullable = false)
    private Integer predictedClass;
    
    @Column(name = "class_name", nullable = false)
    private String className;
    
    @Column(name = "confidence", nullable = false)
    private Double confidence;
    
    @Column(name = "upload_time", nullable = false)
    private LocalDateTime uploadTime;
    
    @Column(name = "ip_address")
    private String ipAddress;
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getImagePath() {
        return imagePath;
    }
    
    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }
    
    public Integer getPredictedClass() {
        return predictedClass;
    }
    
    public void setPredictedClass(Integer predictedClass) {
        this.predictedClass = predictedClass;
    }
    
    public String getClassName() {
        return className;
    }
    
    public void setClassName(String className) {
        this.className = className;
    }
    
    public Double getConfidence() {
        return confidence;
    }
    
    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }
    
    public LocalDateTime getUploadTime() {
        return uploadTime;
    }
    
    public void setUploadTime(LocalDateTime uploadTime) {
        this.uploadTime = uploadTime;
    }
    
    public String getIpAddress() {
        return ipAddress;
    }
    
    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
}
