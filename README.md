# milecoolab-email-server

### Start the Email Server 
Using docker compose:
```python
docker compose up
```

Using FastAPI command:
```
fastapi dev src/main.py --port 8080 
```

### Run Tests

#### Run all unittests
```python
python -m unittest
```

#### Test publish function in queue adapter with pub/sub
```
python -m test.adapter.outward.queue.test_queue_publisher_with_pub_sub
```

### System Design Diagram
![Example Image](./images/system_design_diagram.png)
