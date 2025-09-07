from src.services.flagship_srv import FlagShipService


def test_user_can_add_a_new_flag():
    """
    Given a `flag` name and some initial boolean value
    When I call the `add` method from `FlagShipService`
    Then I'm expected a new flag added.
    """

    # Given
    flag_ship = FlagShipService()
    flag_name_ = "my first flag"
    value = False
    # When
    assert flag_ship.add(name=flag_name_, value=value) == "ok"
    # Then
