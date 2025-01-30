from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.openapi.docs import (
    get_swagger_ui_html,
     get_swagger_ui_oauth2_redirect_html,
     get_redoc_html
     )
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    keys = await redis.keys("*cache*")
    for key in keys:
        await redis.delete(key)

def register_static_docs_routes(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        if app.openapi_url is None or app.swagger_ui_oauth2_redirect_url is None:
            raise ValueError("OpenAPI URL and OAuth2 redirect URL must not be None")

        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url or "/oauth2-redirect", include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        if app.openapi_url is None:
            raise ValueError("OpenAPI URL must not be None")

        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )


def create_app(
    create_custom_static_urls: bool = False
) -> FastAPI:
    app = FastAPI(
        docs_url = None if create_custom_static_urls else "/docs",
        redoc_url = None if create_custom_static_urls else "/redoc",
        root_path="/api",
        root_path_in_servers=False,
        lifespan=lifespan
    )
    if create_custom_static_urls:
        register_static_docs_routes(app)
    return app