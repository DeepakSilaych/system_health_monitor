# System Monitor Integration Guide

This guide explains how to integrate your services with the Climate System Monitor.

## Base URL
```
http://your-monitor-host:8000
```

## Authentication
Currently using basic authentication. Include your API key in the headers:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Service Status Updates
Report your service's health status.

```http
POST /services/
```

```json
{
    "name": "your-service-name",
    "status": "up",  // up, down, or unknown
    "endpoint": "http://your-service:port"
}
```

### 2. Metrics Reporting
Send system metrics (CPU, memory, etc.).

```http
POST /metrics/
```

```json
{
    "service": "your-service-name",
    "metric_type": "cpu",  // cpu, memory, disk, network
    "value": 45.2
}
```

### 3. Pipeline Status Updates
Report ML/data pipeline status.

```http
POST /pipelines/
```

```json
{
    "pipeline_type": "data_ingestion",  // data_ingestion, preprocessing, training, evaluation
    "status": "running",  // running, completed, failed
    "metadata": {
        "step": "data_download",
        "progress": 45
    }
}
```

### 4. Alert Creation
Create system alerts.

```http
POST /alerts/
```

```json
{
    "title": "High CPU Usage",
    "message": "CPU usage above 90%",
    "severity": 2,  // 1: Info, 2: Warning, 3: Critical
    "service": "your-service-name"
}
```

## Python Integration Example

```python
import requests
import psutil
import time

class SystemMonitorClient:
    def __init__(self, base_url, service_name, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.service_name = service_name
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def update_status(self, status='up', endpoint=None):
        """Update service status"""
        data = {
            'name': self.service_name,
            'status': status
        }
        if endpoint:
            data['endpoint'] = endpoint
        
        response = requests.post(
            f'{self.base_url}/services/',
            json=data,
            headers=self.headers
        )
        return response.json()

    def send_metrics(self):
        """Send system metrics"""
        metrics = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent
        }
        
        for metric_type, value in metrics.items():
            data = {
                'service': self.service_name,
                'metric_type': metric_type,
                'value': value
            }
            requests.post(
                f'{self.base_url}/metrics/',
                json=data,
                headers=self.headers
            )

    def update_pipeline(self, pipeline_type, status, metadata=None):
        """Update pipeline status"""
        data = {
            'pipeline_type': pipeline_type,
            'status': status
        }
        if metadata:
            data['metadata'] = metadata
            
        response = requests.post(
            f'{self.base_url}/pipelines/',
            json=data,
            headers=self.headers
        )
        return response.json()

    def send_alert(self, title, message, severity=1):
        """Send an alert"""
        data = {
            'title': title,
            'message': message,
            'severity': severity,
            'service': self.service_name
        }
        response = requests.post(
            f'{self.base_url}/alerts/',
            json=data,
            headers=self.headers
        )
        return response.json()

# Usage Example
if __name__ == '__main__':
    monitor = SystemMonitorClient(
        base_url='http://localhost:8000',
        service_name='example-service'
    )

    # Update service status
    monitor.update_status('up', 'http://example-service:8000')

    # Send metrics every minute
    while True:
        try:
            monitor.send_metrics()
            time.sleep(60)
        except Exception as e:
            monitor.send_alert(
                'Metrics Collection Failed',
                str(e),
                severity=2
            )
```

## Node.js Integration Example

```javascript
const axios = require('axios');
const os = require('os');

class SystemMonitorClient {
    constructor(baseUrl, serviceName, apiKey = null) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.serviceName = serviceName;
        this.headers = {
            'Content-Type': 'application/json'
        };
        if (apiKey) {
            this.headers['Authorization'] = `Bearer ${apiKey}`;
        }
    }

    async updateStatus(status = 'up', endpoint = null) {
        const data = {
            name: this.serviceName,
            status
        };
        if (endpoint) {
            data.endpoint = endpoint;
        }

        const response = await axios.post(
            `${this.baseUrl}/services/`,
            data,
            { headers: this.headers }
        );
        return response.data;
    }

    async sendMetrics() {
        const metrics = {
            cpu: os.loadavg()[0],
            memory: (os.totalmem() - os.freemem()) / os.totalmem() * 100,
            disk: 0 // Requires additional package for disk usage
        };

        for (const [metricType, value] of Object.entries(metrics)) {
            const data = {
                service: this.serviceName,
                metric_type: metricType,
                value
            };
            await axios.post(
                `${this.baseUrl}/metrics/`,
                data,
                { headers: this.headers }
            );
        }
    }

    async updatePipeline(pipelineType, status, metadata = null) {
        const data = {
            pipeline_type: pipelineType,
            status
        };
        if (metadata) {
            data.metadata = metadata;
        }

        const response = await axios.post(
            `${this.baseUrl}/pipelines/`,
            data,
            { headers: this.headers }
        );
        return response.data;
    }

    async sendAlert(title, message, severity = 1) {
        const data = {
            title,
            message,
            severity,
            service: this.serviceName
        };
        const response = await axios.post(
            `${this.baseUrl}/alerts/`,
            data,
            { headers: this.headers }
        );
        return response.data;
    }
}

// Usage Example
async function main() {
    const monitor = new SystemMonitorClient(
        'http://localhost:8000',
        'example-service'
    );

    try {
        // Update service status
        await monitor.updateStatus('up', 'http://example-service:3000');

        // Send metrics every minute
        setInterval(async () => {
            try {
                await monitor.sendMetrics();
            } catch (error) {
                await monitor.sendAlert(
                    'Metrics Collection Failed',
                    error.message,
                    2
                );
            }
        }, 60000);
    } catch (error) {
        console.error('Monitor error:', error);
    }
}

main();
```

## Integration Best Practices

1. **Regular Status Updates**: Send service status updates at least every minute
2. **Metric Collection**: Send system metrics every 1-5 minutes depending on your needs
3. **Pipeline Updates**: Send pipeline status updates at each state change
4. **Error Handling**: Send alerts for any critical errors or anomalies
5. **Retry Logic**: Implement exponential backoff for failed requests
6. **Batch Metrics**: If sending many metrics, consider batching them

## Support

For integration support or to report issues:
1. Create an issue in our GitHub repository
2. Contact the system monitoring team
3. Check the monitoring dashboard for system status
