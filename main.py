from utils import mylogger
import time
logger = mylogger.get_logger(__name__)
import os
import sys

def log_environment():
    with open("env_log1.txt", "w") as f:
        f.write(f"Executable: {sys.executable}\n")
        f.write(f"Sys Path: {sys.path}\n")
        f.write(f"Environment Variables: {os.environ}\n")

log_environment()


if __name__ == "__main__":
    logger.info("Starting pptflow...")
    from frames.main_frame import App
    start_time = time.time()  # record start time
    app = App()
    end_time = time.time()  # record end time
    logger.info(f"Application started. Startup time: {end_time - start_time:.2f} seconds.")
    app.mainloop()
