import abc

from src.app.port.outward.execute_send_email.execute_send_email_command import ExecuteSendEmailCommand


class ExecuteSendEmailPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute_send_email(self, command: ExecuteSendEmailCommand):
        raise NotImplementedError