#!/opt/inaSpeechSegEnv/bin/python
# coding: utf-8

import sys
import os
import subprocess
from glob import glob
from pathlib import Path
from joblib import Parallel, delayed
from multiprocessing import cpu_count


def run_inaspeech(audio, output_folder):
    output_csv = f"{output_folder}/{Path(audio).stem}.csv"
    if os.path.exists(f"{output_csv}"):
        print(f"File \"{output_csv}\" already exists, skipping...",
              file=sys.stderr)
        return
    print(f"Running ina_speech_segmenter on {audio}")
    ina_path = "/opt/inaSpeechSegEnv/bin"
    cmd = subprocess.run([
        f'{ina_path}/ina_speech_segmenter.py',
        '-d', 'smn',
        '-g', 'false',
        '-i', f"{audio}",
        '-o', f"{output_folder}"
    ], capture_output=True)
    if cmd.returncode != 0:
        raise OSError(f"ina_speech_segmenter.py failed with: {cmd.stderr}")
    else:
        print(f"ina_speech_segmenter of {audio} finished successfully")
        return f"{output_csv}"


def run_segmentation(audio_folder, output_folder):
    audio_files = glob(f"{audio_folder}/*.wav")
    if audio_files:
        Parallel(n_jobs=int(cpu_count()/2))(delayed(run_inaspeech)
                                                   (audio_file, output_folder)
                                            for audio_file in audio_files)
    else:
        print(f"No audio files found on {audio_folder}", file=sys.stderr)


if __name__ == '__main__':
    def show_usage():
        print(f"Usage: {sys.argv[0]} <audio_folder> <output_folder>\n",
              file=sys.stderr)
        sys.exit(2)
    if len(sys.argv) != 3:
        show_usage()
    audio_folder = sys.argv[1]
    output_folder = sys.argv[2]
    if not os.path.isdir(audio_folder):
        print(f"Error: \"{audio_folder}\" does not exist or is not a folder")
        show_usage()
    elif not os.path.isdir(output_folder):
        print(f"Error: \"{output_folder}\" does not exist or is not a folder")
        show_usage()
    else:
        run_segmentation(audio_folder, output_folder)
