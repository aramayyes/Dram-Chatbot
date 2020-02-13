from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from msg_recognizers import RecognizedMessage, MessageIntent


class BaseMsgRecognizer(ABC):
    """Provides a generic logic for recognizing a message based on command-words."""

    @property
    @abstractmethod
    def _commands(self) -> Dict[str, List[str]]:
        """A dictionary with commands as keys and command synonyms as values."""
        pass

    @property
    @abstractmethod
    def _intent(self) -> MessageIntent:
        """Message intent for all messages which will be recognized by this recognizer."""
        pass

    def recognize(self, message: str) -> Optional[RecognizedMessage]:
        """
        Tries to recognize the given message, by searching a command from :py:attr:`_commands` in that message.

        :param message: Message which should be recognized
        :return RecognizedMessage:
        """
        # Convert the message to lowercase letters,
        #   remove the very first '/' sign and replace all '_' signs with spaces (' '),
        #   which are used for commands in telegram
        message = message.lower()
        message = message.strip()
        message = message.replace('_', ' ')
        if message.startswith('/'):
            message = message[1:]

        # For each command (and its synonyms) check whether the message contains it
        #   and if so, then set that command as the message action, and the other words as params.
        result = RecognizedMessage(self._intent)
        for command, synonyms in self._commands.items():
            for synonym in synonyms:
                new_message = message.replace(synonym, '', 1)
                if new_message != message:
                    result.action = command
                    result.params = new_message.strip().split(' ')
                    break

        # Return none if the message didn't contain any of the commands
        if result.action is None:
            return None
        else:
            return result
