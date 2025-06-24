"""
图像消失动画效果
包含淡出、滑出等效果
"""

from typing import List
import numpy as np
from PIL import Image


def fade_out(img: Image.Image, num_frames: int = 20) -> List[Image.Image]:
    """图像淡出效果（由完全显示到透明）"""
    frames = []
    
    # 确保图像有Alpha通道
    img = img.convert("RGBA")
    img_array = np.array(img)
    
    # 创建一系列透明度递减的帧
    for step in range(num_frames + 1):
        alpha = 1 - (step / num_frames)  # 从1到0的透明度
        
        # 创建当前帧的副本
        frame_array = img_array.copy()
        
        # 修改alpha通道
        frame_array[:, :, 3] = (frame_array[:, :, 3] * alpha).astype(np.uint8)
        
        # 转换回PIL图像
        frame = Image.fromarray(frame_array)
        frames.append(frame)
    
    return frames


def slide_out_to_right(img: Image.Image, num_frames: int = 20) -> List[Image.Image]:
    """图像向右滑出"""
    frames = []
    w, h = img.size
    img = img.convert("RGBA")  # 确保有Alpha通道
    
    for step in range(num_frames + 1):
        # 计算当前位置，从图像完全显示到完全滑出右侧
        progress = step / num_frames
        start_x = int(w * progress)
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在计算出的位置
        canvas.paste(img, (start_x, 0), img)
        
        frames.append(canvas)
    
    return frames


def slide_out_to_bottom(img: Image.Image, num_frames: int = 20) -> List[Image.Image]:
    """图像向下滑出"""
    frames = []
    w, h = img.size
    img = img.convert("RGBA")  # 确保有Alpha通道
    
    for step in range(num_frames + 1):
        # 计算当前位置，从图像完全显示到完全滑出底部
        progress = step / num_frames
        start_y = int(h * progress)
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在计算出的位置
        canvas.paste(img, (0, start_y), img)
        
        frames.append(canvas)
    
    return frames


def zoom_out(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    图像缩小至中心点消失。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    original_width, original_height = img.size
    
    scale_factors = np.linspace(1.0, 0.01, num_frames)
    
    for scale in scale_factors:
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        if new_width < 1 or new_height < 1:
            resized_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        else:
            resized_img = img.resize((new_width, new_height), resample=Image.BICUBIC)
        
        background = Image.new('RGBA', img.size, (255, 255, 255, 0))
        
        paste_x = (original_width - new_width) // 2
        paste_y = (original_height - new_height) // 2
        
        background.paste(resized_img, (paste_x, paste_y), resized_img)
        frames.append(background)
        
    return frames
