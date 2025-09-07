import datetime

from src.flag import Flag


def test_user_can_create_a_flag_with_a_name():
    """
    Given a `flag name` as string
    When I initialize a `Flag` with this name
    Then I'm expecting a `Flag` instance with the `date_created` field
        auto populated to the  current utc time.
    """
    # Given
    flag_name = "my_first_flag"
    # When
    flag = Flag(name=flag_name)
    # Then
    assert flag.name == flag_name, "Something went very wrong!"
    assert isinstance(flag.date_created, datetime.datetime)
