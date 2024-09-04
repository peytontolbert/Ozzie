class Dashboard {
    constructor() {
        this.data = {};
        this.components = {
            taskList: null,
            progressCharts: null,
            performanceMetrics: null,
            milestoneView: null
        };
    }

    async initialize() {
        await this.fetchData();
        this.renderLayout();
        this.initializeComponents();
        this.setupWebSocket();
    }

    async fetchData() {
        const response = await fetch('/api/dashboard-data', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (response.ok) {
            this.data = await response.json();
        } else {
            console.error('Failed to fetch dashboard data');
        }
    }

    renderLayout() {
        const dashboard = document.getElementById('dashboard');
        dashboard.innerHTML = `
            <div class="row">
                <div class="col-md-6" id="task-list"></div>
                <div class="col-md-6" id="progress-charts"></div>
            </div>
            <div class="row">
                <div class="col-md-6" id="performance-metrics"></div>
                <div class="col-md-6" id="milestone-view"></div>
            </div>
        `;
    }

    initializeComponents() {
        this.components.taskList = new TaskList('task-list', this.data.tasks);
        this.components.progressCharts = new ProgressCharts('progress-charts', this.data.progress);
        this.components.performanceMetrics = new PerformanceMetrics('performance-metrics', this.data.metrics);
        this.components.milestoneView = new MilestoneView('milestone-view', this.data.milestones);

        Object.values(this.components).forEach(component => component.render());
    }

    setupWebSocket() {
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateComponent(data.type, data.data);
        };
    }

    updateComponent(type, data) {
        switch (type) {
            case 'tasks':
                this.components.taskList.update(data);
                break;
            case 'progress':
                this.components.progressCharts.update(data);
                break;
            case 'metrics':
                this.components.performanceMetrics.update(data);
                break;
            case 'milestones':
                this.components.milestoneView.update(data);
                break;
        }
    }

    update() {
        Object.values(this.components).forEach(component => component.update());
    }
}

class TaskList {
    constructor(containerId, tasks) {
        this.container = document.getElementById(containerId);
        this.tasks = tasks;
    }

    render() {
        this.container.innerHTML = `
            <h2>Tasks</h2>
            <ul class="list-group">
                ${this.tasks.map(task => `
                    <li class="list-group-item">
                        <span class="badge ${this.getStatusBadgeClass(task.status)}">${task.status}</span>
                        ${task.title}
                    </li>
                `).join('')}
            </ul>
        `;
    }

    getStatusBadgeClass(status) {
        switch (status.toLowerCase()) {
            case 'completed': return 'bg-success';
            case 'in progress': return 'bg-primary';
            case 'pending': return 'bg-warning';
            default: return 'bg-secondary';
        }
    }

    update() {
        // Implement update logic
    }
}

class ProgressCharts {
    constructor(containerId, progressData) {
        this.container = document.getElementById(containerId);
        this.progressData = progressData;
    }

    render() {
        this.container.innerHTML = `
            <h2>Progress</h2>
            <canvas id="progress-chart"></canvas>
        `;
        this.createChart();
    }

    createChart() {
        const ctx = document.getElementById('progress-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(this.progressData),
                datasets: [{
                    label: 'Progress',
                    data: Object.values(this.progressData),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)'
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    update() {
        // Implement update logic
    }
}

class PerformanceMetrics {
    constructor(containerId, metrics) {
        this.container = document.getElementById(containerId);
        this.metrics = metrics;
    }

    render() {
        this.container.innerHTML = `
            <h2>Performance Metrics</h2>
            <div class="row">
                ${Object.entries(this.metrics).map(([key, value]) => `
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${key}</h5>
                                <p class="card-text display-4">${value}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    update() {
        // Implement update logic
    }
}

class MilestoneView {
    constructor(containerId, milestones) {
        this.container = document.getElementById(containerId);
        this.milestones = milestones;
    }

    render() {
        this.container.innerHTML = `
            <h2>Milestones</h2>
            <div class="timeline">
                ${this.milestones.map((milestone, index) => `
                    <div class="timeline-item">
                        <div class="timeline-badge ${this.getMilestoneBadgeClass(milestone.status)}"></div>
                        <div class="timeline-panel">
                            <div class="timeline-heading">
                                <h4 class="timeline-title">${milestone.title}</h4>
                                <p><small class="text-muted">${milestone.date}</small></p>
                            </div>
                            <div class="timeline-body">
                                <p>${milestone.description}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    getMilestoneBadgeClass(status) {
        switch (status.toLowerCase()) {
            case 'completed': return 'bg-success';
            case 'in progress': return 'bg-primary';
            case 'upcoming': return 'bg-info';
            default: return 'bg-secondary';
        }
    }

    update() {
        // Implement update logic
    }
}

// Usage
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    dashboard.initialize();
});