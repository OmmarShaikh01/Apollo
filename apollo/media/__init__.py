import json
import os
from pathlib import PurePath
from typing import Any, Union

from apollo.media.decoders.decode import Stream
from apollo.media.decoders.mp3 import MP3_File
from apollo.utils import get_logger
from configs import settings

LOGGER = get_logger(__name__)
CONFIG = settings


class Mediafile:
    TAG_FRAMES = Stream.TAG_FRAMES

    def __init__(self, path: Union[str, PurePath]):
        if self.isSupported(path):
            if isinstance(path, str):
                self.path = PurePath(path)
            else:
                self.path = path
            LOGGER.debug(f"Read {self.path}")
            self._stream = self._get_stream()
        else:
            LOGGER.error(f"Failed to read {path}")
            raise NotImplementedError(str(os.path.splitext(path)[1]).lower())

    def __str__(self):
        return json.dumps(self._stream.SynthTags, indent = 2)

    def __bool__(self):
        if self._stream is not None:
            return True
        else:
            return False

    def _get_stream(self):
        ext = str(self.path.suffix).lower().replace(".", "")
        if ext == 'mp3':
            return MP3_File(self.path)
        else:
            return None

    @property
    def Decoder(self) -> Union[Any, None]:
        if self._stream is not None:
            return self._stream.Decoder
        else:
            return None

    @property
    def Tags(self) -> Union[dict, None]:
        if self._stream is not None:
            return self._stream.Tags
        else:
            return None

    @property
    def SynthTags(self) -> Union[Any, None]:
        if self._stream is not None:
            return self._stream.SynthTags
        else:
            return None

    @property
    def Artwork(self) -> Union[Any, None]:
        if self._stream is not None:
            return self._stream.Artwork
        else:
            return None

    @staticmethod
    def isSupported(path: Union[str, PurePath]) -> bool:
        if isinstance(path, str):
            path = PurePath(path)
        enabled = settings.enabled_formats
        path = str(path.suffix).lower().replace(".", "")
        if path in enabled:
            return True
        else:
            return False
