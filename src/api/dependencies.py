from src.services.flagship import FlagShipService

flash_ship = FlagShipService()


def get_flagship_service() -> FlagShipService:
    return flash_ship
