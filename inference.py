# coding: utf-8
import glob
import os
import os.path as osp
import tyro
import subprocess
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline


def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})

def fast_check_args(args: ArgumentConfig):
    if args.source_folder:
        args.source = glob.glob(osp.join(args.source_folder, '*.mp4'))  # 폴더 내의 .mp4 파일들을 리스트로 수집
        if not args.source:
            raise FileNotFoundError(f"No video files found in the source folder: {args.source_folder}")
    else:
        if not isinstance(args.source, list):
            args.source = [args.source]  # source가 리스트가 아니면 리스트로 변환
        for source in args.source:
            if not osp.exists(source):
                raise FileNotFoundError(f"source info not found: {source}")
    
    if not osp.exists(args.driving):
        raise FileNotFoundError(f"driving info not found: {args.driving}")

def main():
    tyro.extras.set_accent_color("bright_cyan")
    args = tyro.cli(ArgumentConfig)

    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    if osp.exists(ffmpeg_dir):
        os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

    if not fast_check_ffmpeg():
        raise ImportError(
            "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
        )

    fast_check_args(args)

    inference_cfg = partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = partial_fields(CropConfig, args.__dict__)

    live_portrait_pipeline = LivePortraitPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg
    )

    for source in args.source:
        args.source = source
        live_portrait_pipeline.execute(args)

if __name__ == "__main__":
    main()

# def fast_check_ffmpeg():
#     try:
#         subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
#         return True
#     except:
#         return False


# def fast_check_args(args: ArgumentConfig):
#     if not osp.exists(args.source):
#         raise FileNotFoundError(f"source info not found: {args.source}")
#     if not osp.exists(args.driving):
#         raise FileNotFoundError(f"driving info not found: {args.driving}")


# def main():
#     # set tyro theme
#     tyro.extras.set_accent_color("bright_cyan")
#     args = tyro.cli(ArgumentConfig)

#     ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
#     if osp.exists(ffmpeg_dir):
#         os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

#     if not fast_check_ffmpeg():
#         raise ImportError(
#             "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
#         )

#     fast_check_args(args)

#     # specify configs for inference
#     inference_cfg = partial_fields(InferenceConfig, args.__dict__)
#     crop_cfg = partial_fields(CropConfig, args.__dict__)

#     live_portrait_pipeline = LivePortraitPipeline(
#         inference_cfg=inference_cfg,
#         crop_cfg=crop_cfg
#     )

#     # run
#     live_portrait_pipeline.execute(args)


# if __name__ == "__main__":
#     main()
