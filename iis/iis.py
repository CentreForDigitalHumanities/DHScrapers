from iis.collector import Collector


def parse(import_folder: str, export_folder: str):
    Collector().collect(import_folder, export_folder)
