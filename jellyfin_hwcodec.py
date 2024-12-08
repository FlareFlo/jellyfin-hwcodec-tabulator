import argparse
import subprocess

# Taken from: https://jellyfin.org/docs/general/administration/hardware-acceleration/amd#configure-on-linux-host
jellyfin_table = {
    "H264": [
        "VAProfileH264Baseline",
        "VAProfileH264Main",
        "VAProfileH264High",
        "VAProfileH264ConstrainedBaseline"
    ],
    "HEVC": ["VAProfileHEVCMain"],
    "MPEG2": [
        "VAProfileMPEG2Simple",
        "VAProfileMPEG2Main"
    ],
    "VC1": [
        "VAProfileVC1Simple",
        "VAProfileVC1Main",
        "VAProfileVC1Advanced"
    ],
    "VP8": [
        "VAProfileVP8Version0",
        "VAProfileVP8Version1",
        "VAProfileVP8Version2",
        "VAProfileVP8Version3"
    ],
    "VP9": ["VAProfileVP9Profile0"],
    "AV1": ["VAProfileAV1Profile0"],
    "HEVC 10bit": ["VAProfileHEVCMain10"],
    "VP9 10bit": ["VAProfileVP9Profile2"]
}

inverted_table = {}
for codec, profiles in jellyfin_table.items():
    for profile in profiles:
        inverted_table[profile] = codec

def main():
    parser = argparse.ArgumentParser(
        prog='jellyfin_hwcodec',
        description='Enumerates options to tick')

    parser.add_argument('--device', metavar='device', type=str, default='renderD128')

    args = parser.parse_args()
    cmd = subprocess.run(["sudo", "vainfo", "--display", "drm", "--device", f"/dev/dri/{args.device}"], text=True, capture_output=True)
    if cmd.returncode != 0:
        print("vainfo failed with: ", cmd.stderr)
        return

    stdout = cmd.stdout.strip()
    encoders = []
    decoders = []
    for codec in stdout.split("\n"):
        codec = codec.strip()
        if not codec.startswith("VAProfile"):
            continue
        profile, capability = codec.split(":")
        profile = profile.strip()
        capability = capability.strip()

        match capability:
            case "VAEntrypointVLD":
                capability = "decode"
            case "VAEntrypointEncSlice":
                capability = "encode"
        pretty_profile = inverted_table.get(profile)
        if pretty_profile is not None:
            if capability == "decode":
                decoders.append(pretty_profile)
            elif capability == "encode":
                encoders.append(pretty_profile)

    encoders = sorted(list(set(encoders)))
    decoders = sorted(list(set(decoders)))
    print("Decoders:")
    for r in decoders:
        print("\t", r)

    print("Encoders:")
    for r in encoders:
        print("\t", r)

if __name__ == '__main__':
    main()