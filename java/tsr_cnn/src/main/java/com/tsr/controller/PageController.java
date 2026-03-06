package com.tsr.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {
    
    /**
     * 首页
     */
    @GetMapping("/")
    public String index() {
        return "index.html";
    }
    
    /**
     * 上传页面
     */
    @GetMapping("/upload")
    public String upload() {
        return "index.html";
    }
    
    /**
     * 记录页面
     */
    @GetMapping("/records")
    public String records() {
        return "records.html";
    }
    
    /**
     * 统计页面
     */
    @GetMapping("/statistics")
    public String statistics() {
        return "statistics.html";
    }
}
