from fastapi import Depends, Request

from src.repo.doc_store import DocStoreRepo
from src.services.flagbit import FlagBitService


def get_doc_store_repo(request: Request) -> DocStoreRepo:
    return DocStoreRepo(client=request.app.state.mongo_client)


def get_flag_bit_service(
    repo: DocStoreRepo = Depends(get_doc_store_repo),  # noqa: B008
) -> FlagBitService:
    return FlagBitService(repo=repo)
