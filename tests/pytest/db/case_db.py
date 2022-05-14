from pathlib import PurePath
from pytest_cases import parametrize

from configs import settings

CONFIG = settings
MEDIA_FOLDER = PurePath(CONFIG.assets_dir, "music_samples")


def import_json_data():
    data = dict(sql_table_schema = dict(
            test_table_0 = 'CREATE TABLE test_table_0 ("col_0" TEXT, "col_1" TEXT, "col_2" TEXT)',
            test_table_1 = 'CREATE TABLE test_table_1 ("col_0" TEXT, "col_1" TEXT, "col_2" TEXT)', ),
            test_table_0 = {0: dict(col_0 = 'test_1_0', col_1 = 'test_2_0', col_2 = 'test_3_0'),
                            1: dict(col_0 = 'test_1_1', col_1 = 'test_2_1', col_2 = 'test_3_1'),
                            2: dict(col_0 = 'test_1_2', col_1 = 'test_2_2', col_2 = 'test_3_2'),
                            3: dict(col_0 = 'test_1_3', col_1 = 'test_2_3', col_2 = 'test_3_3'),
                            4: dict(col_0 = 'test_1_4', col_1 = 'test_2_4', col_2 = 'test_3_4'), },
            test_table_1 = {0: dict(col_0 = 'test_1_0', col_1 = 'test_2_0', col_2 = 'test_3_0'),
                            1: dict(col_0 = 'test_1_1', col_1 = 'test_2_1', col_2 = 'test_3_1'),
                            2: dict(col_0 = 'test_1_2', col_1 = 'test_2_2', col_2 = 'test_3_2'),
                            3: dict(col_0 = 'test_1_3', col_1 = 'test_2_3', col_2 = 'test_3_3'),
                            4: dict(col_0 = 'test_1_4', col_1 = 'test_2_4', col_2 = 'test_3_4'), })
    return data


@parametrize('path', [(MEDIA_FOLDER / 'dsf' / "example.dsf"),
                      (MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3"),
                      (MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3").as_posix(),
                      [(MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3"),
                       (MEDIA_FOLDER / 'mp3' / "example_48000H_2C_TAGGED.mp3")]])
def file_tagged_mp3(path):
    return path
