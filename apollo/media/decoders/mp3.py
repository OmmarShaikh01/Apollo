import warnings
from pathlib import PurePath
from typing import Any, Iterator, Optional, Union

import av
import mutagen
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from apollo.media.decoders.decode import Stream
from apollo.utils import get_logger
from configs import settings

CONFIG = settings
LOGGER = get_logger(__name__)


class MP3_Decoder:
    """
    Decoder class for handling MP3 files
    """

    def __init__(self, path: PurePath) -> None:
        """
        Constructor

        Returns:
            path (PurePath): path to the file to decode
        """
        self.file_path = path
        # noinspection PyUnresolvedReferences
        self.InputStream: av.container.InputContainer = av.open(str(self.file_path))
        self.resampler = av.AudioResampler(format = CONFIG.server.format, rate = CONFIG.server.rate,
                                           layout = CONFIG.server.chnl)
        self._decoder = self.decode()

    def decode(self) -> Iterator[av.AudioFrame]:
        """
        Generator object to get AudioFrames

        Returns:
            Iterator[av.AudioFrame]: Iterator object to get AudioFrames
        """
        # actual decoding and demuxing of file
        for packet in self.InputStream.demux(audio = 0):
            if not (packet.size <= 0):
                for frame in packet.decode():
                    for resam_frame in self.resampler.resample(frame):
                        yield resam_frame
            else:
                return None

    def get(self) -> av.AudioFrame:
        """
        Getter callback to get a frame

        Returns:
            av.AudioFrame: Decoded AudioFrame
        """
        return next(self._decoder)

    def seek(self, time: float):
        """
        Seeks to a given time in the audio buffer

        Args:
            time (float): Time to seek to
        """
        self.InputStream.seek(int(time * av.time_base), any_frame = True)

    def reset_buffer(self):
        """
        Resets the file pointer to the start of the file
        """
        self.InputStream.close()
        # noinspection PyUnresolvedReferences
        self.InputStream = av.open(str(self.file_path))
        self._decoder = self.decode()


class MP3_File(Stream):
    """
    File Handler for MP3 format
    """

    # noinspection SpellCheckingInspection
    V2_2 = [('CONTENTGROUP', 'TT1'), ('TITLE', 'TT2'), ('SUBTITLE', 'TT3'), ('ARTIST', 'TP1'), ('BAND', 'TP2'),
            ('CONDUCTOR', 'TP3'), ('MIXARTIST', 'TP4'), ('COMPOSER', 'TCM'), ('LYRICIST', 'TXT'), ('LANGUAGE', 'TLA'),
            ('CONTENTTYPE', 'TCO'), ('ALBUM', 'TAL'), ('TRACKNUM', 'TRK'), ('PARTINSET', 'TPA'), ('ISRC', 'TRC'),
            ('DATE', 'TDA'), ('YEAR', 'TYE'), ('TIME', 'TIM'), ('RECORDINGDATES', 'TRD'), ('RECORDINGTIME', 'EMPTY'),
            ('ORIGYEAR', 'TOR'), ('ORIGRELEASETIME', 'EMPTY'), ('BPM', 'TBP'), ('MEDIATYPE', 'TMT'),
            ('FILETYPE', 'TFT'), ('COPYRIGHT', 'TCR'), ('PUBLISHER', 'TPB'), ('ENCODEDBY', 'TEN'),
            ('ENCODERSETTINGS', 'TSS'), ('SONGLEN', 'TLE'), ('SIZE', 'TSI'), ('INITIALKEY', 'TKE'),
            ('ORIGALBUM', 'TOT'), ('ORIGFILENAME', 'TOF'), ('ORIGARTIST', 'TOA'), ('ORIGLYRICIST', 'TOL'),
            ('FILEOWNER', 'TOWN'), ('NETRADIOSTATION', 'EMPTY'), ('NETRADIOOWNER', 'EMPTY'), ('SETSUBTITLE', 'EMPTY'),
            ('MOOD', 'EMPTY'), ('PRODUCEDNOTICE', 'EMPTY'), ('ENCODINGTIME', 'EMPTY'), ('RELEASETIME', 'EMPTY'),
            ('TAGGINGTIME', 'EMPTY'), ('ALBUMSORTORDER', 'EMPTY'), ('PERFORMERSORTORDER', 'EMPTY'),
            ('TITLESORTORDER', 'EMPTY'), ('USERTEXT', 'TXX'), ('WWWAUDIOFILE', 'WAF'), ('WWWARTIST', 'WAR'),
            ('WWWAUDIOSOURCE', 'WAS'), ('WWWCOMMERCIALINFO', 'WCM'), ('WWWCOPYRIGHT', 'WCP'), ('WWWPUBLISHER', 'WPB'),
            ('WWWRADIOPAGE', 'EMPTY'), ('WWWPAYMENT', 'EMPTY'), ('WWWUSER', 'WXX'), ('INVOLVEDPEOPLE', 'IPL'),
            ('MUSICIANCREDITLIST', 'EMPTY'), ('INVOLVEDPEOPLE2', 'EMPTY'), ('UNSYNCEDLYRICS', 'ULT'),
            ('COMMENT', 'COM'), ('CDID', 'MCI'), ('EVENTTIMING', 'ETC'), ('PICTURE', 'PIC'), ('GENERALOBJECT', 'GEO'),
            ('PLAYCOUNTER', 'CNT'), ('POPULARIMETER', 'POP'), ('AUDIOCRYPTO', 'CRA'), ('LINKEDINFO', 'LNK'),
            ('POSITIONSYNC', 'EMPTY'), ('COMMERCIAL', 'EMPTY')]
    # noinspection SpellCheckingInspection
    V2_3 = [('CONTENTGROUP', 'TIT1'), ('TITLE', 'TIT2'), ('SUBTITLE', 'TIT3'), ('ARTIST', 'TPE1'), ('BAND', 'TPE2'),
            ('CONDUCTOR', 'TPE3'), ('MIXARTIST', 'TPE4'), ('COMPOSER', 'TCOM'), ('LYRICIST', 'TEXT'),
            ('LANGUAGE', 'TLAN'), ('CONTENTTYPE', 'TCON'), ('ALBUM', 'TALB'), ('TRACKNUM', 'TRCK'),
            ('PARTINSET', 'TPOS'), ('ISRC', 'TSRC'), ('DATE', 'TDAT'), ('YEAR', 'TYER'), ('TIME', 'TIME'),
            ('RECORDINGDATES', 'TRDA'), ('RECORDINGTIME', 'EMPTY'), ('ORIGYEAR', 'TORY'), ('ORIGRELEASETIME', 'EMPTY'),
            ('BPM', 'TBPM'), ('MEDIATYPE', 'TMED'), ('FILETYPE', 'TFLT'), ('COPYRIGHT', 'TCOP'), ('PUBLISHER', 'TPUB'),
            ('ENCODEDBY', 'TENC'), ('ENCODERSETTINGS', 'TSSE'), ('SONGLEN', 'TLEN'), ('SIZE', 'TSIZ'),
            ('INITIALKEY', 'TKEY'), ('ORIGALBUM', 'TOAL'), ('ORIGFILENAME', 'TOFN'), ('ORIGARTIST', 'TOPE'),
            ('ORIGLYRICIST', 'TOLY'), ('FILEOWNER', 'TOWN'), ('NETRADIOSTATION', 'TRSN'), ('NETRADIOOWNER', 'TRSO'),
            ('SETSUBTITLE', 'EMPTY'), ('MOOD', 'EMPTY'), ('PRODUCEDNOTICE', 'EMPTY'), ('ENCODINGTIME', 'EMPTY'),
            ('RELEASETIME', 'EMPTY'), ('TAGGINGTIME', 'EMPTY'), ('ALBUMSORTORDER', 'EMPTY'),
            ('PERFORMERSORTORDER', 'EMPTY'), ('TITLESORTORDER', 'EMPTY'), ('USERTEXT', 'TXXX'),
            ('WWWAUDIOFILE', 'WOAF'), ('WWWARTIST', 'WOAR'), ('WWWAUDIOSOURCE', 'WOAS'), ('WWWCOMMERCIALINFO', 'WCOM'),
            ('WWWCOPYRIGHT', 'WCOP'), ('WWWPUBLISHER', 'WPUB'), ('WWWRADIOPAGE', 'WORS'), ('WWWPAYMENT', 'WPAY'),
            ('WWWUSER', 'WXXX'), ('INVOLVEDPEOPLE', 'IPLS'), ('MUSICIANCREDITLIST', 'EMPTY'),
            ('INVOLVEDPEOPLE2', 'EMPTY'), ('UNSYNCEDLYRICS', 'USLT'), ('COMMENT', 'COMM'), ('CDID', 'MCDI'),
            ('EVENTTIMING', 'ETCO'), ('PICTURE', 'APIC'), ('GENERALOBJECT', 'GEOB'), ('PLAYCOUNTER', 'PCNT'),
            ('POPULARIMETER', 'POPM'), ('AUDIOCRYPTO', 'AENC'), ('LINKEDINFO', 'LINK'), ('POSITIONSYNC', 'POSS'),
            ('COMMERCIAL', 'COMR')]
    # noinspection SpellCheckingInspection
    V2_4 = [('CONTENTGROUP', 'TIT1'), ('TITLE', 'TIT2'), ('SUBTITLE', 'TIT3'), ('ARTIST', 'TPE1'), ('BAND', 'TPE2'),
            ('CONDUCTOR', 'TPE3'), ('MIXARTIST', 'TPE4'), ('COMPOSER', 'TCOM'), ('LYRICIST', 'TEXT'),
            ('LANGUAGE', 'TLAN'), ('CONTENTTYPE', 'TCON'), ('ALBUM', 'TALB'), ('TRACKNUM', 'TRCK'),
            ('PARTINSET', 'TPOS'), ('ISRC', 'TSRC'), ('DATE', 'EMPTY'), ('YEAR', 'EMPTY'), ('TIME', 'EMPTY'),
            ('RECORDINGDATES', 'EMPTY'), ('RECORDINGTIME', 'TDRC'), ('ORIGYEAR', 'EMPTY'), ('ORIGRELEASETIME', 'TDOR'),
            ('BPM', 'TBPM'), ('MEDIATYPE', 'TMED'), ('FILETYPE', 'TFLT'), ('COPYRIGHT', 'TCOP'), ('PUBLISHER', 'TPUB'),
            ('ENCODEDBY', 'TENC'), ('ENCODERSETTINGS', 'TSSE'), ('SONGLEN', 'TLEN'), ('SIZE', 'EMPTY'),
            ('INITIALKEY', 'TKEY'), ('ORIGALBUM', 'TOAL'), ('ORIGFILENAME', 'TOFN'), ('ORIGARTIST', 'TOPE'),
            ('ORIGLYRICIST', 'TOLY'), ('FILEOWNER', 'EMPTY'), ('NETRADIOSTATION', 'TRSN'), ('NETRADIOOWNER', 'TRSO'),
            ('SETSUBTITLE', 'TSST'), ('MOOD', 'TMOO'), ('PRODUCEDNOTICE', 'TPRO'), ('ENCODINGTIME', 'TDEN'),
            ('RELEASETIME', 'TDRL'), ('TAGGINGTIME', 'TDTG'), ('ALBUMSORTORDER', 'TSOA'),
            ('PERFORMERSORTORDER', 'TSOP'), ('TITLESORTORDER', 'TSOT'), ('USERTEXT', 'TXXX'), ('WWWAUDIOFILE', 'WOAF'),
            ('WWWARTIST', 'WOAR'), ('WWWAUDIOSOURCE', 'WOAS'), ('WWWCOMMERCIALINFO', 'WCOM'), ('WWWCOPYRIGHT', 'WCOP'),
            ('WWWPUBLISHER', 'WPUB'), ('WWWRADIOPAGE', 'WORS'), ('WWWPAYMENT', 'WPAY'), ('WWWUSER', 'WXXX'),
            ('INVOLVEDPEOPLE', 'EMPTY'), ('MUSICIANCREDITLIST', 'TMCL'), ('INVOLVEDPEOPLE2', 'TIPL'),
            ('UNSYNCEDLYRICS', 'USLT'), ('COMMENT', 'COMM'), ('CDID', 'MCDI'), ('EVENTTIMING', 'ETCO'),
            ('PICTURE', 'APIC'), ('GENERALOBJECT', 'GEOB'), ('PLAYCOUNTER', 'PCNT'), ('POPULARIMETER', 'POPM'),
            ('AUDIOCRYPTO', 'AENC'), ('LINKEDINFO', 'LINK'), ('POSITIONSYNC', 'POSS'), ('COMMERCIAL', 'COMR')]

    def __init__(self, path: PurePath) -> None:
        """
        Constructor

        Args:
            path: Path to an MP3 fiel to handle
        """
        super().__init__(path)
        self._file_obj = MP3(self.path)

    def parse_tags_into(self, tags: ID3, into: dict) -> Union[dict[Any, Any], None]:
        """
        Parses the tags according to the ID3 version.

        Args:
            tags (ID3): ID3 tag dict
            into (dict): dict to parse into

        Returns:
            dict: filled dict
        """
        if tags.version == (2, 2, 0):
            parser = self.V2_2
        elif tags.version == (2, 3, 0):
            parser = self.V2_3
        elif tags.version == (2, 4, 0):
            parser = self.V2_4
        else:
            LOGGER.warning(f"Parser doesnt support Version {tags.version}")
            warnings.warn(f"Parser doesnt support Version {tags.version}")
            return None

        tags_dict = into
        for (frame_key, tag_key) in parser:
            if frame_key in self.TAG_FRAMES:
                if tag_key == 'EMPTY':
                    tags_dict[frame_key] = []
                elif frame_key == 'PLAYCOUNTER':
                    tags_dict[frame_key] = [0 if len(tags.getall(tag_key)) == 0 else tags.getall(tag_key)[0].count]
                elif frame_key == 'POPULARIMETER':
                    tags_dict[frame_key] = [0 if len(tags.getall(tag_key)) == 0 else tags.getall(tag_key)[0].rating]
                elif frame_key == "PICTURE":
                    tags_dict[frame_key] = [False if len(tags.getall(tag_key)) == 0 else True]
                else:
                    tags_dict[frame_key] = list(map(str, tags.getall(tag_key)))
        return tags_dict

    # noinspection PyAttributeOutsideInit
    @property
    def Tags(self) -> ID3:
        """
        Mediafile Tags Getter

        Returns:
            ID3: ID3 Tags
        """
        if not hasattr(self, '_tags'):
            if self._file_obj.tags is None:
                self._file_obj.add_tags()
            self._tags = self._file_obj.tags
        return self._tags

    # noinspection PyAttributeOutsideInit
    @property
    def SynthTags(self) -> dict:
        """
        Mediafile SynthTags Getter

        Returns:
            dict: SynthTags dict
        """
        if hasattr(self, '_synth_tags'):
            return self._synth_tags

        # load empty
        self._synth_tags = dict.fromkeys(self.TAG_FRAMES, [])

        # Parse tags by frames
        self.parse_tags_into(self.Tags, self._synth_tags)

        # sets stream info
        self._synth_tags["FILEID"] = [self.stream_info['file_id']]
        self._synth_tags["FILEPATH"] = [self.stream_info['file_path']]
        self._synth_tags["FILENAME"] = [self.stream_info['file_name']]
        self._synth_tags["FILESIZE"] = [self.stream_info['file_size']]
        self._synth_tags["SIZE"] = [self.stream_info['file_size']]
        self._synth_tags["FILEEXT"] = [self.stream_info['file_ext']]

        info = self._file_obj.info
        self._synth_tags["SONGLEN"] = [info.length]
        self._synth_tags["BITRATE"] = [info.bitrate]
        self._synth_tags["CHANNELS"] = [info.channels]
        self._synth_tags["SAMPLERATE"] = [info.sample_rate]
        self._synth_tags["BITRATEMODE"] = [int(info.bitrate_mode)]
        self._synth_tags["TRACKGAIN"] = [0 if info.track_gain is None else info.track_gain]
        self._synth_tags["TRACKPEAK"] = [0 if info.track_peak is None else info.track_peak]
        self._synth_tags["ALBUMGAIN"] = [0 if info.album_gain is None else info.album_gain]

        return self._synth_tags

    # noinspection PyAttributeOutsideInit
    @property
    def Artwork(self) -> list[bytes]:
        """
        Mediafile Artwork Getter

        Returns:
            list[bytes]: List of Cover images saved in the tag
        """
        if not hasattr(self, '_art'):
            tags = self.Tags
            if tags.version == (2, 2, 0):
                parser = self.V2_2
            elif tags.version == (2, 3, 0):
                parser = self.V2_3
            elif tags.version == (2, 4, 0):
                parser = self.V2_4
            else:
                LOGGER.warning(f"Parser doesnt support Version {tags.version}")
                warnings.warn(f"Parser doesnt support Version {tags.version}")
                return []

            for (frame_key, tag_key) in parser:
                if frame_key == "PICTURE":
                    self._art = tags.getall(tag_key)
                    break
        return self._art

    # noinspection PyAttributeOutsideInit
    @property
    def Decoder(self) -> MP3_Decoder:
        """
        Mediafile Decoder Getter

        Returns:
            MP3_Decoder: Decoder for the file type
        """
        if not hasattr(self, '_decoder'):
            self._decoder = MP3_Decoder(self.path)
        return self._decoder

    # noinspection PyAttributeOutsideInit
    @property
    def Records(self) -> dict:
        """
        Mediafile Records Getter

        Returns:
            dict: Flattened representation of all tags in a dict
        """
        tags = dict.fromkeys(self.TAG_FRAMES, None)
        for k, v in self.SynthTags.items():
            for f, dt in self.TAG_FRAMES_FIELDS:
                if k == f and len(v) > 0:
                    if dt == "STRING":
                        tags[k] = str(v[0])
                    elif dt == "INTEGER":
                        tags[k] = int(v[0])
                    else:
                        continue
        return tags
