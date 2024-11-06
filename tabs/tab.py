from typing import Union


class Tab():
    save: bool
    base_url: str
    endpoint: str


    def __init__(
        self, 
        save: Union[bool, None], 
        base_url: Union[str, None],
        endpoint: str
    ):
        self.save = save if save is not None else False
        self.base_url = 'http://127.0.0.1:8000' if base_url is None else base_url
        self.endpoint = endpoint