// LinguaAI - Charts & Analytics JavaScript

class ProgressChart {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            type: options.type || 'line',
            colors: options.colors || ['#6366f1', '#8b5cf6', '#10b981'],
            ...options
        };
        this.data = [];
        this.init();
    }
    
    init() {
        if (this.container) {
            this.render();
        }
    }
    
    setData(data) {
        this.data = data;
        this.render();
    }
    
    render() {
        if (!this.container) return;
        
        switch (this.options.type) {
            case 'line':
                this.renderLineChart();
                break;
            case 'bar':
                this.renderBarChart();
                break;
            case 'doughnut':
                this.renderDoughnutChart();
                break;
            case 'progress':
                this.renderProgressRing();
                break;
        }
    }
    
    renderLineChart() {
        const canvas = document.createElement('canvas');
        canvas.className = 'progress-chart';
        this.container.innerHTML = '';
        this.container.appendChild(canvas);
        
        // Simple SVG line chart
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 400 200');
        svg.setAttribute('class', 'line-chart-svg');
        
        if (this.data.length > 0) {
            const max = Math.max(...this.data.map(d => d.value));
            const points = this.data.map((d, i) => {
                const x = (i / (this.data.length - 1)) * 360 + 20;
                const y = 180 - (d.value / max) * 160;
                return `${x},${y}`;
            }).join(' ');
            
            // Line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
            line.setAttribute('points', points);
            line.setAttribute('fill', 'none');
            line.setAttribute('stroke', this.options.colors[0]);
            line.setAttribute('stroke-width', '3');
            line.setAttribute('stroke-linecap', 'round');
            line.setAttribute('stroke-linejoin', 'round');
            svg.appendChild(line);
            
            // Area
            const area = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
            area.setAttribute('points', `20,180 ${points} 380,180`);
            area.setAttribute('fill', `url(#gradient-${this.container.id})`);
            svg.insertBefore(area, line);
            
            // Gradient
            const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
            defs.innerHTML = `
                <linearGradient id="gradient-${this.container.id}" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="${this.options.colors[0]}" stop-opacity="0.3"/>
                    <stop offset="100%" stop-color="${this.options.colors[0]}" stop-opacity="0"/>
                </linearGradient>
            `;
            svg.insertBefore(defs, svg.firstChild);
            
            // Points
            this.data.forEach((d, i) => {
                const x = (i / (this.data.length - 1)) * 360 + 20;
                const y = 180 - (d.value / max) * 160;
                
                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('cx', x);
                circle.setAttribute('cy', y);
                circle.setAttribute('r', '6');
                circle.setAttribute('fill', this.options.colors[0]);
                svg.appendChild(circle);
            });
        }
        
        this.container.appendChild(svg);
    }
    
    renderBarChart() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 400 200');
        
        if (this.data.length > 0) {
            const max = Math.max(...this.data.map(d => d.value));
            const barWidth = 340 / this.data.length - 10;
            
            this.data.forEach((d, i) => {
                const x = 30 + i * (barWidth + 10);
                const height = (d.value / max) * 160;
                const y = 180 - height;
                
                // Bar
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', x);
                rect.setAttribute('y', y);
                rect.setAttribute('width', barWidth);
                rect.setAttribute('height', height);
                rect.setAttribute('fill', this.options.colors[i % this.options.colors.length]);
                rect.setAttribute('rx', '4');
                svg.appendChild(rect);
                
                // Label
                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', x + barWidth / 2);
                text.setAttribute('y', '195');
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('fill', '#64748b');
                text.setAttribute('font-size', '12');
                text.textContent = d.label;
                svg.appendChild(text);
            });
        }
        
        this.container.appendChild(svg);
    }
    
    renderDoughnutChart() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 200 200');
        
        const cx = 100;
        const cy = 100;
        const radius = 80;
        const thickness = 20;
        
        if (this.data.length > 0) {
            const total = this.data.reduce((sum, d) => sum + d.value, 0);
            let startAngle = -90;
            
            this.data.forEach((d, i) => {
                const percentage = d.value / total;
                const angle = percentage * 360;
                const endAngle = startAngle + angle;
                
                const startRad = (startAngle * Math.PI) / 180;
                const endRad = (endAngle * Math.PI) / 180;
                
                const x1 = cx + radius * Math.cos(startRad);
                const y1 = cy + radius * Math.sin(startRad);
                const x2 = cx + radius * Math.cos(endRad);
                const y2 = cy + radius * Math.sin(endRad);
                
                const largeArc = angle > 180 ? 1 : 0;
                
                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                path.setAttribute('d', `M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} Z`);
                path.setAttribute('fill', this.options.colors[i % this.options.colors.length]);
                svg.appendChild(path);
                
                startAngle = endAngle;
            });
            
            // Center circle
            const center = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            center.setAttribute('cx', cx);
            center.setAttribute('cy', cy);
            center.setAttribute('r', radius - thickness);
            center.setAttribute('fill', '#1e293b');
            svg.appendChild(center);
        }
        
        this.container.appendChild(svg);
    }
    
    renderProgressRing() {
        const percentage = this.data[0]?.value || 0;
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 120 120');
        
        const cx = 60;
        const cy = 60;
        const radius = 50;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (percentage / 100) * circumference;
        
        // Background circle
        const bgCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        bgCircle.setAttribute('cx', cx);
        bgCircle.setAttribute('cy', cy);
        bgCircle.setAttribute('r', radius);
        bgCircle.setAttribute('fill', 'none');
        bgCircle.setAttribute('stroke', 'rgba(255,255,255,0.1)');
        bgCircle.setAttribute('stroke-width', '8');
        svg.appendChild(bgCircle);
        
        // Progress circle
        const progressCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        progressCircle.setAttribute('cx', cx);
        progressCircle.setAttribute('cy', cy);
        progressCircle.setAttribute('r', radius);
        progressCircle.setAttribute('fill', 'none');
        progressCircle.setAttribute('stroke', this.options.colors[0]);
        progressCircle.setAttribute('stroke-width', '8');
        progressCircle.setAttribute('stroke-linecap', 'round');
        progressCircle.setAttribute('stroke-dasharray', circumference);
        progressCircle.setAttribute('stroke-dashoffset', circumference);
        progressCircle.style.transition = 'stroke-dashoffset 1s ease';
        svg.appendChild(progressCircle);
        
        this.container.appendChild(svg);
        
        // Animate
        setTimeout(() => {
            progressCircle.setAttribute('stroke-dashoffset', offset);
        }, 100);
    }
}

// Statistics Manager
class StatsManager {
    constructor() {
        this.stats = {
            lessonsCompleted: 0,
            totalTime: 0,
            currentStreak: 0,
            longestStreak: 0,
            totalXP: 0,
            messagesExchanged: 0
        };
        this.init();
    }
    
    init() {
        this.loadStats();
    }
    
    loadStats() {
        const saved = storage.get('user_stats');
        if (saved) {
            this.stats = { ...this.stats, ...saved };
        }
    }
    
    saveStats() {
        storage.set('user_stats', this.stats);
    }
    
    incrementLessons() {
        this.stats.lessonsCompleted++;
        this.saveStats();
    }
    
    addTime(minutes) {
        this.stats.totalTime += minutes;
        this.saveStats();
    }
    
    addXP(amount) {
        this.stats.totalXP += amount;
        this.saveStats();
    }
    
    incrementMessages() {
        this.stats.messagesExchanged++;
        this.saveStats();
    }
    
    updateStreak() {
        const today = new Date().toDateString();
        const lastPractice = storage.get('last_practice_date');
        
        if (lastPractice === today) {
            return;
        }
        
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (lastPractice === yesterday.toDateString()) {
            this.stats.currentStreak++;
        } else {
            this.stats.currentStreak = 1;
        }
        
        if (this.stats.currentStreak > this.stats.longestStreak) {
            this.stats.longestStreak = this.stats.currentStreak;
        }
        
        storage.set('last_practice_date', today);
        this.saveStats();
    }
    
    getStats() {
        return this.stats;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    window.statsManager = new StatsManager();
    
    // Initialize charts if containers exist
    const progressChart = document.getElementById('progressChart');
    if (progressChart) {
        window.progressChart = new ProgressChart('progressChart', {
            type: 'line',
            data: [
                { label: 'Mon', value: 30 },
                { label: 'Tue', value: 45 },
                { label: 'Wed', value: 35 },
                { label: 'Thu', value: 60 },
                { label: 'Fri', value: 50 },
                { label: 'Sat', value: 75 },
                { label: 'Sun', value: 65 }
            ]
        });
    }
    
    const dailyProgress = document.getElementById('dailyProgress');
    if (dailyProgress) {
        window.dailyProgress = new ProgressChart('dailyProgress', {
            type: 'progress',
            data: [{ value: 66 }]
        });
    }
});

// Export
window.ProgressChart = ProgressChart;
window.StatsManager = StatsManager;