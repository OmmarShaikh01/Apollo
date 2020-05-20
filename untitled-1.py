
a = """(id, path_id, path, album_id, title, artist, rating, 
artist_sort, artist_credit, album, albumartist, albumartist_sort, albumartist_credit, 
genre, lyricist, composer, composer_sort, arranger, grouping, 
year, month, day, track, tracktotal, disc, 
disctotal, lyrics, comments, bpm, comp, mb_trackid, 
mb_albumid, mb_artistid, mb_albumartistid, mb_releasetrackid, albumtype, label, 
acoustid_fingerprint, acoustid_id, mb_releasegroupid, asin, catalognum, script,
language, country, albumstatus, media, albumdisambig, releasegroupdisambig,
disctitle, encoder, rg_track_gain, rg_track_peak, rg_album_gain, rg_album_peak,
r128_track_gain, r128_album_gain, original_year,original_month,original_day,initial_key,
length, bitrate, format, samplerate, bitdepth, channels,
mtime, added, file_size)"""
a = ((((a.replace(")", '')).replace("(", '')).replace("\n", '')).replace(" ", '')).split(',')
b = {i: j for i,j in zip(range(len(a)), a)}