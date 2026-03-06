package com.tsr.util;

import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

public class FileUtil {
    
    /**
     * 生成唯一的文件名
     */
    public static String generateUniqueFileName(String originalFileName) {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"));
        String randomId = UUID.randomUUID().toString().substring(0, 8);
        String extension = getFileExtension(originalFileName);
        return timestamp + "_" + randomId + "." + extension;
    }
    
    /**
     * 获取文件扩展名
     */
    private static String getFileExtension(String fileName) {
        int lastDotIndex = fileName.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return "jpg"; // 默认扩展名
        }
        return fileName.substring(lastDotIndex + 1).toLowerCase();
    }
    
    /**
     * 保存上传的文件
     */
    public static String saveFile(MultipartFile file, String storagePath) throws IOException {
        // 确保存储目录存在
        File directory = new File(storagePath);
        if (!directory.exists()) {
            directory.mkdirs();
        }
        
        // 生成唯一文件名
        String fileName = generateUniqueFileName(file.getOriginalFilename());
        String filePath = storagePath + File.separator + fileName;
        
        // 保存文件
        file.transferTo(new File(filePath));
        
        return fileName;
    }
    
    /**
     * 验证文件是否为有效的图像文件
     */
    public static boolean isValidImageFile(MultipartFile file) {
        String contentType = file.getContentType();
        return contentType != null && contentType.startsWith("image/");
    }
}
