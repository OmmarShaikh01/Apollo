import copy
import hashlib
import os

import music_tag

from apollo.media.decoders import MP3_Decoder, WAV_Decoder


class Mediafile:
    tags_fields = (
        'file_id',
        'file_name',
        'file_path',
        'tracktitle',
        'artist',
        'album',
        'albumartist',
        'composer',
        'tracknumber',
        'totaltracks',
        'discnumber',
        'totaldiscs',
        'genre',
        'year',
        'compilation',
        'lyrics',
        'isrc',
        'comment',
        'artwork',
        'bitrate',
        'codec',
        'length',
        'channels',
        'bitspersample',
        'samplerate'
    )

    def __init__(self, path) -> None:
        self.path = os.path.normpath(path)
        self.file_obj = None
        self.tags = dict.fromkeys(self.tags_fields, "")

    @property
    def Decoder(self):
        ext = str(os.path.splitext(self.path)[1]).lower().replace(".", "")
        if ext == 'wav':
            self.decoder = WAV_Decoder(self.path)
            return self.decoder
        if ext == 'mp3':
            self.decoder = MP3_Decoder(self.path)
            return self.decoder
        else:
            return None

    @property
    def File(self):
        if self.isSupported(self.path):
            self.file_obj = music_tag.load_file(self.path)
        return self.file_obj

    @property
    def Tags(self):
        self.tags['tracktitle'] = str(self.File['tracktitle'])
        self.tags['artist'] = str(self.File['artist'])
        self.tags['album'] = str(self.File['album'])
        self.tags['albumartist'] = str(self.File['albumartist'])
        self.tags['composer'] = str(self.File['composer'])
        self.tags['tracknumber'] = str(self.File['tracknumber'])
        self.tags['totaltracks'] = str(self.File['totaltracks'])
        self.tags['discnumber'] = str(self.File['discnumber'])
        self.tags['totaldiscs'] = str(self.File['totaldiscs'])
        self.tags['genre'] = str(self.File['genre'])
        self.tags['year'] = str(self.File['year'])
        self.tags['compilation'] = str(self.File['compilation'])
        self.tags['lyrics'] = str(self.File['lyrics'])
        self.tags['isrc'] = str(self.File['isrc'])
        self.tags['comment'] = str(self.File['comment'])
        self.tags['artwork'] = str(self.File['artwork'])
        self.tags['bitrate'] = str(self.File['#bitrate'])
        self.tags['length'] = str(self.File['#length'])
        self.tags['channels'] = str(self.File['#channels'])
        self.tags['bitspersample'] = str(self.File['#bitspersample'])
        self.tags['samplerate'] = str(self.File['#samplerate'])
        self.tags['codec'] = str(os.path.splitext(self.path)[1]).lower().replace(".", "")
        return self.tags

    @property
    def SynthTags(self):
        tags = copy.deepcopy(self.Tags)
        tags['file_id'] = self.FileHash
        tags['file_name'] = os.path.split(self.path)[1]
        tags['file_path'] = self.path
        return tags

    @property
    def FileHash(self):
        with open(self.path, "rb") as fobj:
            return (hashlib.md5(fobj.read(1024 * 10))).hexdigest()

    @property
    def Artwork(self) -> bytes:
        art = self.File['artwork'].first
        try:
            if art is None:
                raise ValueError()
            else:
                return art.data
        except ValueError:
            return b''

    @staticmethod
    def isSupported(path) -> bool:
        supported = [".mp3"]
        path = str(os.path.splitext(path)[1]).lower()
        if path in supported:
            return True
        else:
            return False
