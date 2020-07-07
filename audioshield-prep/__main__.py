import argparse
import random
from pathlib import Path
from pydub import AudioSegment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-warm-up', help="skip warm up songs", action="store_true", default=False)
    parser.add_argument("output", help="output MP3 path")
    args = parser.parse_args()

    length = int(input(">> How many minutes: ")) * 60
    print(length)

    # Gather paths
    cwd = Path.cwd()
    slows = list(cwd.glob("slow/*.mp3"))
    fasts = list(cwd.glob("fast/*.mp3"))
    if len(slows) < 2:
        raise Exception("Not enough slow songs")
    if len(fasts) == 0:
        raise Exception("No fast songs")

    # Pick start song
    if args.no_warm_up:
        start_sample = AudioSegment.empty()
        slow_duration = 0
        print('Skipping warmup.')
    else:
        random.shuffle(slows)
        slows = random.choices(slows, k=2)
        start = slows[0]

        start_sample = AudioSegment.from_mp3(str(start))
        slow_duration = start_sample.duration_seconds
        print('Warmup: {}s - {}'.format(slow_duration, start))

    # Gather fast sample lengths
    print("Gathering input durations (this may take a while)...")
    durations = [(str(k), AudioSegment.from_mp3(str(k)).duration_seconds) for k in fasts]

    print("Generating permutation...")
    solution = []
    random.shuffle(durations)
    current_duration = 0
    for k, v in durations:
        solution.append(k)
        current_duration += v
        if current_duration + slow_duration > length:
            print("Solution of {}s: {}".format(current_duration + slow_duration, solution))
            break

    print("Building output file...")
    out = start_sample
    for k in solution:
        segment = AudioSegment.from_mp3(k).normalize()
        # Only crossfade if the sample is long enough - anything smaller is probably a purposely empty segment
        if out.duration_seconds > 2:
            out = out.append(segment, crossfade=2000)
        else:
            out = out.append(segment, crossfade=0)
    out.export(args.output, format='mp3')
    print("Done!")
