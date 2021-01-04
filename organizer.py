#!/usr/bin/env /Users/srinibasmisra/Documents/Projects/File-Organizer/venv/bin/python

import time
import os
import argparse
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

_WATCH_DIRECTORY = "/Users/srinibasmisra/Downloads"

_AUDIO_FILE_FORMATS = ['aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl']
_COMPRESSED_FILE_FORMATS = ['7z', 'arj', 'deb', 'pkg', 'rar', 'rpm', 'tar.gz', 'gz', 'z', 'zip']
_DISK_MEDIA_FILE_FORMATS = ['bin', 'dmg', 'iso', 'toast', 'vcd']
_DATA_DATABASE_FILE_FORMATS = ['csv', 'dat', 'db', 'dbf', 'log', 'mdb', 'sav', 'sql', 'tar', 'xml']
_EMAIL_FILE_FORMATS = ['email', 'eml', 'emlx', 'msg', 'oft', 'ost', 'pst', 'vcf']
_EXECUTABLE_FILE_FORMATS = ['apk', 'bat', 'sh', 'bin', 'cgi', 'com', 'exe', 'gadget', 'jar', 'command', 'msi', 'wsf']
_FONT_FILE_FORMATS = ['fnt', 'fon', 'otf', 'ttf']
_IMAGE_FILE_FORMATS = ['ai', 'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'ps', 'psd', 'svg', 'tif', 'tiff']
_PRESENTATION_FILE_FORMATS = ['key', 'odp', 'pps', 'ppt', 'pptx']
_PROGRAMMING_FILE_FORMATS = ['c', 'cgi', 'pl', 'class', 'cpp', 'cs', 'h', 'java', 'php', 'py', 'sh', 'swift', 'vb',
                             'asp', 'aspx', 'css', 'htm', 'html', 'js', 'jsp', 'xhtml', 'json']
_SPREADSHEET_FILE_FORMATS = ['ods', 'xls', 'xlm', 'xlsx']
_SYSTEM_FILE_FORMATS = ['bak', 'cab', 'cfg', 'cpl', 'cur', 'dll', 'dmp', 'drv', 'icns', 'ini', 'lnk', 'sys', 'tmp']
_VIDEO_FILE_FORMATS = ['3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'rm', 'swf',
                       'vob', 'wmv']
_TEXT_FILE_FORMATS = ['doc', 'docx', 'pdf', 'rtf', 'tex', 'txt', 'wpd']

_CHROME_DOWNLOAD = False

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(msecs)-3d::%(levelname)-8s%(message)s',
                    datefmt='%Y%m%d %H%M%S',
                    filename='/Users/srinibasmisra/Documents/Projects/File-Organizer/organizer_' + datetime.now().strftime('%Y%m%d') + '.log',
                    filemode='a'
                    )


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event, **kwargs):
        global _CHROME_DOWNLOAD
        if event.is_directory:
            return None
        elif event.event_type in ['created', 'modified']:
            file_name = os.path.basename(event.src_path)
            extension = file_name.split(".")[len(file_name.split(".")) - 1]
            if "com.google.Chrome" in file_name:
                _CHROME_DOWNLOAD = True
                return None
            if ".download" in os.path.dirname(event.src_path):
                return None
            if extension in ['crdownload', 'download', 'DS_Store', 'plist']:
                return None

            logging.info("{} {}".format(event.event_type, event.src_path))

            if _CHROME_DOWNLOAD:
                if event.event_type == 'modified':
                    organizer = Organizer(os.path.dirname(event.src_path))
                    organize(organizer, event.src_path)
                    _CHROME_DOWNLOAD = False
        elif event.event_type == 'deleted':
            logging.info("Deleted {}".format(event.src_path))
        elif event.event_type == 'moved':
            logging.info("Moved {}".format(event.src_path))
        else:
            logging.warning("Unhandled event type {} on {}".format(event.event_type, event.src_path))


class Watcher:

    def __init__(self, directory):
        try:
            self.observer = Observer()
            logging.info("Initialised Observer!")
            self.watchDirectory = directory
            logging.info("Setting watch directory to: {}".format(self.watchDirectory))
        except:
            logging.error("Error occurred while initialising Observer.")

    def run(self):
        event_handler = Handler()
        logging.info("Initialised Handler!")
        self.observer.schedule(event_handler, self.watchDirectory, recursive=False)
        logging.info("Observer scheduled!")
        logging.info("Starting observer!")
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.info("Observer stopped!")

        self.observer.join()


class Organizer:

    def __init__(self, directory):
        self.organizeDirectory = directory
        self.audio_files_dir = os.path.join(self.organizeDirectory, 'AUDIO FILES')
        self.compressed_files_dir = os.path.join(self.organizeDirectory, 'COMPRESSED FILES')
        self.disk_media_files_dir = os.path.join(self.organizeDirectory, 'DISK AND MEDIA FILES')
        self.data_database_files_dir = os.path.join(self.organizeDirectory, 'DATA DATABASE FILES')
        self.email_files_dir = os.path.join(self.organizeDirectory, 'EMAIL FILES')
        self.executable_files_dir = os.path.join(self.organizeDirectory, 'EXECUTABLE FILES')
        self.font_files_dir = os.path.join(self.organizeDirectory, 'FONT FILES')
        self.image_files_dir = os.path.join(self.organizeDirectory, 'IMAGE FILES')
        self.presentation_files_dir = os.path.join(self.organizeDirectory, 'PRESENTATION FILES')
        self.programming_files_dir = os.path.join(self.organizeDirectory, 'PROGRAMMING FILES')
        self.spreadsheet_files_dir = os.path.join(self.organizeDirectory, 'SPREADSHEET FILES')
        self.system_files_dir = os.path.join(self.organizeDirectory, 'SYSTEM FILES')
        self.video_files_dir = os.path.join(self.organizeDirectory, 'VIDEO FILES')
        self.text_files_dir = os.path.join(self.organizeDirectory, 'TEXT FILES')
        logging.info("Organizer initialised!")

    def organize_folder(self):
        logging.info("Beginning folder organization!")
        for filename in os.listdir(self.organizeDirectory):
            organize(self, os.path.join(self.organizeDirectory, filename))
        logging.info("Folder organization completed!")


def organize(organizer, file_path):
    file_name = os.path.basename(file_path)
    extension = file_name.split(".")[len(file_name.split(".")) - 1]

    try:
        if extension in _AUDIO_FILE_FORMATS:
            if not os.path.exists(organizer.audio_files_dir):
                os.mkdir(organizer.audio_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.audio_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.audio_files_dir))
        elif extension in _COMPRESSED_FILE_FORMATS:
            if not os.path.exists(organizer.compressed_files_dir):
                os.mkdir(organizer.compressed_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.compressed_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.compressed_files_dir))
        elif extension in _DISK_MEDIA_FILE_FORMATS:
            if not os.path.exists(organizer.disk_media_files_dir):
                os.mkdir(organizer.disk_media_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.disk_media_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.disk_media_files_dir))
        elif extension in _DATA_DATABASE_FILE_FORMATS:
            if not os.path.exists(organizer.data_database_files_dir):
                os.mkdir(organizer.data_database_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.data_database_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.data_database_files_dir))
        elif extension in _EMAIL_FILE_FORMATS:
            if not os.path.exists(organizer.email_files_dir):
                os.mkdir(organizer.email_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.email_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.email_files_dir))
        elif extension in _EXECUTABLE_FILE_FORMATS:
            if not os.path.exists(organizer.executable_files_dir):
                os.mkdir(organizer.executable_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.executable_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.executable_files_dir))
        elif extension in _FONT_FILE_FORMATS:
            if not os.path.exists(organizer.font_files_dir):
                os.mkdir(organizer.font_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.font_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.font_files_dir))
        elif extension in _IMAGE_FILE_FORMATS:
            if not os.path.exists(organizer.image_files_dir):
                os.mkdir(organizer.image_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.image_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.image_files_dir))
        elif extension in _PRESENTATION_FILE_FORMATS:
            if not os.path.exists(organizer.presentation_files_dir):
                os.mkdir(organizer.presentation_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.presentation_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.presentation_files_dir))
        elif extension in _PROGRAMMING_FILE_FORMATS:
            if not os.path.exists(organizer.programming_files_dir):
                os.mkdir(organizer.programming_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.programming_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.programming_files_dir))
        elif extension in _SPREADSHEET_FILE_FORMATS:
            if not os.path.exists(organizer.spreadsheet_files_dir):
                os.mkdir(organizer.spreadsheet_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.spreadsheet_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.spreadsheet_files_dir))
        elif extension in _SYSTEM_FILE_FORMATS:
            if not os.path.exists(organizer.system_files_dir):
                os.mkdir(organizer.system_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.system_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.system_files_dir))
        elif extension in _TEXT_FILE_FORMATS:
            if not os.path.exists(organizer.text_files_dir):
                os.mkdir(organizer.text_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.text_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.text_files_dir))
        elif extension in _VIDEO_FILE_FORMATS:
            if not os.path.exists(organizer.video_files_dir):
                os.mkdir(organizer.video_files_dir)
            os.rename(os.path.join(organizer.organizeDirectory, file_name),
                      os.path.join(organizer.video_files_dir, file_name))
            logging.info("Moving {} to {}".format(file_name, organizer.video_files_dir))
    except Exception as e:
        logging.error(str(e))


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_command_line_args():
    parser = argparse.ArgumentParser(description=(
        'Organize your files and start a watching service that automatically organizes your files when added!'))

    parser.add_argument(
        '--folder',
        type=str,
        required=False,
        default=_WATCH_DIRECTORY,
        help="Folder to organize (Provide the absolute path to the folder)"
    )

    parser.add_argument(
        '--watch',
        type=str2bool,
        nargs='?',
        const=True,
        default=True,
        required=False,
        help="Enable a watcher on the folder or not"
    )

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    if args.watch:
        watch = Watcher(args.folder)
        watch.run()
    else:
        Organizer(args.folder).organize_folder()


if __name__ == '__main__':
    main()
