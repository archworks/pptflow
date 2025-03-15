# Author: Valley-e
# Date: 2025/3/15  
# Description:
from openai import OpenAI
import os
import re
import ast
from dotenv import load_dotenv
from datetime import datetime
from pptflow.config.setting import Setting
from pptflow.utils import mylogger
logger = mylogger.get_logger(__name__)

# 初始化配置
load_dotenv()
# 可配置参数（放在类常量中）
MIN_ENGLISH_RATIO = 0.9  # 英文判定阈值
CHINESE_RANGE = ('\u4e00', '\u9fff')  # 中文Unicode范围


class DeepSeekClient:
    """LLM 交互基类"""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LKEAP_API_KEY"),
            base_url="https://api.lkeap.cloud.tencent.com/v1"
        )

    def _process_stream(self, stream, callback=None):
        """通用流式响应处理器"""
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
                # print(delta.reasoning_content, end='', flush=True)
                reasoning.append(delta.reasoning_content)
            # 处理回复内容
            elif getattr(delta, 'content', None):
                print(delta.content, end='', flush=True)
                answer.append(delta.content)
        return ''.join(reasoning), ''.join(answer)


class TextRefiner(DeepSeekClient):
    """文本润色处理器"""
    STYLE_MAP = {
        "video_script": "视频脚本风格（短句，口语化）",
        "storytelling": "故事叙述风格（感官描写）",
        "academic": "学术风格（数据引用）",
        "formal": "正式风格（专业术语）",
        "casual": "休闲风格（日常话术）",
        "poetic": "诗情画意风格（verse）",
        "humor": "幽默风格（ Sarcasm）",
        "presentation": "演讲风格（段落间有空行）",
    }

    def refine(self, text: str, setting: Setting) -> list:
        """
        执行文本润色
        :param text: 50-500字的输入文本
        :param setting: 个性化配置
        :return: 结构化字幕列表
        """
        if len(text) < 20:
            raise ValueError("输入文本过短（至少20字符）")

        prompt = self._build_prompt(text, setting)
        stream = self.client.chat.completions.create(
            model="deepseek-r1",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        _, response = self._process_stream(stream)
        cleaned_str = response.strip().replace('\n', '')  # 清理换行
        array_pattern = r'\[.*?\]'  # 匹配最外层的中括号内容
        matches = re.findall(array_pattern, cleaned_str, re.DOTALL)

        if not matches:
            raise ValueError("未检测到有效数组格式")

        # 选择最后一个匹配项（防止大模型多次输出）
        final_match = matches[-1]

        # 安全转换
        try:
            result_list = ast.literal_eval(final_match)
            if not isinstance(result_list, list):
                raise TypeError("返回结果不是列表类型")
            # 新增过滤逻辑
            result_list = [s for s in result_list if s.strip()]  # 过滤空字符串元素
            if not result_list:  # 增加空列表检查
                raise ValueError("有效内容为空")
            return result_list
        except (SyntaxError, ValueError) as e:
            logger.error(f"格式解析失败: {e}\n原始响应: {response}")
            raise ValueError("响应格式不符合要求，请尝试重新生成")

    def _build_prompt(self, text: str, setting: Setting) -> str:
        """构建视频字幕专用提示词"""
        # 自动检测输入语言
        has_chinese = any(CHINESE_RANGE[0] <= c <= CHINESE_RANGE[1] for c in text)
        english_alpha_count = sum('a' <= c.lower() <= 'z' for c in text)
        english_ratio = english_alpha_count / len(text) if text else 0
        input_lang = '中文' if has_chinese and english_ratio < MIN_ENGLISH_RATIO else '英文'

        return f"""【视频字幕生成规范】
    📽️ 原始素材：（{input_lang}）:{text}

    🎯 语言控制规则：
    1. 严格保持与原始素材相同的语言体系
    2. {input_lang}字幕必须使用原始语言创作，禁止翻译
    3. 混合语言场景需用方括号标注（例：[专业术语]）

    🎯 核心要求：
    1. 风格适配：采用{self.STYLE_MAP.get(setting.subtitle_style, '标准')}风格，注意口语化表达（例如：将"因此"改为"所以"，"立即"改为"马上"）
    2. 节奏控制：
       {self._build_lang_specific_rules(input_lang, setting.subtitle_length)}
    3. 视觉适配：
       ■ 避免专业术语（如必须出现需用括号解释）
       ■ 数字信息口语化（如"68%"改为"超过六成"）
       ■ 保留关键修饰词（"非常"、"特别"等强调词）
    4. 技术规范：
       - ❗ 必须严格使用数组格式返回（即使只有1条字幕），禁止包含任何解释性文字
       - ❗ 示例错误格式："这是优化后的字幕：['内容']" 
       - ❗ 正确格式：['第一句内容','第二句内容']
       - 禁用Markdown格式和特殊符号（&、*等）
       - 保留必要标点（？！）但避免连续使用

    🔄 处理流程：
    1. 语义分析 → 识别核心信息
    2. 节奏调整 → 按呼吸节奏分割
    3. 视觉优化 → 添加衔接词
    4. 格式校验 → 确保符合技术规范

    📐 格式示例：
    {self._build_lang_example(input_lang)}
    """

    def _build_lang_specific_rules(self, lang: str, max_words: int = 12) -> str:
        """构建语言特定规则"""
        rules = {
            '中文': [
                f"▶ 每行12-{max_words}个汉字（3-4秒显示时长）",
                "▶ 使用中文标点（，。！）",
                "▶ 长句在连词前分割（而、且、但）",
                "▶ 句子中有分点或分步骤论述时，可以使用（首先，然后，最后）或者序数词（一、二、三）或者阿拉伯数字（1. 2. 3.）",
                "▶ 相邻字幕保持语义连贯（使用'不过'、'另外'等过渡词）"
            ],
            '英文': [
                f"▶ 每行8-{max_words}个单词（3-4秒显示时长）",
                "▶ 使用英文标点（, . !）",
                "▶ 长句在连词前分割（and, but, or）",
                "▶ 在介词前断句（in, on, with）",
                "▶ 保持首字母大写",
                "▶ 避免使用缩写（e.g., 'etc.'）",
                "▶ 句子中有分点或分步骤论述时，可以使用Firstly, Foremost或者阿拉伯数字（1. 2. 3.）",
                "▶ 相邻字幕保持语义连贯（使用'However'、'Moreover' 等过渡词）"
            ]
        }
        return "\n".join(rules.get(lang, []))

    def _build_lang_example(self, lang: str) -> str:
        """构建语言特定示例"""
        examples = {
            '中文': (
                "原始文本：气候变化影响显著\n"
                "优化结果：['最新研究显示，全球变暖导致极端天气频发，', '科学家呼吁各国立即采取减排措施。']"
            ),
            '英文': (
                "Original: PPTFlow is an open-source desktop app\n"
                "Result: ['PPTFlow revolutionizes content creation', "
                "'as a cross-platform desktop solution', "
                "'supporting offline video production.']"
            )
        }
        return examples.get(lang, "")


class OutputManager:
    """输出结果管理器"""

    @staticmethod
    def save(subtitles: list, style: str):
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs/{style}_{datetime.now():%Y%m%d_%H%M%S}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            index = 1
            for subtitle in subtitles:
                f.write(subtitle + "\n")
                index += 1
        print(f"\n✅ 结果已保存至：{filename}")

    @staticmethod
    def display(subtitles: list):
        print("\n" + "=" * 20 + "最终字幕" + "=" * 20)
        index = 1
        for subtitle in subtitles:
            print(f"{index}. {subtitle}")
            index += 1


def get_polishing_text(text: str, setting: Setting) -> list:
    try:
        refiner = TextRefiner()
        subtitles = refiner.refine(text, setting)
        return subtitles
    except Exception as e:
        logger.info(f"\n❌ 润色失败：{str(e)}", exc_info=True)
        return []


def main():
    """主交互流程"""
    setting = Setting()
    try:
        refiner = TextRefiner()

        text = input("\n请输入待润色文本：").strip()
        style = input(f"选择风格（{'/'.join(refiner.STYLE_MAP.keys())}）：").strip()

        if style not in TextRefiner.STYLE_MAP:
            print("⚠️ 无效风格，已使用默认风格")
            style = "presentation"
        setting.subtitle_style = style
        subtitles = refiner.refine(text, setting)
        OutputManager.display(subtitles)
        OutputManager.save(subtitles, style)
    except Exception as e:
        logger.info(f"\n❌ 操作失败：{str(e)}", exc_info=True)
        print("💡 建议：请检查输入格式或联系技术支持")


if __name__ == "__main__":
    main()
