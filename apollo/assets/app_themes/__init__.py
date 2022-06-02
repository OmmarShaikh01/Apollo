import os
from collections import namedtuple
from pathlib import PurePath


class _AppIcons:
    __slots__ = ['ADD', 'ARROW_BACK', 'ARROW_FORWARD', 'AUDIO_FILE', 'CHECK_BOX', 'CHECK_BOX_OUTLINE_BLANK', 'CLOSE',
        'DELETE', 'DONE', 'EQUALIZER', 'EXPAND_LESS', 'EXPAND_MORE', 'FAVORITE', 'FAVORITE_FILLED', 'FILE_DOWNLOAD',
        'STAR_OUTLINE', 'HOME', 'INDETERMINATE_CHECK_BOX', 'LIBRARY_MUSIC', 'MENU', 'MUSIC_NOTE', 'PAUSE', 'PLAYLIST_ADD',
        'PLAYLIST_PLAY', 'PLAY_ARROW', 'POWER_SETTINGS_NEW', 'QUEUE_MUSIC', 'RADIO_BUTTON_CHECKED',
        'RADIO_BUTTON_UNCHECKED', 'REPEAT_OFF', 'REPEAT_ON', 'REPEAT_ONE_ON', 'SEARCH', 'SETTINGS', 'SHUFFLE',
        'SHUFFLE_OFF', 'SKIP_NEXT', 'SKIP_PREVIOUS', 'STAR', 'STAR_HALF', 'VOLUME_DOWN', 'VOLUME_MUTE', 'VOLUME_OFF',
        'VOLUME_UP']
    Icon = namedtuple('Icon', ['danger', 'disabled', 'primary', 'secondary', 'success', 'warning'])

    def __init__(self):
        self._init_attrs()

    def _init_attrs(self):
        path = PurePath(os.path.dirname(__file__), '__loaded_theme__', 'icons')
        if os.path.exists(path):
            for file in os.listdir(path / 'primary'):
                name, ext = os.path.splitext(file)
                value = self.Icon(*[
                    (path / 'danger' / str(file)), (path / 'disabled' / str(file)),
                    (path / 'primary' / str(file)), (path / 'secondary' / str(file)),
                    (path / 'success' / str(file)), (path / 'warning' / str(file))
                ])
                setattr(self, str(name), value)

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            self._init_attrs()
            return object.__getattribute__(self, item)


AppIcons = _AppIcons()

if __name__ == '__main__':
    print(AppIcons.HOME)