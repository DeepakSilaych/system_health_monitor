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

## Python Client Library

We now provide an official Python client library for easier integration:

```bash
pip install climate-monitor-client
```

### Quick Start

```python
from climate_monitor import SystemMonitorClient

# Initialize the client
monitor = SystemMonitorClient(
    base_url='http://your-monitor-host:8000',
    service_name='your-service-name',
    api_key='your-api-key'  # Optional
)

# Update service status
monitor.update_status('up', 'http://your-service:port')

# Send system metrics
monitor.send_metrics()

# Update pipeline status
monitor.update_pipeline(
    pipeline_type='data_ingestion',
    status='running',
    metadata={'step': 'download', 'progress': 45}
)

# Send an alert
monitor.send_alert(
    title='High CPU Usage',
    message='CPU usage above 90%',
    severity=2  # 1: Info, 2: Warning, 3: Critical
)

# Start automatic metric collection
monitor.start_metric_collection(interval=60)  # Every minute
```

### Features

The client library provides:
- Automatic retry with exponential backoff
- Built-in error handling and logging
- System metrics collection using `psutil`
- Configurable request timeouts
- Automatic alert generation on errors

### Advanced Usage

1. **Custom Metrics**
```python
# Send custom metrics along with system metrics
monitor.send_metrics({
    'requests_per_second': 156.7,
    'response_time_ms': 245.3
})
```

2. **Pipeline Monitoring**
```python
# Track ML pipeline progress
monitor.update_pipeline(
    pipeline_type='training',
    status='running',
    metadata={
        'epoch': 5,
        'loss': 0.234,
        'accuracy': 0.945
    }
)
```

3. **Continuous Monitoring**
```python
# Start collecting metrics with custom metrics
monitor.start_metric_collection(
    interval=30,  # Every 30 seconds
    additional_metrics={
        'queue_size': lambda: get_queue_size(),
        'active_users': lambda: count_active_users()
    }
)
```

## Error Handling

The client library automatically handles common errors:

1. **Network Issues**
- Automatic retry with exponential backoff
- Configurable max retries and timeout
- Automatic error logging

2. **Server Errors**
- Retry on 5xx errors
- Automatic alert generation
- Detailed error logging

3. **Authentication**
- Proper API key handling
- Clear error messages on auth failures

## Best Practices

1. **Service Status**
- Update status on service startup
- Set status to 'down' on graceful shutdown
- Use health check endpoints

2. **Metrics Collection**
- Use reasonable collection intervals (30-60s)
- Include relevant custom metrics
- Monitor resource usage trends

3. **Pipeline Monitoring**
- Track all important pipeline stages
- Include relevant metadata
- Set appropriate error messages

4. **Alerts**
- Use appropriate severity levels
- Include actionable information
- Avoid alert fatigue

## Support

For issues and feature requests, please visit our [GitHub repository](https://github.com/your-org/climate-system-monitor).

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
