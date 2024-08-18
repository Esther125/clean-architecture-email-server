# milecoolab-email-server

### Start the Email Server 
```python
docker compose up
```

### Run Tests
```python
python -m unittest
```

#### Test save_email function in persistence adapter with firestore
```
python -m test.adapter.outward.persistence.test_email_repository_with_firestore
```

### System Design Diagram
![Example Image](./images/system_design_diagram.png)

