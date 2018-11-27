import sounddevice as sd
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int,
    help='input device (numeric ID or substring)')
args = parser.parse_args()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, flush=True)
    queue.put(indata.copy())


if args.list_devices:
    print(sd.query_devices())
    parser.exit()

fs = 16000
sd.default.samplerate = fs
sd.default.channels = 1

with sd.InputStream(
        samplerate=16000,
        device=args.device,
        channels=args.channels,
        callback=callback
):
    myrecording = sd.rec(int(5 * fs))
