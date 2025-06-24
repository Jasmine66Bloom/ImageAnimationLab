"""
图像出现动画效果
包含淡入、滑入等效果
"""

from typing import List
import numpy as np
from PIL import Image


def fade_in(img: Image.Image, num_frames: int = 15) -> list[Image.Image]:
    """淡入出现"""
    frames = []
    for i in np.linspace(0, 1, num_frames):
        alpha_img = img.copy()
        alpha = int(255 * i)
        alpha_img.putalpha(alpha)
        frames.append(alpha_img)
    return frames


def slide_in_from_left(img: Image.Image, num_frames: int = 15) -> list[Image.Image]:
    """图像从左侧滑入"""
    frames = []
    w, h = img.size
    img = img.convert("RGBA")  # 确保有Alpha通道
    
    for step in range(num_frames + 1):
        # 计算当前位置，从图像完全在左侧外到完全显示
        progress = step / num_frames
        start_x = int(-w * (1 - progress))
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在计算出的位置
        canvas.paste(img, (start_x, 0), img)
        
        frames.append(canvas)
    
    return frames


def slide_in_from_top(img: Image.Image, num_frames: int = 15) -> list[Image.Image]:
    """图像从顶部滑入"""
    frames = []
    w, h = img.size
    img = img.convert("RGBA")  # 确保有Alpha通道
    
    for step in range(num_frames + 1):
        # 计算当前位置，从图像完全在顶部外到完全显示
        progress = step / num_frames
        start_y = int(-h * (1 - progress))
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在计算出的位置
        canvas.paste(img, (0, start_y), img)
        
        frames.append(canvas)
    
    return frames


def zoom_in(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    图像从中心小点放大出现。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    original_width, original_height = img.size
    
    scale_factors = np.linspace(0.01, 1.0, num_frames)
    
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
