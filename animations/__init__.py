"""
动画效果模块
包含各种图像动画效果的实现
动画效果分为三类：图像出现、图像消失和图像强调
"""

# 图像出现效果
from .appear import fade_in, slide_in_from_left, slide_in_from_top

# 图像消失效果
from .disappear import fade_out, slide_out_to_right, slide_out_to_bottom

# 图像强调效果
from .emphasis import pulse, shake, bounce

# 动画效果映射表，按类别分组
EFFECTS = {
    # 图像出现类
    "淡入出现": fade_in,
    "从左滑入": slide_in_from_left,
    "从上滑入": slide_in_from_top,
    
    # 图像消失类
    "淡出消失": fade_out,
    "向右滑出": slide_out_to_right,
    "向下滑出": slide_out_to_bottom,
    
    # 图像强调类
    "脉冲效果": pulse,
    "左右摇晃": shake,
    "上下弹跳": bounce,
}
