
# for future reference

## 1. project location on server: /home/system_health_monitor
```bash
cd /home/system_health_monitor
git pull
```

## 2. restart services
```bash
sudo systemctl restart gunicorn2
sudo systemctl restart celery_worker
sudo systemctl restart celery_beat
```

## 3. check logs
```bash
sudo journalctl -u gunicorn2
sudo journalctl -u celery_worker
sudo journalctl -u celery_beat
```

## 4. check status
```bash
sudo systemctl status gunicorn2
sudo systemctl status celery_worker
sudo systemctl status celery_beat
```
