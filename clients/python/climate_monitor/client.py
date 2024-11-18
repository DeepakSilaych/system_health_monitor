import requests
import psutil
import time
import logging
from typing import Optional, Dict, Any, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class SystemMonitorClient:
    """Client for the Climate System Monitor."""

    def __init__(
        self,
        base_url: str,
        service_name: str,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 10
    ):
        """
        Initialize the monitor client.

        Args:
            base_url: Base URL of the monitoring service
            service_name: Name of your service
            api_key: Optional API key for authentication
            max_retries: Maximum number of retries for failed requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.service_name = service_name
        self.timeout = timeout
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Setup headers
        self.headers = {'Content-Type': 'application/json'}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with error handling and logging.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            self.send_alert(
                title=f"Monitor Client Error",
                message=f"Failed to {method} {endpoint}: {str(e)}",
                severity=2
            )
            raise

    def update_status(
        self,
        status: str = 'up',
        endpoint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update service status.

        Args:
            status: Service status ('up', 'down', or 'unknown')
            endpoint: Service endpoint URL
        """
        data = {
            'name': self.service_name,
            'status': status
        }
        if endpoint:
            data['endpoint'] = endpoint
        
        return self._make_request('POST', 'services/', data)

    def send_metrics(
        self,
        additional_metrics: Optional[Dict[str, float]] = None
    ) -> None:
        """
        Send system metrics.

        Args:
            additional_metrics: Optional dictionary of additional metrics to send
        """
        # Collect system metrics
        metrics = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent
        }
        
        # Add additional metrics
        if additional_metrics:
            metrics.update(additional_metrics)
        
        # Send each metric
        for metric_type, value in metrics.items():
            data = {
                'service': self.service_name,
                'metric_type': metric_type,
                'value': value
            }
            self._make_request('POST', 'metrics/', data)

    def update_pipeline(
        self,
        pipeline_type: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update pipeline status.

        Args:
            pipeline_type: Type of pipeline
            status: Pipeline status
            metadata: Optional pipeline metadata
            error_message: Optional error message if pipeline failed
        """
        data = {
            'pipeline_type': pipeline_type,
            'status': status
        }
        if metadata:
            data['metadata'] = metadata
        if error_message:
            data['error_message'] = error_message
            
        return self._make_request('POST', 'pipelines/', data)

    def send_alert(
        self,
        title: str,
        message: str,
        severity: int = 1
    ) -> Dict[str, Any]:
        """
        Send an alert.

        Args:
            title: Alert title
            message: Alert message
            severity: Alert severity (1: Info, 2: Warning, 3: Critical)
        """
        data = {
            'title': title,
            'message': message,
            'severity': severity,
            'service': self.service_name
        }
        return self._make_request('POST', 'alerts/', data)

    def start_metric_collection(
        self,
        interval: int = 60,
        additional_metrics: Optional[Dict[str, float]] = None
    ) -> None:
        """
        Start collecting and sending metrics at regular intervals.

        Args:
            interval: Collection interval in seconds
            additional_metrics: Optional dictionary of additional metrics to collect
        """
        while True:
            try:
                self.send_metrics(additional_metrics)
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Metric collection failed: {str(e)}")
                # Don't send alert here as send_metrics already does
