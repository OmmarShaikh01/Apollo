import json
import os
from pathlib import PurePath
from typing import Any, Union

import av
from mutagen.id3 import APIC

from apollo.media.decoders.decode import Stream
from apollo.media.decoders.mp3 import MP3_File
from apollo.utils import get_logger
from configs import settings


LOGGER = get_logger(__name__)
CONFIG = settings


class Mediafile:
    """
    Mediafile class for all Media handling
    """

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
        return json.dumps(self._stream.SynthTags, indent=2)

    def __bool__(self):
        if self._stream is not None:
            return bool(self._stream)
        return False

    # pylint: disable=R1710
    def _get_stream(self) -> Stream:
        """
        Gets stream

        Returns:
            (Stream): media stream
        """
        ext = str(self.path.suffix).lower().replace(".", "")
        if ext == "mp3":
            return MP3_File(self.path)

    def get_frame(self) -> av.audio.frame.AudioFrame:
        """
        Gets a decoded audio frame

        Returns:
            av.audio.frame.AudioFrame: Audio frame
        """
        return self.Decoder.get()

    @property
    def Decoder(self) -> Any:
        """
        Decoder attribute

        Returns:
            (Any): Decoder object
        """
        return self._stream.Decoder

    @property
    def Tags(self) -> Any:
        """
        Returns media tags

        Returns:
            (Any): Media tags
        """
        return self._stream.Tags

    @property
    def SynthTags(self) -> dict:
        """
        Syntethic Tags generated during runtime

        Returns:
            (dict): Syntethic Tags
        """
        return self._stream.SynthTags

    @property
    def Artwork(self) -> list[APIC]:
        """
        Album artwork for media

        Returns:
            (list): Artworks
        """
        return self._stream.Artwork

    @property
    def Records(self) -> dict:
        """
        Returns tags with respective fields

        Returns:
            (dict): Flattened representation of all tags in a dict
        """
        return self._stream.Records

    # noinspection PyAttributeOutsideInit
    @property
    def Info(self) -> dict:
        """
        Gets stream information

        Returns:
            (dict): stream information
        """
        return self._stream.stream_info

    @staticmethod
    def isSupported(path: Union[str, PurePath]) -> bool:
        """
        Validator for supported file types

        Args:
            path (Union[str, PurePath]): file path

        Returns:
            bool: if valid returns true, otherwise false
        """
        if isinstance(path, str):
            path = PurePath(path)
        enabled = settings.enabled_formats
        path = str(path.suffix).lower().replace(".", "")
        return bool(path in enabled)
