import os, sys, datetime

from mutagen import easyid3
import mutagen

DBFIELDS = ["file_id", "path_id","file_name","file_path","album",
            "albumartist","artist","author","bpm","compilation",
            "composer","conductor","date","discnumber","discsubtitle",
            "encodedby","genre","language","length","filesize",
            "lyricist","media","mood","organization","originaldate",
            "performer","releasecountry","replaygain_gain","replaygain_peak",
            "title","tracknumber","version","website","album_gain",
            "bitrate","bitrate_mode","channels","encoder_info","encoder_settings",
            "frame_offset","layer","mode","padding","protected","sample_rate",
            "track_gain","track_peak", "rating", "playcount"]

# FileEXT Support

# ASF  -> No
# FLAC -> Yes
# MP4 -> Yes
# Monkey’s Audio -> No
# MP3 -> Yes
# Musepack -> No 
# Ogg Opus -> No
# Ogg FLAC -> No
# Ogg Speex -> No
# Ogg Theora -> No
# Ogg Vorbis -> No
# True Audio -> No
# WavPack -> Yes
# OptimFROG -> No
# AIFF -> No


class MP3:
    """
    MP3 File format metadata reader class
    """
    def __init__(self, path):
        self.FILEPATH = path
        
    def GetMetadata(self):
        Media = mutagen.File(self.FILEPATH, easy = True)
        metadata = dict.fromkeys(DBFIELDS, "")

        for key in Media.keys():
            metadata[key] = Media.get(key, "NA")[0]
        metadata["bitrate_mode"] = str(Media.info.bitrate_mode).replace('BitrateMode', "").replace('.', "")
        metadata['album_gain'] = Media.info.album_gain
        metadata['encoder_info'] = Media.info.encoder_info
        metadata['encoder_settings'] = Media.info.encoder_settings
        metadata['frame_offset'] = Media.info.frame_offset
        metadata['layer'] = Media.info.layer
        metadata['mode'] = Media.info.mode
        metadata['padding'] = Media.info.padding
        metadata['protected'] = Media.info.protected
        metadata['track_gain'] = Media.info.track_gain
        metadata['track_peak'] = Media.info.track_peak
        metadata['version'] = Media.info.version
        metadata['sample_rate'] = f"{Media.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = Media.info.length))
        metadata["bitrate"] = f"{int(Media.info.bitrate / 1000)} Kbps"
        metadata['channels'] = Media.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(Media.filename) * 0.00000095367432, 2)} Mb"
        metadata["file_name"] = os.path.split(Media.filename)[1]
        metadata["file_path"] = Media.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
        return metadata
    
    def GetArtwork(self):
        Media = mutagen.File(self.FILEPATH)
        Artwork = Media.tags.getall("APIC:")
        Artwork = {int(data.type): data.data for data in Artwork}
        return Artwork 
        
        
class WAVE:
    
    def __init__(self, path):
        self.FILEPATH = path
        
    def GetMetadata(self):
        Media = easyid3.EasyID3FileType(self.FILEPATH)
        metadata = dict.fromkeys(DBFIELDS, "")

        for key in Media.keys():
            metadata[key] = Media.get(key, "NA")[0]
        
        Media = mutagen.File(self.FILEPATH, easy = True)
        metadata['sample_rate'] = f"{Media.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = Media.info.length))
        metadata["bitrate"] = f"{int(Media.info.bitrate / 1000)} Kbps"
        metadata['channels'] = Media.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(Media.filename) * 0.00000095367432, 2)} Mb"
        metadata["file_name"] = os.path.split(Media.filename)[1]
        metadata["file_path"] = Media.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
        return metadata
    
    def GetArtwork(self):
        Media = mutagen.File(self.FILEPATH)
        Artwork = Media.tags.getall("APIC:")
        Artwork = {int(data.type): data.data for data in Artwork}
        return Artwork
    
    
class FLAC:
    
    def __init__(self, path):
        self.FILEPATH = path
        
    def GetMetadata(self):
        Media = mutagen.File(self.FILEPATH, easy = True)
        metadata = dict.fromkeys(DBFIELDS, "")

        for key in Media.keys():
            metadata[key] = Media.get(key, "NA")[0]
            
        metadata['encoder_info'] = Media.get("encoder")[0]
        metadata['sample_rate'] = f"{Media.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = Media.info.length))
        metadata["bitrate"] = f"{int(Media.info.bitrate / 1000)} Kbps"
        metadata['channels'] = Media.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(Media.filename) * 0.00000095367432, 2)} Mb"
        metadata["file_name"] = os.path.split(Media.filename)[1]
        metadata["file_path"] = Media.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
        return metadata
    
    def GetArtwork(self):
        Media = mutagen.File(self.FILEPATH)
        Artwork = Media.pictures
        Artwork = {int(data.type): data.data for data in Artwork}
        return Artwork 
    
class MP4:
    
    def __init__(self, path):
        self.FILEPATH = path
        
    def GetMetadata(self):
        Media = mutagen.File(self.FILEPATH, easy = True)
        metadata = dict.fromkeys(DBFIELDS, "")

        for key in Media.keys():
            metadata[key] = Media.get(key, "NA")[0]
        metadata['encoder_info'] = Media.info.codec_description
        metadata['encoder_settings'] = Media.info.codec
        metadata['sample_rate'] = f"{Media.info.sample_rate}Hz"
        metadata["length"] = str(datetime.timedelta(seconds = Media.info.length))
        metadata["bitrate"] = f"{int(Media.info.bitrate / 1000)} Kbps"
        metadata['channels'] = Media.info.channels
        metadata["filesize"] = f"{round(os.path.getsize(Media.filename) * 0.00000095367432, 2)} Mb"
        metadata["file_name"] = os.path.split(Media.filename)[1]
        metadata["file_path"] = Media.filename
        metadata["rating"] = 0
        metadata["playcount"] = 0
        return metadata
    
    def GetArtwork(self):
        Media = mutagen.File(self.FILEPATH)
        Artwork = Media.tags.get("covr")
        Artwork = {3: data for data in Artwork}
        return Artwork 