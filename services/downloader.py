# -*- coding: utf-8 -*-
from pytubefix import YouTube
from abc import abstractmethod, ABC
from pydantic import BaseModel
import ffmpeg
import os


class BaseDownloader(ABC):
    @abstractmethod
    def init_source_loader(self, url, file_type):
        pass

    @abstractmethod
    def get_resource_title(self):
        # 获取资源标题
        pass

    @abstractmethod
    def get_resource_data(self, dir_path: str):
        pass


class ResourceSupportModel(BaseModel):
    data_source: str
    domain: str
    file_type: str
    downloader: BaseDownloader

    class Config:
        arbitrary_types_allowed = True


class YoutubeDownloader(BaseDownloader):

    def __init__(self):
        self.file_type = None
        self.url = None
        self.yt = None

    def init_source_loader(self, url, file_type):
        self.url = url
        self.file_type = file_type
        self.yt = YouTube(self.url, on_progress_callback=self.on_progress_callback)

    def get_resource_title(self):
        return self.yt.title + "." + self.file_type

    def download_video(self, dir_path):
        # 下载高质量视频
        return self.yt.streams.filter(only_video=True).order_by('bitrate').desc().first().download(output_path=dir_path)

    def download_music(self, dir_path):
        return self.yt.streams.get_audio_only().download(mp3=True, output_path=dir_path)

    def get_resource_data(self, file_path):
        dir_path = os.path.dirname(file_path)
        # 下载高质量视频
        video_file = self.download_video(dir_path)
        # 下载音频
        audio_file = self.download_music(dir_path)
        video_stream = ffmpeg.input(video_file)
        audio_stream = ffmpeg.input(audio_file)
        (
            ffmpeg
            .output(video_stream, audio_stream, file_path, codec='copy', acodec='aac')
            .global_args("-loglevel", "error")
            .run(overwrite_output=True)  # 允许覆盖输出文件
        )

    @staticmethod
    def on_progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print(f"Downloading... {percentage:.2f}%")


class BilibiliDownloader(BaseDownloader):

    def init_source_loader(self, url, file_type):
        return None

    def get_resource_title(self):
        return "temp file"

    def get_resource_data(self, dir_path: str):
        return None


class UnknownDownloader(BaseDownloader):
    def init_source_loader(self, url, file_type):
        return None

    def get_resource_data(self, dir_path):
        return None

    def get_resource_title(self):
        return "unknown name"


if __name__ == '__main__':
    yt = YoutubeDownloader()
    url1 = "https://www.youtube.com/watch?v=bZkRo4e4Y9E"
    file_type1 = "mp4"
    yt.init_source_loader(url1, file_type1)
    yt.get_resource_data(f"/data/files/{yt.get_resource_title()}")
