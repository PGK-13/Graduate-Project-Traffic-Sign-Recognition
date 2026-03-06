-- 创建数据库
CREATE DATABASE IF NOT EXISTS tsr_cnn CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE tsr_cnn;

-- 创建识别记录表
CREATE TABLE IF NOT EXISTS recognition_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    image_path VARCHAR(255) NOT NULL,
    predicted_class INT NOT NULL,
    class_name VARCHAR(255) NOT NULL,
    confidence DOUBLE NOT NULL,
    upload_time DATETIME NOT NULL,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 添加索引
CREATE INDEX idx_upload_time ON recognition_record(upload_time);
CREATE INDEX idx_predicted_class ON recognition_record(predicted_class);
CREATE INDEX idx_class_name ON recognition_record(class_name);

-- 插入测试数据
INSERT INTO recognition_record (image_path, predicted_class, class_name, confidence, upload_time, ip_address)
VALUES 
('test_1.jpg', 0, '限速 20km/h', 0.98, NOW(), '127.0.0.1'),
('test_2.jpg', 1, '限速 30km/h', 0.95, NOW(), '127.0.0.1'),
('test_3.jpg', 2, '限速 50km/h', 0.99, NOW(), '127.0.0.1');

-- 查看表结构
DESCRIBE recognition_record;

-- 查看插入的数据
SELECT * FROM recognition_record;
