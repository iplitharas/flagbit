import pytest

from src.services.flagship import FlagShipService, FlagAllowedUpdates
from src.exceptions import FlagNotFoundException
from uuid import UUID


def test_user_can_add_a_new_flag():
    """
    Given a `flag` name and some initial `boolean` value
    When I call the `create_flag` method from `FlagShipService`
    Then I'm expected a new `Flag` instance to be return
         with the right arguments.
    """

    # Given
    flagship = FlagShipService()
    flag_name = "my first flag"
    value = False

    # When
    expected_flag = flagship.create_flag(name=flag_name, value=value)

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


@pytest.mark.parametrize(
    "updated_field_name,updated_field_value",
    [
        pytest.param("desc", "my updated desc", id="Flag description can be updated"),
        pytest.param("name", "my updated name", id="Flag name can be updated"),
        pytest.param("value", True, id="Flag value can be updated"),
    ],
)
def test_user_can_update_an_existing_flag_by_its_flag_id_and_the_new_fields(
    updated_field_name, updated_field_value
):
    """
    Given an existing `Flag` and some new fields to update
    When I call the `update_flag` method from `FlagShipService`
    Then I'm expecting the `Flag` to be updated with the new value
    """
    # Given
    flagship = FlagShipService()
    existing_flag = flagship.create_flag("my flag", value=True)

    updated_data = {updated_field_name: updated_field_value}
    updated_fields = FlagAllowedUpdates(**updated_data)

    # When
    updated_flag = flagship.update_flag(
        flag_id=str(existing_flag.id), updated_fields=updated_fields
    )

    # Then
    assert (
        getattr(updated_flag, updated_field_name) == updated_field_value
    ), f"Flag: `{updated_field_name}` should be updated"


def test_user_cannot_update_flag_that_does_not_exist():
    """
    Given a non-existing `Flag`
    When I call the `update_flag` method from `FlagShipService`
    Then I'm expecting a `ValueError` to be raised
    """
    # Given
    flagship = FlagShipService()
    updated_fields = FlagAllowedUpdates(name="new name")

    # When / Then
    with pytest.raises(FlagNotFoundException):
        flagship.update_flag(
            flag_id="non-existing-flag-id", updated_fields=updated_fields
        )


def test_user_can_see_all_flags():
    """
    Given some `Flags`
    When I call the `list` method from `FlagShipService`
    Then I'm expecting an Iterable of flags
    """
    # Given
    flagship = FlagShipService()
    flagship.create_flag("first flag", value=True)
    flagship.create_flag("second flag", value=False)

    # When
    flags_iter = flagship.get_all_flags()

    # Then
    flags = list(flags_iter)
    assert len(flags) == 2, "We should have only two flags"
