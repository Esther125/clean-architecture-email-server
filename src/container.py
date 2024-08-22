from dependency_injector import containers, providers
from src.adapter.outward.integration.send_email_adapter import SendEmailAdapter
from src.adapter.outward.persistence.email_repository import DBClient, EmailRepository
from src.adapter.outward.persistence.save_email_adapter import SaveEmailAdapter
from src.adapter.outward.persistence.update_email_state_adapter import (
    UpdateEmailStateAdapter,
)
from src.adapter.outward.queue.email_queue_publisher_adapter import (
    EmailQueuePublisherAdapter,
)
from src.app.domain.service.queue_and_save_email.queue_and_save_email import (
    QueueAndSaveEmailService,
)
from src.app.domain.service.send_and_update_email_state.send_and_update_email_state import (
    SendAndUpdateEmailStateService,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.adapter.inward.web.send_email.queue_email_request_controller",
            "src.adapter.inward.web.send_email.user_email_request_controller",
        ]
    )
    config = providers.Configuration()
    db_client = providers.Factory(
        DBClient,
    )
    email_repository = providers.Factory(EmailRepository, client=db_client)
    save_email_adapter = providers.Factory(
        SaveEmailAdapter, repository=email_repository
    )
    queue_email_adapter = providers.Factory(
        EmailQueuePublisherAdapter, email_repository=email_repository
    )
    queue_and_save_email_service = providers.Factory(
        QueueAndSaveEmailService,
        save_email_adapter=save_email_adapter,
        queue_email_adapter=queue_email_adapter,
    )

    send_email_adapter = providers.Factory(
        SendEmailAdapter,
    )
    update_email_state_adapter = providers.Factory(
        UpdateEmailStateAdapter, repository=email_repository
    )
    send_and_update_email_state_service = providers.Factory(
        SendAndUpdateEmailStateService,
        send_email_adapter=send_email_adapter,
        update_email_state_adapter=update_email_state_adapter,
    )
