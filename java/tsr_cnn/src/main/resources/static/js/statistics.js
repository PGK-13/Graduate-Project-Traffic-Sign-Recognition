document.addEventListener('DOMContentLoaded', function() {
    const totalRecordsElement = document.getElementById('total-records');
    const avgConfidenceElement = document.getElementById('avg-confidence');
    const distributionChart = document.getElementById('distribution-chart');
    
    // 加载统计概览
    function loadOverview() {
        fetch('/api/statistic/overview')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const stats = data.data;
                    totalRecordsElement.textContent = stats.totalRecords || 0;
                    
                    if (stats.avgConfidence) {
                        avgConfidenceElement.textContent = (stats.avgConfidence * 100).toFixed(2) + '%';
                    } else {
                        avgConfidenceElement.textContent = '0%';
                    }
                } else {
                    console.error('加载统计概览失败:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    // 加载类别分布
    function loadClassDistribution() {
        fetch('/api/statistic/class-distribution')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderClassDistribution(data.data);
                } else {
                    console.error('加载类别分布失败:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    // 渲染类别分布
    function renderClassDistribution(distribution) {
        if (distribution.length === 0) {
            distributionChart.innerHTML = '<p style="text-align: center; color: #666;">暂无数据</p>';
            return;
        }
        
        // 创建简单的柱状图
        let chartHTML = '<div style="display: flex; flex-direction: column; gap: 1rem;">';
        
        distribution.forEach(item => {
            const className = item.className;
            const count = item.count;
            const percentage = calculatePercentage(count, distribution);
            
            chartHTML += `
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 150px; font-size: 0.9rem;">${className}</div>
                    <div style="flex: 1; height: 30px; background-color: #f0f0f0; border-radius: 4px; overflow: hidden;">
                        <div style="height: 100%; width: ${percentage}%; background-color: #3498db; transition: width 0.5s ease;"></div>
                    </div>
                    <div style="width: 80px; text-align: right; font-weight: bold;">${count}</div>
                </div>
            `;
        });
        
        chartHTML += '</div>';
        distributionChart.innerHTML = chartHTML;
    }
    
    // 计算百分比
    function calculatePercentage(count, distribution) {
        const total = distribution.reduce((sum, item) => sum + item.count, 0);
        return total > 0 ? (count / total) * 100 : 0;
    }
    
    // 初始加载
    loadOverview();
    loadClassDistribution();
});
