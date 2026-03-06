document.addEventListener('DOMContentLoaded', function() {
    const recordsTable = document.getElementById('records-table').querySelector('tbody');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    
    let currentPage = 0;
    let totalPages = 1;
    let pageSize = 10;
    
    // 加载记录
    function loadRecords(page) {
        fetch(`/api/record/list?page=${page}&size=${pageSize}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderRecords(data.data);
                    updatePagination(data.page, data.pages, data.total);
                } else {
                    console.error('加载记录失败:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    // 渲染记录
    function renderRecords(records) {
        recordsTable.innerHTML = '';
        
        if (records.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="7" style="text-align: center;">暂无记录</td>';
            recordsTable.appendChild(row);
            return;
        }
        
        records.forEach((record, index) => {
            const row = document.createElement('tr');
            const serialNumber = currentPage * pageSize + index + 1;
            
            row.innerHTML = `
                <td>${serialNumber}</td>
                <td>${formatDateTime(record.uploadTime)}</td>
                <td><img src="/uploads/${record.imagePath}" alt="交通标志"></td>
                <td>${record.predictedClass}</td>
                <td>${record.className}</td>
                <td>${(record.confidence * 100).toFixed(2)}%</td>
                <td>${record.ipAddress || '-'}</td>
            `;
            
            recordsTable.appendChild(row);
        });
    }
    
    // 更新分页信息
    function updatePagination(page, pages, total) {
        currentPage = page;
        totalPages = pages;
        
        pageInfo.textContent = `第 ${page + 1} 页，共 ${pages} 页，总计 ${total} 条记录`;
        
        prevPageBtn.disabled = page === 0;
        nextPageBtn.disabled = page >= pages - 1;
    }
    
    // 格式化日期时间
    function formatDateTime(dateTimeString) {
        const date = new Date(dateTimeString);
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    // 分页按钮事件
    prevPageBtn.addEventListener('click', function() {
        if (currentPage > 0) {
            loadRecords(currentPage - 1);
        }
    });
    
    nextPageBtn.addEventListener('click', function() {
        if (currentPage < totalPages - 1) {
            loadRecords(currentPage + 1);
        }
    });
    
    // 初始加载第一页
    loadRecords(0);
});
