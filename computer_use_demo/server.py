import asyncio
import multiprocessing
import uvicorn
import subprocess
import sys
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_streamlit():
    try:
        logger.info("Starting Streamlit server...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.join(os.path.dirname(__file__), "streamlit.py")])
    except Exception as e:
        logger.error(f"Error starting Streamlit: {str(e)}", exc_info=True)

def run_fastapi():
    try:
        logger.info("Starting FastAPI server...")
        uvicorn.run(
            "computer_use_demo.streamlit:app",
            host="0.0.0.0",
            port=8000,
            log_config={
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    }
                },
                "handlers": {
                    "default": {
                        "formatter": "default",
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stderr"
                    },
                    "file": {
                        "formatter": "default",
                        "class": "logging.FileHandler",
                        "filename": "/tmp/fastapi.log"
                    }
                },
                "loggers": {
                    "": {"handlers": ["default", "file"], "level": "INFO"}
                }
            },
            reload=False,
            workers=1,
            timeout_keep_alive=120
        )
    except Exception as e:
        logger.error(f"Error starting FastAPI: {str(e)}", exc_info=True)

async def main():
    logger.info("Starting server processes...")
    
    # Start Streamlit in a separate process
    streamlit_process = multiprocessing.Process(target=run_streamlit)
    streamlit_process.start()
    logger.info(f"Streamlit process started with PID {streamlit_process.pid}")
    
    # Start FastAPI in the main process
    fastapi_process = multiprocessing.Process(target=run_fastapi)
    fastapi_process.start()
    logger.info(f"FastAPI process started with PID {fastapi_process.pid}")
    
    try:
        # Keep the main process running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down servers...")
        streamlit_process.terminate()
        fastapi_process.terminate()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        streamlit_process.terminate()
        fastapi_process.terminate()

if __name__ == "__main__":
    try:
        logger.info("Starting main server...")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True) 