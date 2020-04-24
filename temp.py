import tinytag

filename = 'E:/musiccc/01 Back 2 U (Steve Aoki & Bad Royale Remix).flac'
meta_info = (tinytag.TinyTag.get(filename)).as_dict()


print(f'Artist: {meta_info["artist"]}')
print(f'Title: {meta_info["title"]}')
print(f'Album: {meta_info["album"]}')
print(f'Album Artist: {meta_info["albumartist"]}')
print(f'Composer: {meta_info["composer"]}')
print(f'Genre: {meta_info["genre"]}')
print(f'Samplerate: {meta_info["samplerate"]} Hz')
print(f'Bitrate: {int(meta_info["bitrate"])} Kbps')
print(f'Channels: {meta_info["channels"]} Channels')
print(f'Duration: {(("{0}.{1} Min".format(str(int( meta_info["duration"] // 60)), str(int( meta_info["duration"] % 60)))))}')
print(f'Year: {meta_info["year"]}')

