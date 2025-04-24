from iis.collector import Collector


def parse(import_folder: str, export_folder: str, job_name: str):
    Collector().collect(import_folder, export_folder, job_name)
