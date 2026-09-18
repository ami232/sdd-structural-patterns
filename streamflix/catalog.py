
from abc import ABC, abstractmethod


class Video(ABC):
    """
    Subject interface. Both the real video and its proxy expose this.
    """

    @abstractmethod
    def play(self) -> str:
        raise NotImplementedError


class RealVideo(Video):
    """
    The expensive resource: loading a video "file" is slow and should only
    happen once, and only when the video is actually about to be played.
    """

    load_count = 0

    def __init__(self, title: str, video_path: str):
        self.title = title
        self.video_path = video_path
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        RealVideo.load_count += 1

    def play(self) -> str:
        return f"Playing '{self.title}' from {self.video_path}"


class ProxyVideo(Video):
    """
    Virtual proxy: stands in for a RealVideo without loading it until the
    first `play()` call, then reuses the same RealVideo for later calls.
    """

    def __init__(self, title: str, video_path: str):
        self.title = title
        self.video_path = video_path
        self._real_video: RealVideo | None = None

    def play(self) -> str:
        if self._real_video is None:
            self._real_video = RealVideo(self.title, self.video_path)
        return self._real_video.play()
