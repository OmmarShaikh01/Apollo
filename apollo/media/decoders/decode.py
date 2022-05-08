import hashlib
import os
from abc import ABC, abstractmethod
from pathlib import PurePath
from typing import Union


class Stream(ABC):
    # noinspection SpellCheckingInspection
    TAG_FRAMES = (
        "FILEID", "FILEPATH", "FILENAME", "FILESIZE", "FILEEXT", 'CONTENTGROUP', 'TITLE', 'SUBTITLE', 'ARTIST', 'BAND',
        'CONDUCTOR', 'MIXARTIST', 'COMPOSER', 'LYRICIST', 'LANGUAGE', 'CONTENTTYPE', 'ALBUM', 'TRACKNUM', 'PARTINSET',
        'ISRC', 'DATE', 'YEAR', 'TIME', 'RECORDINGDATES', 'RECORDINGTIME', 'ORIGYEAR', 'ORIGRELEASETIME', 'BPM',
        'MEDIATYPE', 'FILETYPE', 'COPYRIGHT', 'PUBLISHER', 'ENCODEDBY', 'ENCODERSETTINGS', 'SONGLEN', 'SIZE',
        'PLAYLISTDELAY', 'INITIALKEY', 'ORIGALBUM', 'ORIGFILENAME', 'ORIGARTIST', 'ORIGLYRICIST', 'FILEOWNER',
        'NETRADIOSTATION', 'NETRADIOOWNER', 'SETSUBTITLE', 'MOOD', 'PRODUCEDNOTICE', 'ENCODINGTIME', 'RELEASETIME',
        'TAGGINGTIME', 'ALBUMSORTORDER', 'PERFORMERSORTORDER', 'TITLESORTORDER', 'USERTEXT', 'WWWAUDIOFILE',
        'WWWARTIST', 'WWWAUDIOSOURCE', 'WWWCOMMERCIALINFO', 'WWWCOPYRIGHT', 'WWWPUBLISHER', 'WWWRADIOPAGE',
        'WWWPAYMENT', 'WWWUSER', 'INVOLVEDPEOPLE', 'MUSICIANCREDITLIST', 'INVOLVEDPEOPLE2', 'UNSYNCEDLYRICS', 'COMMENT',
        'TERMSOFUSE', 'UNIQUEFILEID', 'CDID', 'EVENTTIMING', 'MPEGLOOKUP', 'SYNCEDTEMPO', 'SYNCEDLYRICS', 'VOLUMEADJ',
        'VOLUMEADJ2', 'EQUALIZATION', 'EQUALIZATION2', 'REVERB', 'PICTURE', 'GENERALOBJECT', 'PLAYCOUNTER',
        'POPULARIMETER', 'BUFFERSIZE', 'CRYPTEDMETA', 'AUDIOCRYPTO', 'LINKEDINFO', 'POSITIONSYNC', 'COMMERCIAL',
        'CRYPTOREG', 'GROUPINGREG', 'PRIVATE', 'OWNERSHIP', 'SIGNATURE', 'SEEKFRAME', 'AUDIOSEEKPOINT',
    )

    def __init__(self, path: PurePath) -> None:
        self.path = path
        with open(self.path, "rb") as fobj:
            self.stream_info = dict(
                file_id = (hashlib.md5(fobj.read(1024 * 10))).hexdigest(),
                file_path = str(self.path.as_posix()),
                file_name = self.path.name,
                file_size = os.path.getsize(self.path),
                file_ext = self.path.suffix
            )
        super().__init__()

    @property
    @abstractmethod
    def Decoder(self):
        pass

    @property
    @abstractmethod
    def Tags(self):
        pass

    @property
    @abstractmethod
    def SynthTags(self):
        pass

    @property
    @abstractmethod
    def Artwork(self):
        pass
