from features.logger.logger_levels import LoggerLevels
from features.logger.logger_levels import from_logger_level
from features.logger.logger import Logger
from utime import time

import os


class FileLogger(Logger):
    def __init__(self, console: bool, debug: bool, folder: str = "logs"):
        super().__init__(debug)

        if not self._dir_exists(folder):
            os.mkdir(folder)
        else:
            self._remove_files_in_directory(folder)

        file_name = f"log{time()}.txt"

        self.file_path = f"{folder}/{file_name}"
        self.console = console

        with open(self.file_path, "w") as file:
            file.write("Logger Initialized\n")

        print("Logger Initialized")

    def info(self, message: str):
        data = self._format_message(LoggerLevels.INFO, message)
        self._write_to_file(data)
        if self.console:
            print(data)

    def warning(self, message: str):
        data = self._format_message(LoggerLevels.WARNING, message)
        self._write_to_file(data)
        if self.console:
            print(data)

    def error(self, message: str):
        data = self._format_message(LoggerLevels.ERROR, message)
        self._write_to_file(data)
        if self.console:
            print(data)

    def debug(self, message: str):
        if self.is_debug:
            data = self._format_message(LoggerLevels.DEBUG, message)
            self._write_to_file(data)
            if self.console:
                print(data)

    def _write_to_file(self, data: str):
        with open(self.file_path, 'a') as file:
            file.write(data + '\n')

    @staticmethod
    def _dir_exists(filename):
        try:
            return (os.stat(filename)[0] & 0x4000) != 0
        except OSError:
            return False

    @staticmethod
    def _file_exists(filename):
        try:
            return (os.stat(filename)[0] & 0x4000) == 0
        except OSError:
            return False

    @staticmethod
    def _remove_files_in_directory(directory):
        for filename in os.listdir(directory):
            file_path = f"{directory}/{filename}"
            try:
                if FileLogger._file_exists(file_path):
                    os.remove(file_path)
                    print(f"Removed {file_path}")
            except Exception as e:
                print(f"Error: {e}")
