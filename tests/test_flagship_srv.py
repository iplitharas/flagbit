from src.services.flagship import FlagShipService
from uuid import UUID


def test_user_can_add_a_new_flag():
    """
    Given a `flag` name and some initial `boolean` value
    When I call the `add` method from `FlagShipService`
    Then I'm expected a new `Flag` instance to be return
         with the right arguments.
    """

    # Given
    flagship = FlagShipService()
    flag_name = "my first flag"
    value = False

    # When
    expected_flag = flagship.add(name=flag_name, value=value)

    # Then
    assert (
        expected_flag.name == flag_name
    ), "Store flag name should be the same as the input"
    assert (
        expected_flag.value == value
    ), "Store flag value should  be the same as the input"
    assert isinstance(
        expected_flag.id, UUID
    ), "Each flash should be associated with one uuid"


def test_user_can_see_all_flags():
    """
    Given some `Flags`
    When I call the `list` method from `FlagShipService`
    Then I'm expecting an Iterable of flags
    """
    # Given
    flagship = FlagShipService()
    flagship.add("first flag", value=True)
    flagship.add("second flag", value=False)
    # When
    flags_iter = flagship.list()
    # Then
    flags = list(flags_iter)
    assert len(flags) == 2, "We should have only two flags"
