# milecoolab-email-server

### Start the Email Server 
```python
docker compose up
```

### Run Tests
```python
python -m unittest
```

#### Test functions in persistence adapter with firestore
```python
# Save Email
python -m test.adapter.outward.persistence.test_email_repository_with_firestore

# Update Email state
python -m test.adapter.outward.persistence.test_update_email_state_adapter_with_firestore
```

### System Design Diagram
![Example Image](./images/system_design_diagram.png)

