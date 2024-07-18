import abc

from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand

class UpdateEmailStatePort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update_state(self, command: UpdateEmailStateCommand):
        raise NotImplementedError