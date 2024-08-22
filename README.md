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
docker compose up
python -m unittest discover -s test/integration
```

### System Design Diagram
![Example Image](./images/system_design_diagram.png)

### Documents
For detailed documentation, please refer to the [Document](./docs/document.pdf).
