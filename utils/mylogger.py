# Author: Valley-e
# Date: 2024/11/5  
# Description: Make sure that all modules log their information into a single log file.
import logging
from logging.handlers import RotatingFileHandler
import os

# debug: 级别10，用于开发者调试，显示变量等详细信息; 正常版本不应包含
# info: 级别20，通知用户关键的正常行为，如“主库添加成功”;用简单、明确的语言记录
# warning:级别30，不正常或偏离预期的行为; 不会立即影响系统，但具有潜在风险
# error: 级别40，无法修复的严重错误；必须立即处理并可能需要停止程序
# critical:级别50，未知的不正常行为，超出已知容错；可能会影响程序未来运行
# 获取上一级目录
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'log')

# 创建 log 文件夹（如果不存在）
os.makedirs(log_dir, exist_ok=True)

# 设置日志文件的路径
LOG_FILE = os.path.join(log_dir, 'app.log')
MAX_BYTES = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 3  # 保留3个备份文件


# 配置日志格式和级别
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # 设置日志级别，只会输出大于等于该级别的日志
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # 也可以输出到控制台
            RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)  # 日志轮转
        ]
    )


# 你可以定义一个函数用来获取logger
def get_logger(name):
    return logging.getLogger(name)


# 在模块导入时进行日志配置
setup_logging()

