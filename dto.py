import dataclasses
from json import dumps


@dataclasses.dataclass
class RequestDto:

    num_pressed: int | None
    telephone: str
    created_date: str | None
    created_time: str | None

    def __init__(
            self,
            num_pressed: int | None,
            telephone: str,
            created_date: str | None,
            created_time: str | None
    ):

        self.num_pressed = num_pressed
        self.telephone = telephone
        self.created_date = created_date
        self.created_time = created_time

    def __repr__(self) -> str:
        return f'{type(self)}: {self.__dict__.values()}'

    @property
    def __dict__(self) -> dict:
        return dataclasses.asdict(self)



