import subprocess
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(debug=True)

app.wpgarlic_process = None


@app.get("/status")
async def get_status():
    wpgarlic = Path('wpgarlic').is_dir()
    return {
        'wpgarlic_present': wpgarlic
    }


@app.post('/fuzz_plugin/{plugin_name}')
def fuzz(plugin_name: str):
    if app.wpgarlic_process is None:
        app.wpgarlic_process = subprocess.Popen(['python', 'fuzz_plugin.py', plugin_name], cwd='./wpgarlic/')
    else:
        return "Already fuzzing, go away..."
    return
