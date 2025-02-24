# Author: Valley-e
# Date: 2025/2/23  
# Description:
import asyncio
import os
from typing import Optional
from aip import AipSpeech
from pptflow.tts.tts_service import TtsService
from pptflow.config.setting import Setting
from pptflow.utils import mylogger


class BaiduTtsService(TtsService):
    def __init__(self):
        self.logger = mylogger.get_logger(__name__)
        self.logger.info("Using Baidu TTS")
        # 参数合法性校验配置
        # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
        # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
        self._valid_params = {
            'per': {0, 1, 3, 4, 5, 103, 106, 110, 111},  # 合法发音人ID
            'vol': lambda x: 0 <= x <= 15,  # 音量范围校验
            'spd': lambda x: 0 <= x <= 15,  # 语速范围校验
            'pit': lambda x: 0 <= x <= 15  # 音调范围校验
        }

    async def tts(
            self,
            text: str,
            output_audio_filename: str,
            setting: Optional[Setting] = None
    ) -> Optional[str]:
        """
        优化的单次语音合成方法

        :param text: 待合成文本（长度需<=1024字节）
        :param output_audio_filename: 音频输出文件路径
        :param setting: 合成参数配置字典，包含：
            - per: 发音人ID
            - vol: 音量(0-15)
            - spd: 语速(0-15)
            - pit: 音调(0-15)
        :return: 合成音频文件路径（失败返回None）
        """
        appid = setting.baidu_app_id if setting.baidu_app_id else os.environ.get('BAIDU_APP_ID')
        api_key = setting.baidu_api_key if setting.baidu_api_key else os.environ.get('BAIDU_API_KEY')
        secret_key = setting.baidu_secret_key if setting.baidu_secret_key else os.environ.get('BAIDU_SECRET_KEY')
        self.client = AipSpeech(appid, api_key, secret_key)
        try:
            # 输入校验
            if not self._validate_input(text, setting):
                return None

            # 异步执行同步API调用
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.client.synthesis(
                    text,
                    'zh',
                    1,  # 固定参数
                    self._build_tts_params(setting)
                )
            )

            # 结果处理
            if isinstance(result, dict):
                self.logger.error(f"API错误: {result}", extra={"logid": result.get('tts_logid')})
                return None

            return await self._save_audio(result, output_audio_filename)

        except Exception as e:
            self.logger.error(f"合成流程异常: {str(e)}", exc_info=True)
            return None

    def _validate_input(self, text: str, setting: Setting) -> bool:
        """综合参数校验"""
        # 增加空对象判断
        if not setting:
            self.logger.error("配置参数不能为空")
            return False
        # 文本长度校验（百度API限制为1024字节）
        if len(text.encode('utf-8')) > 1024:
            self.logger.error(f"文本过长: {len(text)}字节 (最大1024)")
            return False

        # 发音人参数校验
        if setting.per not in self._valid_params['per']:
            self.logger.error(f"无效发音人ID: {setting.per}")
            return False

        # 动态参数校验
        for param in ['vol', 'spd', 'pit']:
            value = getattr(setting, param, None)
            if value is not None and not self._valid_params[param](value):
                self.logger.error(f"参数{param}值越界: {value}")
                return False

        return True

    def _build_tts_params(self, setting) -> dict:
        """构建合成参数，设置默认值"""
        return {
            'vol': getattr(setting, 'vol', 5),
            'per': getattr(setting, 'per', 0),
            'spd': getattr(setting, 'spd', 5),
            'pit': getattr(setting, 'pit', 5)
        }

    async def _save_audio(self, data: bytes, path: str):
        """异步保存音频文件"""
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._sync_save, data, path)
            self.logger.info(f"音频文件已保存: {path}")
        except IOError as e:
            self.logger.error(f"文件保存失败: {str(e)}")

    def _sync_save(self, data: bytes, path: str):
        """同步文件保存方法"""
        with open(path, 'wb') as f:
            f.write(data)

    def get_voice_list(self, setting: Setting = None):
        return []
