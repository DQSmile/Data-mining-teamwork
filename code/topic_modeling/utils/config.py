import os

# 日志等级
LOG_LEVEL = 'DEBUG'

# 路径
__proj_dir = os.path.dirname(os.path.dirname(__file__))
__data_dir = os.path.join(__proj_dir, 'data')

RAW_DATA_DIR = os.path.join(__data_dir, 'raw_data')
PROCESSED_DATA_DIR = os.path.join(__data_dir, 'processed_data')
MODEL_DIR = os.path.join(__data_dir, 'model')
RESULT_DIR = os.path.join(__data_dir, 'result')

if __name__ == '__main__':
    print(RAW_DATA_DIR)
    print(PROCESSED_DATA_DIR)
    print(MODEL_DIR)
    print(RESULT_DIR)
