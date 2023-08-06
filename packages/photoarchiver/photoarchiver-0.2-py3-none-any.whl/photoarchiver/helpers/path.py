import os

from photoarchiver.helpers.exif import get_file_metadata


def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[-1].lower()


def get_destination_path(file_path) -> str:
    file_metadata = get_file_metadata(file_path)
    file_extension = get_file_extension(file_path)
    file_directory = f"{file_metadata['creation_time']:%Y/%-m - %B - Week %V}"

    # create new file name
    time_string = f"{file_metadata['creation_time']:%Y-%b-%d %H-%M-%S}"
    location_string = "-".join(filter(None, [file_metadata.get("location").get(k)
                                             for k in ["cc", "name"] if file_metadata.get("location")]))

    new_file_name = "-".join(filter(None, [time_string, location_string])) + file_extension
    return os.path.join(file_directory, new_file_name)


def get_deduplicated_destination_path(destionation_path) -> str:
    counter = 1
    deduplicated_destination_path = destionation_path
    while os.path.exists(deduplicated_destination_path):
        path_parts = destionation_path.rsplit(".")
        path_parts[0] = f"{path_parts[0]}_{counter}"
        counter += 1
        deduplicated_destination_path = "".join(path_parts)

    return deduplicated_destination_path
