import uvicorn

import run

if __name__ == "__main__":
    app = run.create_app("development")
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
