"""Module for Message base definition."""
import re

from pydantic_avro.base import AvroBase  # type: ignore


class Message(AvroBase):  # type: ignore
    """Base model for events sent/received by clients."""

    def get_key(self) -> bytes:
        """Returns the message key to used by Kafka."""
        raise NotImplementedError("Please implement the method get_key")

    @classmethod
    def get_topic_name(cls) -> str:
        """Returns the topic name to be used for this message."""
        name = cls.__name__
        snake_case_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return snake_case_name
