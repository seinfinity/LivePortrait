#!/bin/bash

# 기본 설정
SOURCE="assets/examples/source/s9.jpg"  # -s source video.mp4 경로
OUTPUT_DIR="animations/"  # output 저장될 폴더 경로
DRIVING_DIR="assets/examples/driving"  # Driving video가 포함된 directory
ANIMATION_REGION="lip"  # --animation-region 인자

# 모든 MP4 파일에 대해 반복 실행
for DRIVING_FILE in "$DRIVING_DIR"/*.mp4; do
    echo "Processing $DRIVING_FILE..."
    
    # python 명령어로 inference.py 실행
    python inference.py \
        -s "$SOURCE" \
        -d "$DRIVING_FILE" \
        --animation-region "$ANIMATION_REGION"

    echo "Saved result for $DRIVING_FILE in $OUTPUT_DIR"
done
