from unittest import TestCase
from unittest.mock import Mock

from src.app.domain.service.send_email.send_email import EmailSendingError, SendEmailService, UpdateEmailStateError
from src.app.port.inward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.sending_email.sending_email_port import SendingEmailPort
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class TestSendEmailService(TestCase):
    def setUp(self):
        self.sending_email_port = Mock(spec=SendingEmailPort)
        self.update_email_state_port = Mock(spec=UpdateEmailStatePort)
        self.service = SendEmailService(self.sending_email_port, self.update_email_state_port)
        self.command = SendEmailCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    def test_send_email_success(self):
        self.sending_email_port.sending_email.return_value = None
        self.update_email_state_port.update_state.return_value = None

        self.service.send_email(self.command)

        self.sending_email_port.sending_email.assert_called_once()
        self.update_email_state_port.update_state.assert_called_once()
    
    def test_send_email_failure_on_send(self):
        self.sending_email_port.sending_email.side_effect = EmailSendingError()

        with self.assertRaises(EmailSendingError):
            self.service.send_email(self.command)
        
        self.update_email_state_port.update_state.assert_not_called()

    def test_send_email_failure_on_update_state(self):
        self.sending_email_port.sending_email.return_value = None 
        self.update_email_state_port.update_state.side_effect = UpdateEmailStateError()

        with self.assertRaises(UpdateEmailStateError):
            self.service.send_email(self.command)
        
        self.sending_email_port.sending_email.assert_called_once()



        
