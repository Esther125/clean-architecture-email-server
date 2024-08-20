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

### Tests

#### Run unittests
```python
python -m unittest discover -s test/unit
```

#### Run integration tests
```
python -m unittest discover -s test/integration
```

### System Design Diagram
![Example Image](./images/system_design_diagram.png)
