from fastapi import APIRouter
from pydantic import BaseModel

from app.service.debug_request import TranslatorOutput, CodeInfo, handle_debug_request

router = APIRouter()


class DebugRequest(BaseModel):
    post_code: str


class DebugResponse(BaseModel):
    uuid: str
    translator_output: TranslatorOutput
    code_info: CodeInfo


@router.post("/api/v1/debug-request", response_model=DebugResponse)
async def request_debug(request: DebugRequest) -> DebugResponse:
    uuid, translator_output, code_info = await handle_debug_request(request.post_code)
    return DebugResponse(uuid=str(uuid), translator_output=translator_output, code_info=code_info)
