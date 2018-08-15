from pydantic import BaseModel, validator

from griphook.server.settings.constants import EXC_LENGTH_TITLE_NOT_VALID


class UpdateProjectTeamModel(BaseModel):
    id: int = None
    title: str = None

    @validator('title')
    def check_title_length(cls, value):
        if 0 == len(value) or len(value) > 20:
            raise ValueError(EXC_LENGTH_TITLE_NOT_VALID.format(value))
        return value
