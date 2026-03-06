package com.tsr.listener;

import com.tsr.service.ModelService;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
public class ApplicationStartupListener {
    
    private final ModelService modelService;
    
    public ApplicationStartupListener(ModelService modelService) {
        this.modelService = modelService;
    }
    
    /**
     * 应用启动时初始化模型
     */
    @EventListener(ContextRefreshedEvent.class)
    public void onApplicationStartup() {
        try {
            System.out.println("正在初始化 ONNX 模型...");
            modelService.initialize();
            System.out.println("ONNX 模型初始化完成");
        } catch (Exception e) {
            System.err.println("模型初始化失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
