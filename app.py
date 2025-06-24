"""图像动画实验室
提供基本的图像动画效果（翻转、平移、旋转），可生成 GIF 或 MP4。
前端使用 Gradio 构建。
"""

import io
import os
import time
import io
import tempfile
from pathlib import Path
from io import BytesIO
from typing import Tuple

import numpy as np
import imageio
from PIL import Image
import gradio as gr

from animations.appear import fade_in, slide_in_from_left, slide_in_from_top, zoom_in
from animations.disappear import fade_out, slide_out_to_right, slide_out_to_bottom, zoom_out
from animations.emphasis import pulse, shake, bounce, spin, tada, flash, swing

EFFECTS = {
    # 入场效果
    "淡入": fade_in,
    "滑入": slide_in_from_left,
    "顶部滑入": slide_in_from_top,
    "放大出现": zoom_in,
    # 消失效果
    "淡出": fade_out,
    "滑出": slide_out_to_right,
    "底部滑出": slide_out_to_bottom,
    "缩小消失": zoom_out,
    # 强调效果
    "脉冲": pulse,
    "摇晃": shake,
    "弹跳": bounce,
    "旋转": spin,
    "惊喜": tada,
    "闪烁": flash,
    "摆动": swing
}

# -------------- 核心处理 -------------- #

def make_animation(img: Image.Image, effect_name: str, fmt: str, duration_sec: float = 1.0, fps: int = 15) -> Tuple[bytes, str]:
    """
    根据选择的效果生成动画，并返回指定格式的数据。
    
    Args:
        img: 输入图像
        effect_name: 效果名称
        fmt: 输出格式 ("GIF" 或 "MP4")
        duration_sec: 动画持续时间（秒）
        fps: 每秒帧数
        
    Returns:
        动画数据和MIME类型
    """
    # 获取对应的效果函数
    effect_fn = EFFECTS.get(effect_name)
    if effect_fn is None:
        return None, None

    # 确保输入图像是高质量的RGBA模式
    img_rgba = img.convert("RGBA")

    # 计算总帧数并生成动画帧
    num_frames = int(duration_sec * fps)
    frames = effect_fn(img_rgba, num_frames=num_frames)

    # 创建一个内存缓冲区来存储动画
    buffer = BytesIO()

    if fmt == "GIF":
        # 计算每帧延迟（秒）
        frame_delay = duration_sec / len(frames)

        # 保存为GIF，移除特定的quantizer以使用Pillow的默认设置，可能提升画质
        imageio.mimsave(buffer, frames, format="GIF", duration=frame_delay)
        return buffer.getvalue(), "image/gif"
    else:  # MP4
        # 将PIL图像转换为numpy数组
        np_frames = [np.array(frame) for frame in frames]

        # 创建临时文件来存储MP4
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_path = temp_file.name

        # 保存为MP4
        imageio.mimsave(temp_path, np_frames, format="mp4", fps=fps, codec="libx264", quality=8, pixelformat="yuv420p", macro_block_size=1)

        # 读取生成的MP4文件
        with open(temp_path, "rb") as f:
            data = f.read()

        # 删除临时文件
        try:
            os.unlink(temp_path)
        except:
            pass

        return data, "video/mp4"


# -------------- Gradio 界面 -------------- #

def interface_fn(img: Image.Image, effect_name: str, output_fmt: str, duration_sec: float, fps: int):
    """处理用户输入并生成动画。"""
    if img is None:
        return None, None
    
    # 获取选择的动画效果函数
    effect_fn = EFFECTS.get(effect_name)
    if effect_fn is None:
        return None, None
    
    # 计算总帧数
    num_frames = int(duration_sec * fps)
    
    # 只生成用户选择的输出格式
    data, mime = make_animation(img, effect_name, output_fmt, duration_sec=duration_sec, fps=fps)
    
    # 使用固定文件名保存输出
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # 每个格式使用固定文件名
    if output_fmt == "GIF":
        output_path = output_dir / "animation.gif"
        output_path.write_bytes(data)
        return output_path.as_posix(), None
    else:  # MP4
        output_path = output_dir / "animation.mp4"
        output_path.write_bytes(data)
        return None, output_path.as_posix()


def build_interface():
    """构建 Gradio 界面。"""
    # 定义自定义CSS样式
    custom_css = """
    .image-container, .video-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        background-color: #f5f5f5 !important;
        border-radius: 8px !important;
        height: 400px; /* 明确设置高度 */
    }
    .image-container img, .video-container video {
        max-width: 100% !important;
        max-height: 100% !important;
        object-fit: contain !important;
    }
    """
    
    with gr.Blocks(theme=gr.themes.Default(), css=custom_css) as demo:
        gr.Markdown("# 图像动画实验室")

        # 定义动画效果
        appear_effects = ["淡入", "滑入", "顶部滑入", "放大出现"]
        disappear_effects = ["淡出", "滑出", "底部滑出", "缩小消失"]
        emphasis_effects = ["脉冲", "摇晃", "弹跳", "旋转", "惊喜", "闪烁", "摆动"]
        all_effects_grouped = {
            "出现效果": appear_effects,
            "消失效果": disappear_effects,
            "强调效果": emphasis_effects,
        }
        
        # 1. 输入和输出在同一行
        with gr.Row(equal_height=True):
            # 左侧：描述 + 输入图像
            with gr.Column(scale=1):
                gr.Markdown("上传图片，选择动画效果，生成 GIF 或 MP4 动画。")
                inp_img = gr.Image(
                    show_label=False,
                    type="pil",
                    image_mode="RGB",
                    sources=["upload", "clipboard"],
                    interactive=True,
                    elem_classes="image-container",
                    elem_id="input-image"
                )
            
            # 右侧：输出结果
            with gr.Column(scale=1):
                with gr.Tabs() as output_tabs:
                    with gr.TabItem("GIF动画", id="gif_tab") as gif_tab:
                        gif_output = gr.Image(
                            show_label=False,
                            type="filepath",
                            show_download_button=True,
                            interactive=False,
                            elem_classes="image-container",
                            elem_id="gif-output"
                        )
                    
                    with gr.TabItem("MP4动画", id="mp4_tab") as mp4_tab:
                        video_output = gr.Video(
                            show_label=False,
                            autoplay=True,
                            interactive=False,
                            elem_classes="video-container",
                            elem_id="video-output"
                        )

        # 2. 控制组件
        with gr.Row(equal_height=True):
            # 动画效果选择
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("**动画效果**")
                    effect_type_dropdown = gr.Dropdown(
                        label="效果类型",
                        choices=list(all_effects_grouped.keys()),
                        value="出现效果",
                        interactive=True
                    )
                    # 根据默认选择的效果类型，初始化具体效果的下拉列表
                    effect_dropdown = gr.Dropdown(
                        label="具体效果",
                        choices=appear_effects,  # 默认显示与效果类型匹配的选项
                        value=appear_effects[0],
                        interactive=True,
                        elem_id="effect_dropdown",
                        allow_custom_value=True
                    )

            # 输出设置
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("**输出设置**")
                    output_fmt = gr.Radio(
                        label="格式", choices=["GIF", "MP4"], value="GIF"
                    )
                    duration = gr.Slider(
                        minimum=0.5, maximum=5.0, value=1.0, step=0.1, 
                        label="持续时间（秒）"
                    )
                    fps = gr.Slider(
                        minimum=10, maximum=60, value=20, step=1, 
                        label="帧率（FPS）"
                    )
        
        # 3. 生成按钮 - 作为最终操作
        btn = gr.Button("生成动画", variant="primary", size="lg")

        # --- 事件处理逻辑 ---
        def update_effect_choices(effect_type):
            choices = all_effects_grouped[effect_type]
            return gr.update(choices=choices, value=choices[0])

        effect_type_dropdown.change(
            fn=update_effect_choices,
            inputs=effect_type_dropdown,
            outputs=effect_dropdown
        )

        def switch_tab(fmt):
            return gr.update(selected="gif_tab" if fmt == "GIF" else "mp4_tab")

        output_fmt.change(fn=switch_tab, inputs=output_fmt, outputs=output_tabs)
        
        btn.click(
            fn=interface_fn, 
            inputs=[inp_img, effect_dropdown, output_fmt, duration, fps], 
            outputs=[gif_output, video_output]
        ).then(fn=switch_tab, inputs=output_fmt, outputs=output_tabs)

        # --- 示例 ---
        if os.path.exists("examples"):
            import random
            example_images = [os.path.join("examples", f) for f in os.listdir("examples") if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            all_effects = appear_effects + disappear_effects + emphasis_effects

            def find_effect_type(effect_name):
                for type_name, effects in all_effects_grouped.items():
                    if effect_name in effects:
                        return type_name
                return list(all_effects_grouped.keys())[0]

            example_data = []
            for img_path in example_images:
                random_effect = random.choice(all_effects)
                effect_type = find_effect_type(random_effect)
                random_fmt = random.choice(["GIF", "MP4"])
                random_duration = round(random.uniform(0.5, 5.0), 1)
                random_fps = random.randint(10, 60)
                example_data.append([img_path, effect_type, random_effect, random_fmt, random_duration, random_fps])
            
            def example_fn(img, effect_type, effect, fmt, dur, frame_rate):
                gif_result, video_result = interface_fn(img, effect, fmt, dur, frame_rate)
                tab_update = switch_tab(fmt)
                # 当点击示例时，不仅要更新具体效果的值，还要更新它的选项列表
                effect_dropdown_update = gr.update(choices=all_effects_grouped[effect_type], value=effect)
                # 返回所有输出，以更新UI控件
                return gif_result, video_result, tab_update, effect_type, effect_dropdown_update, fmt, dur, frame_rate
            
            gr.Examples(
                examples=example_data,
                inputs=[inp_img, effect_type_dropdown, effect_dropdown, output_fmt, duration, fps],
                outputs=[
                    gif_output, video_output, output_tabs, 
                    effect_type_dropdown, effect_dropdown, 
                    output_fmt, duration, fps
                ],
                fn=example_fn,
                cache_examples=False  # 禁用示例缓存，避免因版本更新导致警告
            )
            
    return demo


def main():
    # 禁用 Gradio 的分析数据收集，避免网络问题导致的错误
    os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'
    demo = build_interface()
    demo.launch()


if __name__ == "__main__":
    main()