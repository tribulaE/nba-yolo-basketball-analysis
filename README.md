# AI/ML NBA Basketball Analysis System (WIP)

This project builds an AI/ML basketball analysis pipeline using YOLO, OpenCV, PyTorch and Python.

## Overview
It takes broadcast footage and uses AI to track players, identify teams by jersey color and track the ball 

## Planned Features
- Player and ball detection using YOLO  
- Passes and Interceptions also ball control displayed
- Multi-object tracking across frames  
- Custom object detector training  
- Team assignment using zero-shot image classification (Hugging Face)  

## Status
 Complete

## Credits
- Tutorial inspiration: https://youtu.be/QqVahw9tBfw

## Docker 
- Docker execution: Containerized the full NBA video analytics pipeline with all system and Python dependencies, to enable reproducible, one command execution on any machine
- Docker outputs: Implemented vloume mounted output handling so processed tracking videos are saved outside the container, ensuring clean separation between code, runtime environment, and generated artifcats.