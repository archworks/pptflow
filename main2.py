from pptflow.utils import mylogger
import time
logger = mylogger.get_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting pptflow...")
    from pptflow.gui.ppt2video_flow2 import PPTFlowApp
    start_time = time.time()  # record start time
    app = PPTFlowApp()
    end_time = time.time()  # record end time
    logger.info(f"Application started. Startup time: {end_time - start_time:.2f} seconds.")
    app.mainloop()
