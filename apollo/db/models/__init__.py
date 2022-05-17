from apollo.db.models.library import LibraryModel
# from apollo.db.models.playlists import PlaylistsModel
# from apollo.db.models.queue import QueueModel


class _Provider:

    def __init__(self) -> None:
        super().__init__()

    # noinspection PyAttributeOutsideInit
    def get_model(self, _type):
        if _type is LibraryModel:
            if not hasattr(self, "LibraryModel"):
                self.LibraryModel = LibraryModel()
            return self.LibraryModel
        # elif (PlaylistsModel) == (_type):
        #     if not hasattr(self, "PlaylistsModel"):
        #         self.PlaylistsModel = PlaylistsModel()
        #     return self.PlaylistsModel
        # elif (QueueModel) == (_type):
        #     if not hasattr(self, "QueueModel"):
        #         self.QueueModel = QueueModel()
        #     return self.QueueModel
        else:
            return None


Provider = _Provider()
