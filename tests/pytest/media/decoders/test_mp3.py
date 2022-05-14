import os
import timeit
from pathlib import PurePath

import av
import pytest
import pytest_cases

from apollo.media import Mediafile
from apollo.utils import get_logger
from configs import settings
from tests.assets.music_samples.generate import create_mp3
from tests.pytest.utils_for_tests import IDGen

CONFIG = settings
BENCHMARK = CONFIG.benchmark_formats  # TODO: remove not
LOGGER = get_logger(__name__)
create_mp3()
cases = "tests.pytest.media.decoders.case_decoder"


class Test_Mediafile_MP3:

    @pytest.mark.skipif(not BENCHMARK, reason = f"Benchmarking: {BENCHMARK}")
    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'files_mp3', ids = IDGen)
    def test_benchmark_load_times(self, file_path: PurePath):
        LOGGER.info("RUNTIME: {run}".format(run = timeit.timeit(lambda: Mediafile(file_path), number = 2000)))

    @pytest.mark.skipif(not BENCHMARK, reason = f"Benchmarking: {BENCHMARK}")
    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'files_mp3', ids = IDGen)
    def test_benchmark_full_load_times(self, file_path: PurePath):
        LOGGER.info("RUNTIME: {run}".format(run = timeit.timeit(lambda: Mediafile(file_path).SynthTags, number = 2000)))

    @pytest.mark.skip
    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'files_mp3', ids = IDGen)
    def test_loading_files(self, file_path: PurePath):
        media = Mediafile(file_path)
        if file_path.match("example_48000H_2C_TAGGED.mp3"):
            assert len(media.Tags) > 0
        else:
            assert len(media.Tags) == 0

    @pytest.mark.skip
    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'files_mp3', ids = IDGen)
    def test_loading_decoders(self, file_path: PurePath):
        def validate_frame(_frame: av.AudioFrame):
            LOGGER.debug(_frame)
            assert _frame
            assert _frame.rate == CONFIG.server.rate
            assert len(_frame.layout.channels) == CONFIG.server.chnl

        # read the frames
        media = Mediafile(file_path)
        frame = media.get_frame()
        validate_frame(frame)

        # resets seek pointer and reads first frame
        media.Decoder.reset_buffer()
        frame = media.get_frame()
        validate_frame(frame)

        # seeks 1 sec and reads ahead till EOF
        media.Decoder.reset_buffer()
        media.Decoder.seek(1)
        frame = media.get_frame()
        count = frame.samples

        # checks for EOF
        with pytest.raises(StopIteration):
            while frame:
                frame = media.get_frame()
                count += frame.samples
                continue
        assert (4 == int(count / CONFIG.server.rate))
        LOGGER.debug(f"END FRAME: {(frame, int(count / CONFIG.server.rate))}")

    @pytest_cases.parametrize_with_cases('file_path', cases = cases, prefix = 'files_mp3', ids = IDGen)
    def test_loading_tags(self, file_path):
        media = Mediafile(file_path)
        if not file_path.match("example_48000H_2C_TAGGED.mp3"):
            assert media.SynthTags
        else:
            # TODO: Verbose testing of each tag
            assert media.SynthTags["TITLE"] == ["TESTING"]
            assert media.SynthTags["ARTIST"] == ["TESTING"]
            assert media.SynthTags["ALBUM"] == ["TESTING"]

            assert media.SynthTags["PICTURE"] == [True]
            assert len(media.Artwork) > 0
            LOGGER.debug(media.SynthTags)
            LOGGER.debug(media.Records)
