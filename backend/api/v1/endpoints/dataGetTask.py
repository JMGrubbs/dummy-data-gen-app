from db.dependencies import get_session
from fastapi import APIRouter, Depends, status
from schemas.dataGetTask import PackageFormat
from services.dataGenTask import load_data_gen_task
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(path="/create", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def data_generator(
    task: PackageFormat,
    db_session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    await load_data_gen_task(task, db_session)
    return {"status": "ok"}
