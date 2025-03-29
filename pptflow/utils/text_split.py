# Author: Valley-e
# Date: 2025/3/30  
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


class TextSplit(DeepSeekClient):
    """文本切割处理器"""
    def split(self, text: str, setting: Setting) -> list:
        """
        执行文本切割
        :param text: 任意字的输入文本
        :param setting: 个性化配置
        :return: 分割为结构化字幕列表
        """
        if len(text) < 20:
            raise ValueError("输入文本过短（至少20字符）")

        prompt = self._build_prompt(text)
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
            return self._post_process(result_list, text, setting)
        except (SyntaxError, ValueError) as e:
            logger.error(f"格式解析失败: {e}\n原始响应: {response}")
            raise ValueError("响应格式不符合要求，请尝试重新生成")

    def _post_process(self, subtitles: list, origin_text: str, setting: Setting) -> list:
        """后处理优化"""
        # 1. 长度校验
        total_length = sum(len(s) for s in subtitles)
        if abs(total_length - len(origin_text)) / len(origin_text) > 0.3:
            logger.warning(f"字幕总长度差异超过30%: {total_length} vs {len(origin_text)}")

        # 2. 短句合并（避免单字字幕）
        merged = []
        buffer = ""
        for s in subtitles:
            if len(buffer + s) <= setting.subtitle_length * 1.5:  # 允许1.5倍长度
                buffer += s
            else:
                if buffer:
                    merged.append(buffer)
                buffer = s
        if buffer:
            merged.append(buffer)

        # 3. 标点修正
        return [self._fix_punctuation(s) for s in merged]

    def _fix_punctuation(self, text: str) -> str:
        """确保首尾标点规范"""
        # 去除首部标点
        while text and text[0] in {'，', ',', '、'}:
            text = text[1:]
        # 确保尾部有标点
        if text and text[-1] not in {'，', '；', '。', '!', '?', ',', ';', '.', '！', '？'}:
            text += '。' if any('\u4e00' <= c <= '\u9fff' for c in text) else '.'
        return text

    def _build_prompt(self, text: str) -> str:
        """构建视频字幕专用提示词"""
        return f"""【视频字幕分割规范】
        📽️ 原始素材：{text}
        🎯 语言控制规则：
        1. 严格保持与原始素材相同的语言体系
        2. 字幕必须使用原始语言创作，禁止翻译
        3. 混合语言场景需用方括号标注（例：[专业术语]）
        🎯 高级语义分割策略：
        1. 语义完整性：
           - 保持主谓宾完整（禁止在主语和谓语之间分割）
           - 保留逻辑关联词（但是、因此、同时等）
           - 同一语义单元不可分割（例："虽然...但是..."需保持完整）
        
        2. 呼吸停顿优化：
           - 中文在自然换气点分割（逗号、顿号后）
           - 英文在从句衔接处分割（that, which引导的从句前）
        
        3. 视觉同步原则：
           - 长数字（超过15位）单独成段
           - 引号内容保持完整（"..."不可分割）
           - 对话内容单独分割（张三说："..."）
        
        4. 多语言混合处理：
           - 中英混杂时优先保持语法正确性
           - 专业术语保留原文（例："Python编程"不翻译）
        5. 技术规范：
           - ❗ 必须严格使用数组格式返回（即使只有1条字幕），禁止包含任何解释性文字
           - ❗ 示例错误格式："这是优化后的字幕：['内容']" 
           - ❗ 正确格式：['第一句内容','第二句内容']
           - 禁用Markdown格式和特殊符号（&、*等）
    """


class OutputManager:
    """输出结果管理器"""

    @staticmethod
    def save(subtitles: list):
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs_{datetime.now():%Y%m%d_%H%M%S}.txt"

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


def main():
    """主交互流程"""
    setting = Setting()
    setting.subtitle_length = 20
    try:
        spliter = TextSplit()
        text = "今天我们将共同探讨一个至关重要的主题——内幕交易查处处于持续高压态势。作为企业的一员，我们每个人都有责任维护市场的公平和透明，共同构建诚信的商业环境。内幕交易不仅损害了投资者的利益，还破坏了市场的正常秩序。我们将通过一系列培训，深入了解内幕交易的危害，掌握防范和打击内幕交易的策略。希望通过今天的学习，大家能够更好地识别和避免内幕交易行为，共同维护我们的职业道德和企业声誉。谢谢大家！ "
        subtitles = spliter.split(text, setting)
        OutputManager.display(subtitles)
        OutputManager.save(subtitles)
    except Exception as e:
        logger.info(f"\n❌ 操作失败：{str(e)}", exc_info=True)
        print("💡 建议：请检查输入格式或联系技术支持")


if __name__ == "__main__":
    main()
