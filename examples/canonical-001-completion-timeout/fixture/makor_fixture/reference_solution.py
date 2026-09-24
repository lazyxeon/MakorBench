from __future__ import annotations

from .completion import CompletionChannel, PublishResult


class CurrentCredentialChannel(CompletionChannel):
    """Reference repair used only to validate the public development fixture."""

    def __init__(self, **kwargs):
        self._token_manager = kwargs["token_manager"]
        super().__init__(**kwargs)

    def publish(self, job_id: str) -> PublishResult:
        return self.gateway.publish(
            job_id,
            self._token_manager.current_token,
            channel_id=self.channel_id,
            channel_age=self.clock.now - self.created_at,
        )
