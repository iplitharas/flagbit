from fastapi import Depends, Request

from src.services.flagship import FlagShipService
from src.repo.doc_store import DocStoreRepo


def get_doc_store_repo(request: Request) -> DocStoreRepo:
    return DocStoreRepo(client=request.app.state.mongo_client)


def get_flagship_service(
    repo: DocStoreRepo = Depends(get_doc_store_repo),
) -> FlagShipService:
    return FlagShipService(repo=repo)
