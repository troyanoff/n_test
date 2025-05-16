import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from api.v1 import (
    buildings, companies
)
from core.config import settings as st

print(st)


app = FastAPI(
    title=st.project_name,
    description='Секретная разработка секретных служб.',
    docs_url='/api/docs',
    openapi_url='/api/docs.json',
    default_response_class=ORJSONResponse,
    version='1.0.0',
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    auth_header = request.headers.get('Authorization')
    path = request.url.path
    if (path in st.unprotected_urls
            or (auth_header and auth_header == st.api_token)):
        return response
    return ORJSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Authorization is required'},
    )

app.include_router(
    companies.router,
    prefix='/api/v1/companies',
    tags=['Companies']
)

app.include_router(
    buildings.router,
    prefix='/api/v1/buildings',
    tags=['Buildings']
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=7557,
        reload=True,
        workers=4
    )
