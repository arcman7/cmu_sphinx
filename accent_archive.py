import os
# import wget
import tarfile
import argparse
import csv
from multiprocessing.pool import ThreadPool
import subprocess
import zipfile
import sys
import zipfile


is_windows = sys.platform.startswith('win')

parser = argparse.ArgumentParser(description='Downloads and processes Speech Accent Archive dataset.')
parser.add_argument("--target-dir", default='accent_archive', type=str, help="Directory to store the dataset.")
parser.add_argument("--download-path", default='archive.zip', type=str, help="Path to the Speech Accent Archive folder if downloaded (Optional).")
parser.add_argument('--sample-rate', default=16000, type=int, help='Sample rate')
parser.add_argument('--min-duration', default=0, type=int,
                    help='Prunes training samples shorter than the min duration (given in seconds, default 1)')
parser.add_argument('--max-duration', default=100, type=int,
                    help='Prunes training samples longer than the max duration (given in seconds, default 15)')
# parser.add_argument('--files-to-process', default="cv-valid-dev.csv,cv-valid-test.csv,cv-valid-train.csv",
#                     type=str, help='list of *.csv file names to process')
args = parser.parse_args()
SPEECH_ACCENT_ARCHIVE = "https://www.kaggle.com/rtatman/speech-accent-archive/download"

ListDir = os.listdir
current_dir = os.path.dirname(os.path.realpath(__file__))
# windows sox executable path
# C:\Program Files (x86)\sox-14-4-2

# test command:
# sox 'C:\Users\Ryan\projects\speech\ch8_sphinx\Sphinx\accent_archive\AA_unpacked\recordings\recordings\vlaams3.mp3' -r 16000 -b 16 -c 1 'accent_archive\wav\train_vlaams3.wav'

def convert_to_wav(csv_file, target_dir, dataset_type):
    """ Read *.csv file description, convert mp3 to wav, process text.
        Save results to target_dir.

    Args:
        csv_file: str, path to *.csv file with data description, usually start from 'cv-'
        target_dir: str, path to dir to save results; wav/ and txt/ dirs will be created
        dataset_type: str, "train" or "test" dataset
    """
    wav_dir = os.path.join(current_dir, target_dir, 'wav')
    etc_dir = os.path.join(current_dir, target_dir, 'etc')
    dataset_name = os.path.basename(target_dir)
    os.makedirs(wav_dir, exist_ok=True)
    os.makedirs(etc_dir, exist_ok=True)
    path_to_data = os.path.dirname(csv_file)
    def process(x):
        file_path, wav_path = x
        cmd = [
            'C:\\Program Files (x86)\\sox-14-4-2\\sox.exe' if is_windows else 'sox',
            os.path.join(current_dir, path_to_data, 'recordings', 'recordings', file_path + '.mp3'),
            '-r',
            str(args.sample_rate),
            '-b',
            '16',
            '-c',
            '1',
            wav_path,
        ]
        # subprocess.call(cmd)
        subprocess.run(cmd, check=True)

    # The Accent Archive uses the same text transcript for every audio recording
    text = None
    with open(os.path.join(path_to_data, 'reading-passage.txt'), 'r') as f:
        text = f.read().replace('\n', '').replace(':', '').replace('  ', ' ').upper()#.lower()
    
    print('Converting mp3 to wav for {}.'.format(csv_file))
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        with open(os.path.join(etc_dir, dataset_name + '_'+ dataset_type + '.transcription'), 'w') as trans_file, \
            open(os.path.join(etc_dir, dataset_name + '_'+ dataset_type + '.fileids'), 'w') as ids_file:
            for row in reader: 
                file_name = row['filename']
                if row['file_missing?'] == 'TRUE' or file_name == 'nicaragua' or file_name == 'sinhalese1':
                    continue
                wav_file_name = dataset_type + '_'+ os.path.splitext(os.path.basename(file_name))[0]
                wav_path = os.path.join(wav_dir, wav_file_name + '.wav')
                ids_file.write(wav_file_name + '\n')
                # The Accent Archive uses the same text transcript for every audio recording
                trans_file.write('<s> '+ text + ' </s> (' + wav_file_name + ')' + '\n')
                data.append((file_name,wav_path))

        # DEBUG - no parralization:
        # for d in data:
        #     process(d)
        with ThreadPool(10) as pool:
            pool.map(process, data)

def main():
    target_dir = args.target_dir
    os.makedirs(target_dir, exist_ok=True)

    target_unpacked_dir = os.path.join(target_dir, "AA_unpacked")
    os.makedirs(target_unpacked_dir, exist_ok=True)

    if args.download_path and os.path.exists(args.download_path):
        print('Find existing file {}'.format(args.download_path))
        target_file = args.download_path
    else:
        print("Could not find downloaded Accent archive, Downloading corpus...")
        filename = wget.download(SPEECH_ACCENT_ARCHIVE, target_dir)
        target_file = os.path.join(target_dir, os.path.basename(filename))

    print("Unpacking corpus to {} ...".format(target_unpacked_dir))
    with zipfile.ZipFile(target_file, 'r') as zip_ref:
        zip_ref.extractall(target_unpacked_dir)
    # else:
    #     tar = tarfile.open(target_file)
    #     tar.extractall(target_unpacked_dir)
    #     tar.close()

    convert_to_wav(os.path.join(target_unpacked_dir, 'speakers_all.csv'),
                    target_dir, 'train')
    # convert_to_wav(os.path.join(target_unpacked_dir, 'archive/', 'speakers_all.csv'),
                    # target_dir, 'test')

if __name__ == "__main__":
    main()
