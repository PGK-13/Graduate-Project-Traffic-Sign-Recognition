package com.tsr.repository;

import com.tsr.model.RecognitionRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public interface RecognitionRecordRepository extends JpaRepository<RecognitionRecord, Long> {
    
    // 获取类别分布统计
    @Query(value = "SELECT class_name as className, COUNT(*) as count FROM recognition_record GROUP BY class_name", nativeQuery = true)
    List<Map<String, Object>> getClassDistribution();
    
    // 获取总体统计信息
    @Query(value = "SELECT COUNT(*) as totalRecords, AVG(confidence) as avgConfidence FROM recognition_record", nativeQuery = true)
    Map<String, Object> getOverviewStatistics();
}
