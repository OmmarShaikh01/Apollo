from pathlib import PurePath
from typing import Any, Generator, Iterator, Union

import av
import mutagen

from apollo.media.decoders.decode import Stream
from apollo.utils import get_logger

LOGGER = get_logger(__name__)


class MP3_Decoder:

    def __init__(self, path: PurePath) -> None:
        self.file_path = path
        # noinspection PyUnresolvedReferences
        self.InputStream: av.container.InputContainer = av.open(str(self.file_path))
        self._decoder = self.decode()

    def decode(self) -> Iterator[av.audio.frame.AudioFrame]:
        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not (packet.size <= 0):
                for frame in packet.decode():
                    yield frame
            else:
                return None

    def get(self) -> av.audio.frame.AudioFrame:
        return next(self._decoder)

    def seek(self, time):
        self.InputStream.seek(int(time * av.time_base), any_frame = True)

    def reset_buffer(self):
        self.InputStream.close()
        # noinspection PyUnresolvedReferences
        self.InputStream = av.open(str(self.file_path))
        self._decoder = self.decode()


class MP3_File(Stream):

    def __init__(self, path: PurePath) -> None:
        super().__init__(path)

    # noinspection PyAttributeOutsideInit
    @property
    def Decoder(self) -> MP3_Decoder:
        if not hasattr(self, '_decoder'):
            self._decoder = MP3_Decoder(self.path)
        return self._decoder

    # noinspection PyAttributeOutsideInit
    @property
    def Tags(self) -> Any:
        if not hasattr(self, '_file_obj'):
            self._file_obj = mutagen.File(self.path)

        if not hasattr(self, '_tags'):
            tags = self._file_obj.tags
            self._tags = tags
        return self._tags

    # noinspection PyAttributeOutsideInit
    @property
    def SynthTags(self) -> dict:
        if hasattr(self, '_synth_tags'):
            return self._synth_tags

        self._synth_tags = dict.fromkeys(self.TAG_FRAMES, None)
        self._synth_tags["FILEID"] = self.stream_info['file_id']
        self._synth_tags["FILEPATH"] = self.stream_info['file_path']
        self._synth_tags["FILENAME"] = self.stream_info['file_name']
        self._synth_tags["FILESIZE"] = self.stream_info['file_size']
        self._synth_tags["FILEEXT"] = self.stream_info['file_ext']

        return self._synth_tags

    # noinspection PyAttributeOutsideInit
    @property
    def Artwork(self):
        pass
