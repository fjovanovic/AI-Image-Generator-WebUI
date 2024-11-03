from typing import Union


class Tab():
    save: bool
    api_url: str
    endpoint: str


    def __init__(
        self, 
        save: Union[bool, None], 
        api_url: Union[str, None],
        endpoint: str
    ):
        self.save = save
        self.api_url = 'http://127.0.0.1:8000' if api_url is None else api_url
        self.endpoint = endpoint