import abc

from src.app.port.outward.save_email.save_email_command import SaveEmailCommand 

class SaveEmailPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_email(self, command: SaveEmailCommand):
        raise NotImplementedError