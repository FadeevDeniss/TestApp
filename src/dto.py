import dataclasses


@dataclasses.dataclass(init=True, repr=True)
class RequestDto:

    """
    Class representing row received from server database
    contains id, telephone number, creation date and time

    """

    num_pressed: int | None
    telephone: str
    created_date: str | None
    created_time: str | None




