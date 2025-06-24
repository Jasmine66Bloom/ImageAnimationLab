"""
图像强调动画效果
包含缩放、脉冲等效果
"""

from typing import List
import numpy as np
from PIL import Image


def pulse(img: Image.Image, max_scale: float = 1.2, num_frames: int = 20) -> List[Image.Image]:
    """图像脉冲效果（先放大后恢复原始大小）"""
    frames = []
    w, h = img.size
    
    # 确保所有帧的尺寸与原始图像一致
    # 生成放大阶段的帧
    for step in range(num_frames // 2 + 1):
        scale = 1 + (max_scale - 1) * step / (num_frames // 2)
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        
        # 调整图像大小
        scaled_img = img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将缩放后的图像居中放置
        paste_x = (w - scaled_w) // 2
        paste_y = (h - scaled_h) // 2
        canvas.paste(scaled_img, (paste_x, paste_y))
        
        frames.append(canvas)
    
    # 生成缩小阶段的帧（反向）
    for step in range(num_frames // 2, -1, -1):
        scale = 1 + (max_scale - 1) * step / (num_frames // 2)
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        
        # 调整图像大小
        scaled_img = img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将缩放后的图像居中放置
        paste_x = (w - scaled_w) // 2
        paste_y = (h - scaled_h) // 2
        canvas.paste(scaled_img, (paste_x, paste_y))
        
        frames.append(canvas)
    
    return frames


def shake(img: Image.Image, amplitude: int = 10, num_frames: int = 20) -> List[Image.Image]:
    """图像左右摇晃效果"""
    frames = []
    w, h = img.size
    
    # 增大振幅以使效果更明显
    amplitude = min(amplitude, w // 4)  # 限制振幅不超过图像宽度的1/4
    
    # 计算摇晃位置
    for step in range(num_frames + 1):
        # 使用正弦函数生成平滑的摇晃效果
        angle = 2 * np.pi * step / num_frames
        offset = int(amplitude * np.sin(angle))
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在偏移位置，确保在画布范围内
        paste_x = offset
        canvas.paste(img, (paste_x, 0), img.convert("RGBA"))
        
        frames.append(canvas)
    
    return frames


def bounce(img: Image.Image, amplitude: int = 20, num_frames: int = 20) -> List[Image.Image]:
    """图像上下弹跳效果"""
    frames = []
    w, h = img.size
    
    # 增大振幅以使效果更明显
    amplitude = min(amplitude, h // 4)  # 限制振幅不超过图像高度的1/4
    
    # 计算弹跳位置
    for step in range(num_frames + 1):
        # 使用正弦函数生成平滑的弹跳效果
        angle = 2 * np.pi * step / num_frames
        offset = int(amplitude * np.sin(angle))
        
        # 创建与原始图像大小相同的透明画布
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        
        # 将图像放置在偏移位置，确保在画布范围内
        paste_y = -offset  # 正弦波峰对应图像上移
        canvas.paste(img, (0, paste_y), img.convert("RGBA"))
        
        frames.append(canvas)
    
    return frames


def spin(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    让图像快速旋转360度。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    for i in range(num_frames):
        angle = (i / (num_frames - 1)) * 360 if num_frames > 1 else 0
        # 使用 expand=True 来确保旋转后的图像不会被裁剪
        rotated_img = img.rotate(angle, resample=Image.BICUBIC, expand=True)
        
        # 创建一个与原始图像大小相同的新背景
        background = Image.new('RGBA', img.size, (255, 255, 255, 0))
        
        # 计算将旋转后的图像粘贴到中心的坐标
        paste_x = (img.width - rotated_img.width) // 2
        paste_y = (img.height - rotated_img.height) // 2
        
        background.paste(rotated_img, (paste_x, paste_y), rotated_img)
        frames.append(background)
        
    return frames


def tada(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    一个"Tada!"效果，结合了放大、缩小和轻微的摇摆。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    # 动画分为几个阶段：放大 -> 缩小 -> 摇摆
    p1 = int(num_frames * 0.2)
    p2 = int(num_frames * 0.2)
    p3 = int(num_frames * 0.1)
    p4 = int(num_frames * 0.1)
    p5 = int(num_frames * 0.1)
    p6 = int(num_frames * 0.1)
    p_rest = num_frames - (p1 + p2 + p3 + p4 + p5 + p6)
    if p_rest < 0: p_rest = 0

    # 阶段1 & 2: 放大和缩小
    scales = list(np.linspace(1.0, 1.2, p1)) + list(np.linspace(1.2, 0.9, p2))
    angles = [0] * (p1 + p2)

    # 阶段 3-6: 摇摆
    angles += list(np.linspace(0, -15, p3))
    angles += list(np.linspace(-15, 10, p4))
    angles += list(np.linspace(10, -5, p5))
    angles += list(np.linspace(-5, 0, p6))
    scales += [1.0] * (p3 + p4 + p5 + p6) # Scale back to 1.0 during shake
    
    # 补齐剩余帧
    scales += [1.0] * p_rest
    angles += [0] * p_rest
    
    # 确保列表长度与 num_frames 匹配
    scales = scales[:num_frames]
    angles = angles[:num_frames]
    if len(scales) < num_frames:
        scales.extend([1.0] * (num_frames - len(scales)))
    if len(angles) < num_frames:
        angles.extend([0] * (num_frames - len(angles)))

    for i in range(num_frames):
        scale = scales[i]
        angle = angles[i]
        
        new_size = (int(img.width * scale), int(img.height * scale))
        scaled_img = img.resize(new_size, resample=Image.BICUBIC)
        rotated_img = scaled_img.rotate(angle, resample=Image.BICUBIC, expand=True)

        background = Image.new('RGBA', img.size, (255, 255, 255, 0))
        paste_x = (img.width - rotated_img.width) // 2
        paste_y = (img.height - rotated_img.height) // 2
        background.paste(rotated_img, (paste_x, paste_y), rotated_img)
        frames.append(background)
        
    return frames


def flash(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    图像闪烁效果，通过快速改变透明度实现。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    # 一个周期是 亮 -> 暗 -> 亮
    cycle_len = max(4, num_frames // 4) # Ensure at least some flashes
    
    for i in range(num_frames):
        # Use modulo to create a flashing cycle
        if (i // cycle_len) % 2 == 0:
            frames.append(img.copy()) # Visible
        else:
            # Invisible frame
            frames.append(Image.new('RGBA', img.size, (0, 0, 0, 0)))
            
    return frames


def swing(img: Image.Image, num_frames: int) -> List[Image.Image]:
    """
    图像像钟摆一样来回摆动。

    Args:
        img: 输入图像 (RGBA)
        num_frames: 动画的总帧数

    Returns:
        动画帧列表
    """
    frames = []
    max_angle = 15 # Maximum swing angle
    
    # Use a sine wave to model the swing motion
    for i in range(num_frames):
        # A full swing (left-right-center) should happen over the duration
        angle = max_angle * np.sin(2 * np.pi * i / num_frames)
        
        # Set the rotation origin to top-center
        # PIL rotates around the center, so we need to translate
        rotated_img = img.rotate(angle, resample=Image.BICUBIC, expand=False)
        
        # Create a background to paste onto
        background = Image.new('RGBA', img.size, (255, 255, 255, 0))
        
        # Paste the rotated image in the center
        paste_x = (img.width - rotated_img.width) // 2
        paste_y = (img.height - rotated_img.height) // 2
        background.paste(rotated_img, (paste_x, paste_y), rotated_img)
        frames.append(background)
        
    return frames
