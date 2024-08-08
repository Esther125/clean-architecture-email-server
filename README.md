# milecoolab-email-server

### Start the Email Server
```python
uvicorn src.main:app --port 8080 --reload
```

### Run Tests
```python

python -m unittest tests/app/domain/service/queue_and_save_email/test_queue_and_save_email.py

python -m unittest tests/app/domain/service/send_and_update_email_state/test_send_and_update_email_state.py

python -m unittest tests/adapter/inward/web/send_email/test_send_email_controller.py
```
