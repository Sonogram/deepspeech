#!/usr/bin/env python3
import sounddevice as sd
from deepspeech import Model
import argparse
from pathlib import Path
import queue

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_WEIGHT = 1.50

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
VALID_WORD_COUNT_WEIGHT = 2.10

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('model_path', type=Path)
    return parser


args = get_parser().parse_args()

fs = 16000
sd.default.samplerate = fs
sd.default.channels = 1

ds = Model(str(args.model_path / 'output_graph.pbmm'), N_FEATURES, N_CONTEXT, str(args.model_path / 'alphabet.txt'),
           BEAM_WIDTH)
ds.enableDecoderWithLM(
    str(args.model_path / 'alphabet.txt'),
    str(args.model_path / 'lm.binary'),
    str(args.model_path / 'trie'),
    LM_WEIGHT,
    VALID_WORD_COUNT_WEIGHT
)
sctx = ds.setupStream()

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    q.put(indata.copy())


# Make sure the file is opened before recording anything:
with sd.InputStream(samplerate=fs, channels=1, callback=callback):
    while True:
        ds.feedAudioContent(sctx, q.get())
        print(ds.intermediateDecode())
