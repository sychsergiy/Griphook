from typing import Union

from pydantic import BaseModel, validator

from griphook.server.settings.constants import EXC_LENGTH_TITLE_NOT_VALID


class UpdateProjectTeamModel(BaseModel):
    id: int = None
    title: str = None

    @validator("title")
    def check_title_length(cls, value):
        if 0 == len(value) or len(value) > 20:
            raise ValueError(EXC_LENGTH_TITLE_NOT_VALID.format(value))
        return value


class UpdateServerClusterModel(BaseModel):
    id: int
    cpu_price: Union[float, int, None] = None
    memory_price: Union[float, int, None] = None


class AttachDetachProjectTeamModel(BaseModel):
    project_id: int = None
    team_id: int = None
    services_group_id: int
