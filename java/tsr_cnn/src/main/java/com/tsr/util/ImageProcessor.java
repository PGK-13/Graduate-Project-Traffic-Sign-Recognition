package com.tsr.util;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class ImageProcessor {
    
    private static final int TARGET_WIDTH = 32;
    private static final int TARGET_HEIGHT = 32;
    
    /**
     * 调整图像尺寸
     */
    public static BufferedImage resizeImage(BufferedImage originalImage) {
        BufferedImage resizedImage = new BufferedImage(TARGET_WIDTH, TARGET_HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = resizedImage.createGraphics();
        g.drawImage(originalImage, 0, 0, TARGET_WIDTH, TARGET_HEIGHT, null);
        g.dispose();
        return resizedImage;
    }
    
    /**
     * 将 BufferedImage 转换为字节数组
     */
    public static byte[] imageToBytes(BufferedImage image) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(image, "jpg", baos);
        return baos.toByteArray();
    }
    
    /**
     * 将字节数组转换为 BufferedImage
     */
    public static BufferedImage bytesToImage(byte[] bytes) throws IOException {
        try (InputStream is = new ByteArrayInputStream(bytes)) {
            return ImageIO.read(is);
        }
    }
    
    /**
     * 图像预处理：调整尺寸并归一化
     */
    public static float[] preprocessImage(BufferedImage image) {
        // 调整尺寸
        BufferedImage resizedImage = resizeImage(image);
        
        // 归一化处理
        float[] input = new float[TARGET_WIDTH * TARGET_HEIGHT * 3];
        int index = 0;
        
        for (int y = 0; y < TARGET_HEIGHT; y++) {
            for (int x = 0; x < TARGET_WIDTH; x++) {
                int rgb = resizedImage.getRGB(x, y);
                
                // 提取 RGB 通道并归一化
                float r = ((rgb >> 16) & 0xFF) / 255.0f;
                float g = ((rgb >> 8) & 0xFF) / 255.0f;
                float b = (rgb & 0xFF) / 255.0f;
                
                input[index++] = r;
                input[index++] = g;
                input[index++] = b;
            }
        }
        
        return input;
    }
    
    /**
     * 验证图像是否有效
     */
    public static boolean isValidImage(BufferedImage image) {
        return image != null && image.getWidth() > 0 && image.getHeight() > 0;
    }
}
