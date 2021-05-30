import datetime
import os
import pytest

from PySide6.QtSql import QSqlQuery
from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from apollo.db import DataBaseManager, FileManager, LibraryManager
from apollo.db import DBStructureError, QueryBuildFailed, QueryExecutionFailed

from tests.main.fixtures import DBManager, Gen_DbTable_Data
from tests.main.fixtures import LibraryManager_connected, TempFilled_DB, del_TempFilled_DB

#### Tests ####################################################################

class Test_DataBaseManager:

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        del_TempFilled_DB()

    def test_DBstartup(self):
        Manager = DataBaseManager()

        # checks for a normal connection startup
        assert Manager.connect(":memory:")
        assert Manager.IsConneted()

        # checks for an post connection DB Structure integrity
        assert Manager.StartUpChecks()

        # checks for an post connection drop of main table and still manintains integrity
        Manager.DropTable("library")
        assert Manager.StartUpChecks()

        # checks for a normal connection close
        assert Manager.close_connection()
        assert (not Manager.IsConneted())

    def test_DBFiletype(self):
        Manager = DataBaseManager()

        # checks for non DB file filtering
        assert not Manager.connect("hello.txt")

        # checks for in memory DB file
        assert Manager.connect(":memory:")
        Manager.close_connection() # cleanup

        # checks for DB file filtering
        assert Manager.connect("trial.db")
        assert Manager.StartUpChecks()
        Manager.close_connection() # cleanup
        os.remove('trial.db') # cleanup
        os.path.isfile("trial.db") # cleanup

    def test_BatchInsert_Metadata(self, DBManager, Gen_DbTable_Data):
        Manager = DBManager
        DATA = Gen_DbTable_Data
        Manager.BatchInsert_Metadata(DATA)

        Inserted_data = [[Col[R] for Col in DATA.values()] for R in range(len(DATA["file_id"]))]
        Querydata = Manager.SelectAll("library")

        assert Inserted_data == Querydata
        Manager.close_connection() # cleanup

    def test_SelectAll(self, DBManager, Gen_DbTable_Data):
        Manager = DBManager
        DATA = Gen_DbTable_Data
        Manager.BatchInsert_Metadata(DATA)

        Inserted_data = [[Col[R] for Col in DATA.values()] for R in range(len(DATA["file_id"]))]
        Querydata = Manager.SelectAll("library")

        assert Inserted_data == Querydata
        Manager.close_connection() # cleanup

    def test_ExeQuery(self, DBManager):
        Manager = DBManager

        # string query complete execution
        query = Manager.ExeQuery("""
	        SELECT IIF(name = 'library', TRUE, FALSE)
        FROM sqlite_master WHERE type = 'table'
        """)
        assert isinstance(query, QSqlQuery)

        # SQLQuery object complete execution
        query = Manager.ExeQuery(QSqlQuery("""
	        SELECT IIF(name = 'library', TRUE, FALSE)
        FROM sqlite_master WHERE type = 'table'
        """))
        assert isinstance(query, QSqlQuery)

        # string build failing
        try:
            query = Manager.ExeQuery("""
	            SELECT IIF(name = 'library', TRUE, FALSE)
            FROM sqlite_master type = 'table'
            """)
        except QueryBuildFailed: assert True
        else: assert False

        # SQLQuery object execution failing
        try:
            query = Manager.ExeQuery(QSqlQuery("""
	            SELECT IIF(name = 'library', TRUE, FALSE)
            FROM sqlite_master type = 'table'
            """))
        except QueryExecutionFailed: assert True
        else: assert False

        Manager.close_connection() # cleanup

    def test_fetchAll(self, DBManager):
        Manager = DBManager

        # running the function with no column constraints
        query = Manager.ExeQuery("SELECT cid, name FROM pragma_table_info('library')")
        Expected = [[k,v] for k, v in enumerate(Manager.db_fields)]
        assert Expected == Manager.fetchAll(query)

        # running the function with column constraints
        query = Manager.ExeQuery("SELECT cid, name FROM pragma_table_info('library')")
        Expected = [[v] for v in Manager.db_fields]
        assert Expected == Manager.fetchAll(query, 1)

        Manager.close_connection() # cleanup

    def test_indexedSelector(self, DBManager):
        Manager = DBManager

        # check for getting data for a given column
        assert [[None]] == Manager.IndexSelector("nowplaying", "file_name")

        Manager.close_connection() # cleanup

    def test_CreateView_normal(self, TempFilled_DB):
        Manager, Data = TempFilled_DB
        Selector = ["file_idX1"]
        Manager.CreateView(view_name = "nowplaying", Selector = Selector)
        Expected = [['file_idX1', 'path_idX1', 'file_nameX1', 'file_pathX1', 'albumX1',
                    'albumartistX1', 'artistX1', 'authorX1', 'bpmX1', 'compilationX1', 'composerX1',
                    'conductorX1', 'dateX1', 1, 'discsubtitleX1', 'encodedbyX1', 'genreX1', 'languageX1',
                    '0:01:00', '1024', 'lyricistX1', 'mediaX1', 'moodX1', 'organizationX1', 'originaldateX1',
                    'performerX1', 'releasecountryX1', 'replaygain_gainX1', 'replaygain_peakX1', 'titleX1',
                    'tracknumberX1', 'versionX1', 'websiteX1', 'album_gainX1', 'bitrateX1', 'bitrate_modeX1',
                    1, 'encoder_infoX1', 'encoder_settingsX1', 'frame_offsetX1', 'layerX1', 'modeX1',
                    'paddingX1', 'protectedX1', 'sample_rateX1', 'track_gainX1', 'track_peakX1',
                    'ratingX1', 'playcountX1']]
        assert (Expected == Manager.SelectAll("nowplaying"))
        Manager.close_connection() # cleanup

    def test_CreateView_Shuffled(self, TempFilled_DB):
        Manager, Data = TempFilled_DB
        Selector = ["file_idX1"]
        Manager.CreateView(view_name = "nowplaying", Selector = Selector, Shuffled = True)
        Expected = [['file_idX1', 'path_idX1', 'file_nameX1', 'file_pathX1', 'albumX1',
                    'albumartistX1', 'artistX1', 'authorX1', 'bpmX1', 'compilationX1', 'composerX1',
                    'conductorX1', 'dateX1', 1, 'discsubtitleX1', 'encodedbyX1', 'genreX1', 'languageX1',
                    '0:01:00', '1024', 'lyricistX1', 'mediaX1', 'moodX1', 'organizationX1', 'originaldateX1',
                    'performerX1', 'releasecountryX1', 'replaygain_gainX1', 'replaygain_peakX1', 'titleX1',
                    'tracknumberX1', 'versionX1', 'websiteX1', 'album_gainX1', 'bitrateX1', 'bitrate_modeX1',
                    1, 'encoder_infoX1', 'encoder_settingsX1', 'frame_offsetX1', 'layerX1', 'modeX1',
                    'paddingX1', 'protectedX1', 'sample_rateX1', 'track_gainX1', 'track_peakX1',
                    'ratingX1', 'playcountX1']]
        assert (Expected == Manager.SelectAll("nowplaying"))
        Manager.close_connection() # cleanup

    def test_CreateView_normal_fieldSelector(self, TempFilled_DB):
        Manager, Data = TempFilled_DB
        Selector = ["path_idX1"]
        Manager.CreateView(view_name = "nowplaying", Selector = Selector, FilterField = "path_id")
        Expected = [['file_idX1', 'path_idX1', 'file_nameX1', 'file_pathX1', 'albumX1',
                    'albumartistX1', 'artistX1', 'authorX1', 'bpmX1', 'compilationX1', 'composerX1',
                    'conductorX1', 'dateX1', 1, 'discsubtitleX1', 'encodedbyX1', 'genreX1', 'languageX1',
                    '0:01:00', '1024', 'lyricistX1', 'mediaX1', 'moodX1', 'organizationX1', 'originaldateX1',
                    'performerX1', 'releasecountryX1', 'replaygain_gainX1', 'replaygain_peakX1', 'titleX1',
                    'tracknumberX1', 'versionX1', 'websiteX1', 'album_gainX1', 'bitrateX1', 'bitrate_modeX1',
                    1, 'encoder_infoX1', 'encoder_settingsX1', 'frame_offsetX1', 'layerX1', 'modeX1',
                    'paddingX1', 'protectedX1', 'sample_rateX1', 'track_gainX1', 'track_peakX1',
                    'ratingX1', 'playcountX1']]
        assert (Expected == Manager.SelectAll("nowplaying"))
        Manager.close_connection() # cleanup

    def test_CreateView_filter_fieldSelector_fileID(self, TempFilled_DB):
        Manager, Data = TempFilled_DB
        Selector = ["path_idX1"]
        ID = ["file_idX2"]
        Manager.CreateView(view_name = "nowplaying", Selector = Selector, ID = ID, FilterField = "path_id")

        Expected = [['file_idX1', 'path_idX1', 'file_nameX1', 'file_pathX1', 'albumX1',
                    'albumartistX1', 'artistX1', 'authorX1', 'bpmX1', 'compilationX1', 'composerX1',
                    'conductorX1', 'dateX1', 1, 'discsubtitleX1', 'encodedbyX1', 'genreX1', 'languageX1',
                    '0:01:00', '1024', 'lyricistX1', 'mediaX1', 'moodX1', 'organizationX1', 'originaldateX1',
                    'performerX1', 'releasecountryX1', 'replaygain_gainX1', 'replaygain_peakX1', 'titleX1',
                    'tracknumberX1', 'versionX1', 'websiteX1', 'album_gainX1', 'bitrateX1', 'bitrate_modeX1',
                    1, 'encoder_infoX1', 'encoder_settingsX1', 'frame_offsetX1', 'layerX1', 'modeX1',
                    'paddingX1', 'protectedX1', 'sample_rateX1', 'track_gainX1', 'track_peakX1',
                    'ratingX1', 'playcountX1'],
                    ['file_idX2', 'path_idX2', 'file_nameX2', 'file_pathX2', 'albumX2',
                    'albumartistX2', 'artistX2', 'authorX2', 'bpmX2', 'compilationX2', 'composerX2',
                    'conductorX2', 'dateX2', 2, 'discsubtitleX2', 'encodedbyX2', 'genreX2', 'languageX2',
                    '0:01:00', '1024', 'lyricistX2', 'mediaX2', 'moodX2', 'organizationX2', 'originaldateX2',
                    'performerX2', 'releasecountryX2', 'replaygain_gainX2', 'replaygain_peakX2', 'titleX2',
                    'tracknumberX2', 'versionX2', 'websiteX2', 'album_gainX2', 'bitrateX2', 'bitrate_modeX2',
                    2, 'encoder_infoX2', 'encoder_settingsX2', 'frame_offsetX2', 'layerX2', 'modeX2',
                    'paddingX2', 'protectedX2', 'sample_rateX2', 'track_gainX2', 'track_peakX2',
                    'ratingX2', 'playcountX2']]
        assert all([(E==A) for E, A in zip(Expected, Manager.SelectAll("nowplaying"))])
        Manager.close_connection() # cleanup

    def test_DropTable(self, DBManager):
        Manager = DBManager
        Manager.DropTable("library")

        assert not Manager.fetchAll(Manager.ExeQuery("""
	        SELECT IIF(name = 'library', TRUE, FALSE) AS TABLE_CHECK
        FROM sqlite_master WHERE type = 'table'
        """))

        Manager.close_connection() # cleanup

    def test_DropView(self, DBManager):
        Manager = DBManager

        Manager.DropView("nowplaying")

        assert not Manager.fetchAll(Manager.ExeQuery("""
	        SELECT IIF(name = 'nowplaying', TRUE, FALSE) AS TABLE_CHECK
        FROM sqlite_master WHERE type = 'view'
        """))

        Manager.close_connection() # cleanup

    def test_TableSize(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TableSize("library") >= 0)

        # checks for empty
        assert (Manager.TableSize("nowplaying") == 0)

        Manager.close_connection() # cleanup

    def test_TablePlaycount(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TablePlaycount("library") >= 0)

        # checks for empty
        assert (Manager.TablePlaycount("nowplaying") == 0)

        Manager.close_connection() # cleanup

    def test_TablePlaytime(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TablePlaytime("library") >= datetime.timedelta(seconds = 1))

        # checks for empty
        assert (Manager.TablePlaytime("nowplaying") == datetime.timedelta(seconds = 0))

        Manager.close_connection() # cleanup

    def test_TableAlbumcount(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TableAlbumcount("library") >= 0)

        # checks for empty
        assert (Manager.TableAlbumcount("nowplaying") == 0)

        Manager.close_connection() # cleanup

    def test_TableArtistcount(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TableArtistcount("library") >= 0)

        # checks for empty
        assert (Manager.TableArtistcount("nowplaying") == 0)

        Manager.close_connection() # cleanup

    def test_TableTrackcount(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TableTrackcount("library") >= 0)

        # checks for empty
        assert (Manager.TableTrackcount("nowplaying") == 0)

        Manager.close_connection() # cleanup

    def test_TopAlbum(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.TopAlbum("library") != "")

        # checks for empty
        assert (Manager.TopAlbum("nowplaying") == "")

        Manager.close_connection() # cleanup

    def test_Topgenre(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.Topgenre("library") != "")

        # checks for empty
        assert (Manager.Topgenre("nowplaying") == "")

        Manager.close_connection() # cleanup

    def test_Topartist(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.Topartist("library") != "")

        # checks for empty
        assert (Manager.Topartist("nowplaying") == "")

        Manager.close_connection() # cleanup

    def test_Toptrack(self, TempFilled_DB):
        Manager, Data = TempFilled_DB

        # checks for data avaliable
        assert (Manager.Toptrack("library") != "")

        # checks for empty
        assert (Manager.Toptrack("nowplaying") == "")

        Manager.close_connection() # cleanup


class Test_LibraryManager:

    def test_LibraryManager(self, LibraryManager_connected):
        Manager = LibraryManager_connected
        assert Manager.IsConneted()
