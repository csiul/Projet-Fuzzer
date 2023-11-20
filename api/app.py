"""
API permettant d'utiliser WPGarlic.
"""

from fastapi import FastAPI

from routers import api_status, fuzz_plugin, wordpress

# Create FastAPI
app = FastAPI(debug=True, title="Projet Fuzzer - WPGarlic API", docs_url=None)

# Register routers
app.include_router(api_status.router)
app.include_router(fuzz_plugin.router)
app.include_router(wordpress.router)
