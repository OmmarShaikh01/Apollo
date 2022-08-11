import hashlib
import json
import os
from abc import ABC, abstractmethod
from pathlib import PurePath
from typing import Any

from mutagen.id3 import APIC


class Stream(ABC):
    """
    Abstract Base class for all media classes
    """

    # noinspection SpellCheckingInspection
    TAG_FRAMES = (
        "FILEID",
        "FILEPATH",
        "FILENAME",
        "FILESIZE",
        "FILEEXT",
        "CONTENTGROUP",
        "TITLE",
        "SUBTITLE",
        "ARTIST",
        "BAND",
        "CONDUCTOR",
        "MIXARTIST",
        "COMPOSER",
        "LYRICIST",
        "LANGUAGE",
        "CONTENTTYPE",
        "ALBUM",
        "TRACKNUM",
        "PARTINSET",
        "ISRC",
        "DATE",
        "YEAR",
        "TIME",
        "RECORDINGDATES",
        "RECORDINGTIME",
        "ORIGYEAR",
        "ORIGRELEASETIME",
        "BPM",
        "MEDIATYPE",
        "FILETYPE",
        "COPYRIGHT",
        "PUBLISHER",
        "ENCODEDBY",
        "ENCODERSETTINGS",
        "SONGLEN",
        "SIZE",
        "INITIALKEY",
        "ORIGALBUM",
        "ORIGFILENAME",
        "ORIGARTIST",
        "ORIGLYRICIST",
        "FILEOWNER",
        "NETRADIOSTATION",
        "NETRADIOOWNER",
        "SETSUBTITLE",
        "MOOD",
        "PRODUCEDNOTICE",
        "ENCODINGTIME",
        "RELEASETIME",
        "TAGGINGTIME",
        "ALBUMSORTORDER",
        "PERFORMERSORTORDER",
        "TITLESORTORDER",
        "USERTEXT",
        "WWWAUDIOFILE",
        "WWWARTIST",
        "WWWAUDIOSOURCE",
        "WWWCOMMERCIALINFO",
        "WWWCOPYRIGHT",
        "WWWPUBLISHER",
        "WWWRADIOPAGE",
        "WWWPAYMENT",
        "WWWUSER",
        "INVOLVEDPEOPLE",
        "MUSICIANCREDITLIST",
        "INVOLVEDPEOPLE2",
        "UNSYNCEDLYRICS",
        "COMMENT",
        "CDID",
        "EVENTTIMING",
        "PICTURE",
        "PLAYCOUNTER",
        "POPULARIMETER",
        "BITRATE",
        "CHANNELS",
        "SAMPLERATE",
        "BITRATEMODE",
        "TRACKGAIN",
        "TRACKPEAK",
        "ALBUMGAIN",
    )

    # noinspection SpellCheckingInspection
    TAG_FRAMES_FIELDS = (
        ("FILEID", "STRING"),
        ("FILEPATH", "STRING"),
        ("FILENAME", "STRING"),
        ("FILESIZE", "STRING"),
        ("FILEEXT", "STRING"),
        ("CONTENTGROUP", "STRING"),
        ("TITLE", "STRING"),
        ("SUBTITLE", "STRING"),
        ("ARTIST", "STRING"),
        ("BAND", "STRING"),
        ("CONDUCTOR", "STRING"),
        ("MIXARTIST", "STRING"),
        ("COMPOSER", "STRING"),
        ("LYRICIST", "STRING"),
        ("LANGUAGE", "STRING"),
        ("CONTENTTYPE", "STRING"),
        ("ALBUM", "STRING"),
        ("TRACKNUM", "STRING"),
        ("PARTINSET", "STRING"),
        ("ISRC", "STRING"),
        ("DATE", "STRING"),
        ("YEAR", "STRING"),
        ("TIME", "STRING"),
        ("RECORDINGDATES", "STRING"),
        ("RECORDINGTIME", "STRING"),
        ("ORIGYEAR", "STRING"),
        ("ORIGRELEASETIME", "STRING"),
        ("BPM", "STRING"),
        ("MEDIATYPE", "STRING"),
        ("FILETYPE", "STRING"),
        ("COPYRIGHT", "STRING"),
        ("PUBLISHER", "STRING"),
        ("ENCODEDBY", "STRING"),
        ("ENCODERSETTINGS", "STRING"),
        ("SONGLEN", "FLOAT"),
        ("SIZE", "STRING"),
        ("INITIALKEY", "STRING"),
        ("ORIGALBUM", "STRING"),
        ("ORIGFILENAME", "STRING"),
        ("ORIGARTIST", "STRING"),
        ("ORIGLYRICIST", "STRING"),
        ("FILEOWNER", "STRING"),
        ("NETRADIOSTATION", "STRING"),
        ("NETRADIOOWNER", "STRING"),
        ("SETSUBTITLE", "STRING"),
        ("MOOD", "STRING"),
        ("PRODUCEDNOTICE", "STRING"),
        ("ENCODINGTIME", "STRING"),
        ("RELEASETIME", "STRING"),
        ("TAGGINGTIME", "STRING"),
        ("ALBUMSORTORDER", "STRING"),
        ("PERFORMERSORTORDER", "STRING"),
        ("TITLESORTORDER", "STRING"),
        ("USERTEXT", "STRING"),
        ("WWWAUDIOFILE", "STRING"),
        ("WWWARTIST", "STRING"),
        ("WWWAUDIOSOURCE", "STRING"),
        ("WWWCOMMERCIALINFO", "STRING"),
        ("WWWCOPYRIGHT", "STRING"),
        ("WWWPUBLISHER", "STRING"),
        ("WWWRADIOPAGE", "STRING"),
        ("WWWPAYMENT", "STRING"),
        ("WWWUSER", "STRING"),
        ("INVOLVEDPEOPLE", "STRING"),
        ("MUSICIANCREDITLIST", "STRING"),
        ("INVOLVEDPEOPLE2", "STRING"),
        ("UNSYNCEDLYRICS", "STRING"),
        ("COMMENT", "STRING"),
        ("CDID", "STRING"),
        ("EVENTTIMING", "STRING"),
        ("PICTURE", "BOOLEAN"),
        ("PLAYCOUNTER", "INTEGER"),
        ("POPULARIMETER", "INTEGER"),
        ("BITRATE", "INTEGER"),
        ("CHANNELS", "INTEGER"),
        ("SAMPLERATE", "INTEGER"),
        ("BITRATEMODE", "INTEGER"),
        ("TRACKGAIN", "INTEGER"),
        ("TRACKPEAK", "INTEGER"),
        ("ALBUMGAIN", "INTEGER"),
    )

    def __init__(self, path: PurePath) -> None:
        self.path = path
        self.stream_info = self._get_stream_info()

    def __str__(self):  # pragma: no cover
        return json.dumps(self.SynthTags, indent=2)

    def __bool__(self):  # pragma: no cover
        return all(
            [
                (self.SynthTags.get("FILEID", "") != ""),
                (self.SynthTags.get("SONGLEN")[0] < (24 * 3600)),
            ]
        )

    def _file_id(self) -> str:
        """
        Generates file ids for files

        Returns:
            str: file ids
        """
        with open(self.path, "rb") as fobj:
            return (hashlib.md5(fobj.read(1024 * 10))).hexdigest()

    def _get_stream_info(self) -> dict:
        """
        Gets stream information

        Returns:
            (dict): stream information
        """
        return dict(
            file_id=self._file_id(),
            file_path=str(self.path.as_posix()),
            file_name=self.path.name,
            file_size=os.path.getsize(self.path),
            file_ext=self.path.suffix,
        )

    @property
    @abstractmethod  # pragma: no cover
    def Decoder(self) -> Any:
        """
        Decoder attribute

        Returns:
            (Any): Decoder object
        """

    @property
    @abstractmethod  # pragma: no cover
    def Tags(self) -> Any:
        """
        Returns media tags

        Returns:
            (Any): Media tags
        """

    @property
    @abstractmethod  # pragma: no cover
    def SynthTags(self) -> dict:
        """
        Syntethic Tags generated during runtime

        Returns:
            (dict): Syntethic Tags
        """

    @property
    @abstractmethod  # pragma: no cover
    def Artwork(self) -> list[APIC]:
        """
        Album artwork for media

        Returns:
            (list): Artworks
        """

    @property
    @abstractmethod  # pragma: no cover
    def Records(self) -> dict:
        """
        Returns tags with respective fields

        Returns:
            (dict): Flattened representation of all tags in a dict
        """
