"""
To prevent duplicate code being pasted between scripts, common functions should be
put here. No function should modify or create video/audio files on its own.
"""

from typing import List, Tuple, Union
from auto_editor.utils.log import Log

def get_stdout(cmd: List[str]) -> str:
    from subprocess import Popen, PIPE, STDOUT

    stdout, _ = Popen(cmd, stdout=PIPE, stderr=STDOUT).communicate()
    return stdout.decode()

def clean_list(x: List[str], rm_chars: str) -> list:
    new_list = []
    for item in x:
        for char in rm_chars:
            item = item.replace(char, '')
        new_list.append(item)
    return new_list

def aspect_ratio(width: int, height: int) -> Union[Tuple[int, int], Tuple[None, None]]:
    if height == 0:
        return None, None

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    c = gcd(width, height)
    return width // c, height // c

def get_new_length(chunks: List[Tuple[int, int, float]], fps: float) -> float:
    time_in_frames = 0.0
    for chunk in chunks:
        leng = chunk[1] - chunk[0]
        if chunk[2] != 99999:
            time_in_frames += leng * (1 / chunk[2])
    return time_in_frames / fps

def human_readable_time(time_in_secs: Union[int, float]) -> str:
    units = 'seconds'
    if time_in_secs >= 3600:
        time_in_secs = round(time_in_secs / 3600, 1)
        if time_in_secs % 1 == 0:
            time_in_secs = round(time_in_secs)
        units = 'hours'
    if time_in_secs >= 60:
        time_in_secs = round(time_in_secs / 60, 1)
        if time_in_secs >= 10 or time_in_secs % 1 == 0:
            time_in_secs = round(time_in_secs)
        units = 'minutes'
    return '{} {}'.format(time_in_secs, units)

def open_with_system_default(path: str, log: Log) -> None:
    from subprocess import call
    try:  # should work on Windows
        from os import startfile
        startfile(path)
    except ImportError:
        try:  # should work on MacOS and most Linux versions
            call(['open', path])
        except Exception:
            try: # should work on WSL2
                call(['cmd.exe', '/C', 'start', path])
            except Exception:
                try: # should work on various other Linux distros
                    call(['xdg-open', path])
                except Exception:
                    log.warning('Could not open output file.')

def fnone(val: object) -> bool:
    return val == 'none' or val == 'unset' or val is None

def append_filename(path: str, val: str) -> str:
    from os.path import splitext

    root, ext = splitext(path)
    return root + val + ext

def set_output_name(path: str, inp_ext: str, making_data_file: bool, args: object) -> str:
    from os.path import splitext

    root, ext = splitext(path)

    if args.export_as_json:
        return root + '.json'
    if args.export_to_final_cut_pro:
        return root + '.fcpxml'
    if args.export_to_shotcut:
        return root + '.mlt'
    if making_data_file:
        return root + '.xml'
    if args.export_as_audio:
        return root + '_ALTERED.wav'
    if ext == '':
        if inp_ext is None:
            return root
        return root + inp_ext

    return root + '_ALTERED' + ext
