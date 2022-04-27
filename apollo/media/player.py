import copy
import os
import random

import pyo

from apollo.media.processor import DynamicProcessingChain
from apollo.utils import ApolloSignal


class PlayerQueue:
    """Queue track stores the loaded track paths"""
    def __init__(self, data: list[str] = None):
        """
        Constructor

        Args:
            data (list[str]): ist of file paths
        """
        self._queue = self.gen_queue(data) if data is not None else {}
        self.pointer = 0
        self.circular = False
        self._shuffled = False

    def __str__(self) -> str:
        return str(self._queue)

    def __repr__(self) -> str:
        return str(self._queue)

    def gen_queue(self, data: list, is_shuffled: bool = False) -> dict:
        """
        Generates the ordered queue

        Args:
            data (list[str]): ist of file paths
            is_shuffled (bool): is the ordered shuffled

        Returns:
            dict: ordered queue
        """
        if not is_shuffled:
            self._shuffled = is_shuffled
            return {k: v for k, v in zip(range(len(data)), data)}
        else:
            shuffled_queue = list(range(len(data)))
            random.shuffle(shuffled_queue)
            self._shuffled = is_shuffled
            return {k: v for k, v in zip(shuffled_queue, data)}

    def set_data(self, data: list):
        """
        Sets new data to the queue

        Args:
            data (list[str]): ist of file paths
        """
        self._queue = self.gen_queue(data, self.shuffled)
        self.pointer = 0

    def get_data(self) -> dict:
        """
        Returns the ordered queue

        Returns:
            dict: ordered queue
        """
        return self._queue

    def clear_data(self):
        """
        Clears the ordered queue and resets the pointer
        """
        self._queue = {}
        self.pointer = 0

    def get_current_item(self) -> str:
        """
        gets the item at position

        Returns:
            str: item at index
        """
        return self._queue[self.pointer]

    def get_next_item(self) -> str:
        """
        gets the next item at position

        Returns:
            str: item at index
        """
        if 0 <= (self.pointer + 1) < len(self._queue):
            self.pointer += 1
        else:
            if self.circular:
                self.pointer = 0

        return self.get_current_item()

    def get_prev_item(self) -> str:
        """
        gets the previous item at position

        Returns:
            str: item at index
        """
        if 0 <= (self.pointer - 1) < len(self._queue):
            self.pointer -= 1
        else:
            if self.circular:
                self.pointer = len(self._queue) - 1

        return self.get_current_item()

    def reset_pointer(self):
        """
        resets the pointer location
        """
        if (self.pointer + 1) >= len(self._queue):
            self.pointer = 0
        else:
            self.pointer = len(self._queue) - 1

    @property
    def shuffled(self) -> bool:
        """
        Property accessor to the shuffled flag

        Returns:
            bool: true if the queue is shuffled, otherwise false
        """
        return self._shuffled

    @shuffled.setter
    def shuffled(self, value: bool):
        """
        Property modifier to the shuffled flag

        Args:
            value (bool): true if the queue is shuffled, otherwise false
        """
        self._queue = self.gen_queue(list(self._queue.values()), value)
        self._shuffled = value


class Player:
    """
    Player interface that communicates with the DSP
    """
    STOP_PLAYER = ApolloSignal()
    START_PLAYER = ApolloSignal()
    END_QUEUE = ApolloSignal()

    REPEAT_TRACK = 0
    REPEAT_QUEUE = 1
    REPEAT_NONE = 2
    SHUFFLE_NONE = 0
    SHUFFLE_TRACK = 1

    def __init__(self):
        """
        Constructor
        """
        self.server = pyo.Server().boot().start()
        self.repeat_type = self.REPEAT_NONE
        self.shuffle_type = self.SHUFFLE_NONE
        self.processor = DynamicProcessingChain()
        self.queue = PlayerQueue()
        self.set_volume(25)

        # connect signals
        self.processor.STREAM_ABOUT_TOEND.connect(self.play_next)
        self.server.setCallback(self.processor.recurring_server_callback)
        self.processor.main_output.out()

    def load_track(self, path: str, instant: bool):
        """
        Loads the track into the buffer and cross-fades between both

        Args:
            path (str): path to read into an audio buffer
            instant (bool): instantly switches between the audio buffer rather than cross-fading.
        """
        self.processor.load_track(path, instant)

    def set_queue(self, data: list):
        """
        Sets new data to the queue

        Args:
            data (list[str]): ist of file paths
        """
        self.queue.set_data(data)
        path = self.queue.get_current_item()
        if path is not None:
            self.load_track(path, True)
        else:
            self.queue.reset_pointer()
            self.stop()
            self.END_QUEUE.emit()

    def set_repeat_type(self, _type: int):
        """
        Sets if the track needs to be repeated

        Args:
            _type (Union[REPEAT_TRACK | REPEAT_QUEUE | REPEAT_NONE]): repeat type
        """
        if self.REPEAT_TRACK == _type:
            self.processor.repeat_current_buffer = True
        elif self.REPEAT_QUEUE == _type:
            self.queue.circular = True
        elif self.REPEAT_NONE == _type:
            self.queue.circular = False
            self.processor.repeat_current_buffer = False
        else:
            return None

    def set_shuffle_type(self, _type: int):
        """
        Sets if the queue needs to be shuffled

        Args:
            _type (Union[SHUFFLE_NONE | SHUFFLE_TRACK]): repeat type
        """
        if self.SHUFFLE_NONE == _type:
            self.queue.shuffled = False
        elif self.SHUFFLE_TRACK == _type:
            self.queue.shuffled = True
        else:
            return None

    def play_next(self):
        """
        plays the next item from the queue
        """
        path = self.queue.get_next_item()
        if path is not None:
            self.load_track(path, False)
        else:
            self.queue.reset_pointer()
            self.stop()
            self.END_QUEUE.emit()

    def play_prev(self):
        """
        plays the prev item from the queue
        """
        path = self.queue.get_prev_item()
        if path is not None:
            self.load_track(path, False)
        else:
            self.queue.reset_pointer()
            self.stop()
            self.END_QUEUE.emit()

    def play(self):
        """starts the player"""
        self.START_PLAYER.emit()
        self.processor.play()
        self.server.start()

    def stop(self):
        """stops the player"""
        self.STOP_PLAYER.emit()
        self.processor.stop()
        self.server.stop()

    def set_volume(self, value: int):
        """
        sets the amp value of the server

        Args:
            value (int): value between 0 to 100
        """
        value = ((2 * pow(value, 2)) / 100) * 0.01
        self.server.setAmp(value if value >= 0.0001 else 0.0001)


if __name__ == '__main__':
    player = Player()
    player.set_queue([os.path.join(r'D:\music', file) for file in os.listdir(r'D:\music')])
    player.server.gui(locals())
