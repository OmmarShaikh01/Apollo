import json
import os
from pathlib import PurePath
from typing import Any, Union

import av

from apollo.media.decoders.decode import Stream
from apollo.media.decoders.mp3 import MP3_File
from apollo.utils import get_logger
from configs import settings

LOGGER = get_logger(__name__)
CONFIG = settings


class Mediafile:
    TAG_FRAMES = Stream.TAG_FRAMES
    TAG_FRAMES_FIELDS = Stream.TAG_FRAMES_FIELDS

    def __init__(self, path: Union[str, PurePath]):
        if self.isSupported(path):
            if isinstance(path, str):
                self.path = PurePath(path)
            else:
                self.path = path
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

    def get_frame(self) -> av.audio.frame.AudioFrame:
        return self.Decoder.get()

    @property
    def Decoder(self) -> Any:
        if self._stream is not None:
            return self._stream.Decoder

    @property
    def Tags(self) -> Any:
        if self._stream is not None:
            return self._stream.Tags

    @property
    def SynthTags(self) -> dict:
        if self._stream is not None:
            return self._stream.SynthTags

    @property
    def Artwork(self) -> list:
        if self._stream is not None:
            return self._stream.Artwork

    @property
    def Records(self) -> dict:
        if self._stream is not None:
            return self._stream.Records

    # noinspection PyAttributeOutsideInit
    @property
    def Info(self) -> dict:
        if self._stream is not None:
            return self._stream.stream_info

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
