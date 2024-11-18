# Climate System Monitor Client

Python client library for the Climate System Monitor.

## Installation

```bash
pip install climate-monitor-client
```

## Quick Start

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
```

## Features

- Service health monitoring
- System metrics collection (CPU, Memory, Disk)
- Pipeline status tracking
- Alert management
- Automatic retry with exponential backoff
- Configurable metrics collection interval

## Documentation

For detailed documentation and examples, visit our [documentation site](docs/API_INTEGRATION.md).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
