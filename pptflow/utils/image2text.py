# Author: Valley-e
# Date: 2025/3/18  
# Description:
import os
import random
from pathlib import Path
import logging
from docx import Document
from openai import OpenAI
import base64
import re
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api.lingyiwanwu.com/v1"
API_KEY = os.getenv("LINGYI_API_KEY")
SCENE_PROFILES = {
    "technical": {  # 技术方案场景
        "prompt": (
            "基于{theme}生成技术方案演讲，听众为{audience}\n"
        ),
        "default_style": "专业严谨",
    },
    "marketing": {  # 营销场景
        "prompt": (
            "为{theme}产品生成营销演讲，目标听众：{audience}\n"
        ),
        "default_style": "生动有趣",
    },
    "leadership": {  # 领导致辞
        "prompt": (
            "生成{theme}主题的领导致辞，听众：{audience}\n"
        ),
        "default_style": "鼓舞人心",
    },
    "education": {  # 教学场景
        "prompt": (
            "生成{theme}教学演讲，听众：{audience}\n"
        ),
        "default_style": "亲切自然",
    },
    # 原有leadership和education场景添加同理
    "product_launch": {  # 新增产品发布场景
        "prompt": (
            "为{theme}产品发布会生成演讲稿，听众：{audience}\n"
        ),
        "default_style": "激情澎湃",
    },
    "academic": {  # 新增学术报告场景
        "prompt": (
            "生成{theme}学术报告，听众：{audience}\n"
        ),
        "default_style": "严谨客观",
    }
}


def build_prompt(theme: str, audience: str, duration_seconds: int,
                 scene: str, image_number: int, total_pages: int, style: str = None,
                 context: str = "") -> str:
    """智能提示词生成"""
    profile = SCENE_PROFILES.get(scene, {
        "prompt": (
            f"生成{theme}主题的通用演讲稿，听众：{audience}\n"  # 保持变量占位符统一格式
        ),
        "default_style": "正式",
    })

    # base_prompt = (
    #     profile["prompt"].format(
    #         theme=theme,
    #         audience=audience,
    #     )
    # )
    core_prompt = f"""
    #角色设定
    你是一位专业的视频脚本架构师，擅长将PPT内容转化为自然流畅的解说词。请基于以下要求，将{total_pages}页图片生成PPT演示文稿，每次只生成当前页的内容，目前是第{image_number}页。
    🎯 主题：{theme}
    🎯 观众：{audience}等
    🎯 核心要求：
        1. 时长管理策略：
           - 总时长为{duration_seconds}
           - 每页演讲时长建议（秒）：{duration_seconds}/{total_pages}+调整系数（0.8-1.2）
        2. 内容生成规则：
           - 语言风格保持{style or profile['default_style']}
           - 必须直接切入当前页图片内容相关的核心信息
           - 文稿需结合当前图片中的文字内容
        3. 页面定位策略（请严格遵守）：
           ⚠️仅当当前是第1页时：仿照PPT演示文稿，需要**完整**的开场白（问候语+主题介绍），不需要分析图片元素
           ⚠️仅当当前是第{total_pages}页时：需要鸣谢、总结和升华
           ⚠️中间页（2-{total_pages - 1}页）：直接开始生成当前页的内容，将类似“大家好”等开场白换成衔接词
        4. 输出内容（!强制要求）：
           - 内容开头为”第{image_number}页：“
           - 内容只包含文稿内容，不要包含输出提示词、要求等额外内容
    """

    return core_prompt


def process_slide(
        image: dict,
        total_pages: int,
        api_key: str,
        theme: str,  # 必填
        audience: str,  # 必填
        duration: str,  # 必填
        scene: str = "generic",  # 可选场景
        style: str = None,  # 可选覆盖风格
        context: str = ""  # 可选上下文
) -> tuple[str, str]:
    """极简参数版本"""
    # 参数校验
    if not all([theme, audience, duration]):
        raise ValueError("缺少必要参数：theme/audience/duration")

    duration_seconds = duration_to_seconds(duration)

    # 生成智能提示词
    prompt = build_prompt(
        theme=theme,
        audience=audience,
        duration_seconds=duration_seconds,
        scene=scene,
        image_number=image["number"],
        total_pages=total_pages,
        style=style,
        context=context
    )

    # 替换原有的单图编码逻辑
    path = image["path"]
    if not Path(path).exists():
        raise FileNotFoundError(f"图片文件 {path} 不存在")
    try:
        with open(path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"图片处理失败: {str(e)}")
        raise

    # 构建请求
    client = OpenAI(api_key=api_key, base_url=API_BASE)

    # 流式请求
    try:
        stream = client.chat.completions.create(
            model="yi-vision-v2",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }],
            stream=True,
            temperature=0.7 if image["number"] == 1 else 0.3,  # 控制创造性
            max_tokens=2000,  # 控制输出长度
            top_p=0.9,  # 控制多样性
        )

        reasoning, answer = [], []
        is_answering = False

        for chunk in stream:
            # 处理usage信息
            if not chunk.choices:
                print("\n" + "=" * 20 + "Token 使用情况" + "=" * 20)
                print(chunk.usage)
                continue

            delta = chunk.choices[0].delta

            # 处理空内容情况
            if not getattr(delta, 'reasoning_content', None) and not getattr(delta, 'content', None):
                continue

            # 处理开始回答的情况
            if not getattr(delta, 'reasoning_content', None) and not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True

            # 处理思考过程
            if getattr(delta, 'reasoning_content', None):
                print(delta.reasoning_content, end='', flush=True)
                reasoning.append(delta.reasoning_content)
            # 处理回复内容
            elif getattr(delta, 'content', None):
                print(delta.content, end='', flush=True)
                answer.append(delta.content)
        return ''.join(reasoning), ''.join(answer)

    except Exception as e:
        logging.error(f"API请求失败: {str(e)}")
        raise


def process_all_slides(
        image_dir: str,
        api_key: str,
        theme: str,  # 必填
        audience: str,  # 必填
        duration: str,  # 必填
        scene: str = "generic",  # 可选场景
        style: str = None,  # 可选覆盖风格
        filename_prefix: str = "",  # 可选文件名前缀
):
    full_text = []
    context = ""
    image_list = process_image_dir(image_dir, filename_prefix=filename_prefix)

    for image in image_list:
        print(f"\n正在处理第{image['number']}页：{image['path']}")

        _, batch_text = process_slide(
            image=image,
            total_pages=len(image_list),
            api_key=api_key,
            theme=theme,
            audience=audience,
            duration=duration,
            scene=scene,
            style=style,
            context=context,  # 注入增强后的上下文
        )

        # 内容校验（新增）
        if f"第{image['number']}页：" not in batch_text:
            logging.warning(f"第{image['number']}页缺失页码标记，已自动补充")
            batch_text = f"第{image['number']}页：{batch_text}"

        # 提取并处理内容
        summary = extract_context(batch_text)
        clean_text = re.sub(r"【摘要】.+", "", batch_text, flags=re.DOTALL)
        full_text.append(clean_text)

        # 更新上下文
        context = f"{context}\n{summary}" if context else summary
        context = "\n".join(context.split("\n")[-1:])  # 保留最近两个摘要

    return "\n".join(full_text)


def extract_context(text: str) -> str:
    """从响应文本提取摘要"""
    # 匹配【摘要】标记内容
    import re
    match = re.search(r"【摘要】(.+?)(?=\n\d+\.|$)", text, re.DOTALL)
    return match.group(1).strip() if match else ""


def process_image_dir(img_dir, filename_prefix):
    """处理图片目录"""
    # 使用正则表达式严格匹配文件名格式
    pattern = re.compile(
        r"^{prefix}-P(\d+)\.(?:png|jpg|jpeg)$".format(
            prefix=re.escape(filename_prefix)  # 转义特殊字符
        ),
        re.IGNORECASE  # 忽略大小写
    )

    images = []
    for fname in os.listdir(img_dir):
        match = pattern.match(fname)
        if match:
            images.append({
                'path': os.path.join(img_dir, fname),
                'number': int(match.group(1)),  # 提取页码
            })

    # 按页码排序并验证连续性
    images.sort(key=lambda x: x['number'])
    validate_page_continuity(images, filename_prefix)
    if not images:
        raise ValueError(f"No images found in {img_dir}")
    print(f"Found {len(images)} image files")

    return images


def validate_page_continuity(images, prefix):
    """验证页码连续性"""
    expected = 1
    for img in images:
        if img['number'] != expected:
            raise ValueError(
                f"Missing page {expected} for {prefix}. "
                f"Found page {img['number']} instead."
            )
        expected += 1


def duration_to_seconds(duration_str: str) -> int:
    """
    将时间字符串转换为秒数
    支持格式示例：
    - "20分钟" → 1200
    - "1.5小时" → 5400
    - "2小时30分钟" → 9000
    - "90秒" → 90
    """
    # 使用正则表达式匹配时间单位
    pattern = r'(\d+\.?\d*)\s*([小时钟头分秒]+)'
    matches = re.findall(pattern, duration_str)

    if not matches:
        raise ValueError(f"无效的时间格式: {duration_str}")

    total_seconds = 0
    for value, unit in matches:
        num = float(value)
        if '小时' in unit or '钟头' in unit:
            total_seconds += num * 3600
        elif '分' in unit:
            total_seconds += num * 60
        elif '秒' in unit:
            total_seconds += num

    return int(total_seconds)


# 使用示例
if __name__ == "__main__":
    image_dir = "C:/Users/19622/AppData/Roaming/pptflow/temp/image"
    # filename_prefix = "《坏情绪也没关系》于曈"  # 文件名前缀
    filename_prefix = "国科恒泰内幕信息培训演示文稿"  # 文件名前缀
    output_file = f"{filename_prefix}.docx"  # 输出文件名
    images = process_image_dir(image_dir, filename_prefix)
    for img in images:
        print(f"{img['number']}: {img['path']}")
    try:
        text = process_all_slides(
            image_dir=image_dir,
            api_key=API_KEY,
            theme="内幕交易查处处于持续高压态势",
            audience="企业公司领导和员工",
            duration="30分钟",
            scene="internal training",
            filename_prefix=filename_prefix
        )
        # text = process_all_slides(
        #     image_dir=image_dir,
        #     api_key=API_KEY,
        #     theme="PPT转视频产品介绍",
        #     audience="老师、营销人员",
        #     duration="3分钟",
        #     scene="product_launch",
        #     filename_prefix=filename_prefix
        # )
        print("\n最终回复：")
        print(text)
        # 删除空白行并保存到Word
        cleaned_text = re.sub(r'\n\s*\n', '\n', text)  # 删除空白行
        doc = Document()
        for line in cleaned_text.split('\n'):
            if line.strip():  # 忽略空行
                doc.add_paragraph(line.strip())
        doc.save(output_file)
        print(f"\n✅ 结果已保存至：{output_file}")
    except Exception as e:
        logging.error(f"处理失败: {str(e)}", exc_info=True)
