from .library import LibraryModel
from .playlists import PlaylistsModel


class _Provider:

    def __init__(self) -> None:
        super().__init__()

    def get_model(self, _type):
        if (LibraryModel) == (_type):
            if not hasattr(self, "LibraryModel"):
                self.LibraryModel = LibraryModel()
            return self.LibraryModel
        elif (PlaylistsModel) == (_type):
            if not hasattr(self, "PlaylistsModel"):
                self.PlaylistsModel = PlaylistsModel()
            return self.PlaylistsModel
        else:
            return None


Provider = _Provider()
