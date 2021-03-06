# /bin/python3
"""main()
Run the editor directly as a module.
"""
# pylint: disable=invalid-name,line-too-long

try:
    from HDR10PlusEditor.HDR10Plus import json as HDR10PlusJSON
    from HDR10PlusEditor.HDR10Plus import HDR10Plus
except ModuleNotFoundError:
    from HDR10Plus import json as HDR10PlusJSON
    from HDR10Plus import HDR10Plus
import argparse


def main():
    """Run the script directly
    Keyword arguments:
    """
    parser = argparse.ArgumentParser(
        description="Add/remove frames from a HDR10+ JSON."
    )
    parser.add_argument(
        "--input", "-i", dest="input", type=str, help="Input JSON path.", required=True
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        type=str,
        help="Output JSON path.",
        required=True,
    )
    parser.add_argument(
        "--scene",
        "-s",
        dest="scene",
        type=int,
        help="Scene number to apply edits.",
        required=True,
    )
    parser.add_argument(
        "--adjust",
        "-a",
        dest="adjust",
        type=int,
        help="How to adjust the scene, positive makes it longer, negative makes it shorter.",
        required=True,
    )
    args = parser.parse_args()
    print(f"Loading file '{args.input}'...")
    HDR10PlusJSON_DCT = HDR10PlusJSON.load(json_file=args.input)
    HDR10Plus_Object = HDR10Plus.HDR10Plus(HDR10PlusJSON_DCT)
    HDR10Plus_Object.verify()
    print("Summary of HDR10+")
    print(HDR10Plus_Object.summary())
    HDR10Plus_Object.modify_scene_frames(args.scene, args.adjust)
    HDR10Plus_Object.verify()
    print("Summary of HDR10+ after editing...")
    print(HDR10Plus_Object.summary())
    print(f"Saving JSON to '{args.output}'...")
    HDR10Plus_Object.export_as_json(args.output)
    print("Saved...")


if __name__ == "__main__":
    main()
