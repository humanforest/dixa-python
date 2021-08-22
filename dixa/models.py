from datetime import datetime
from typing import List
import pandas as pd

from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)
from pydantic import (
    BaseModel,
    constr,
    validator,
    Field,
    validate_email
)
from pydantic.color import Color

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class User(BaseModel):
    """A class used to represent a user or agent."""

    user_id: str = Field(default=None, alias="id")
    # avatar_url: HttpUrl = Field(default=None, alias="avatarUrl")
    created_at: datetime = Field(default=None, alias="createdAt")
    display_name: str = Field(default=None, alias="displayName")
    given_name: constr(max_length=63, strip_whitespace=True) = Field(default=None, alias="givenName")
    family_name: constr(max_length=63, strip_whitespace=True) = Field(default=None, alias="familyName")
    middle_names: List[str] = Field(default=None, alias="middleNames")
    email: str = Field(default=None, alias="email")
    phone_number: constr(max_length=50, strip_whitespace=True) = Field(default=None, alias="phoneNumber")
    is_agent: bool = False

    @validator("middle_names")
    def has_middle_names(cls, v):
        return v if v else None

    @validator("email")
    def check_email(cls, v):
        if v is None:
            return v
        return validate_email(v)[1]

    @validator("phone_number")
    def check_phone_number(cls, v):
        if v is None:
            return v

        try:
            n = parse_phone_number(v, "GB")  # Defaulting to GB
        except NumberParseException as e:
            raise ValueError("Please provide a valid mobile phone number") from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError("Please provide a valid mobile phone number")

        return format_number(n, PhoneNumberFormat.E164)

    def payload(self, exclude_id: bool = False) -> dict:
        excluded_fields = {"created_at", "avatar_url", "is_agent"}
        if exclude_id:
            excluded_fields.update({"user_id"})
        return self.dict(by_alias=True, exclude_unset=True, exclude=excluded_fields)

    def dataframe(self):
        return pd.DataFrame([self.dict()])


class UserList(BaseModel):
    """A class used to represent a list of users or agents."""

    user_list: List[User] = Field(default=None, alias="data")
    next_page_key: str = Field(default=None)
    previous_page_key: str = Field(default=None)

    def payload(self, exclude_id: bool = False) -> dict:
        excluded_fields = {"created_at", "avatar_url", "is_agent"}
        if exclude_id:
            excluded_fields.update({"user_id"})
        return self.dict(by_alias=True,
                         exclude_unset=True,
                         exclude_none=True,
                         exclude={
                             "user_list": {"__all__": excluded_fields},
                             "next_page_key": ...,
                             "previous_page_key": ...
                         })

    def dataframe(self):
        return pd.DataFrame.from_dict(self.dict().get("user_list"))


class Tag(BaseModel):
    """A class used to represent a tag."""

    tag_id: str = Field(default=None, alias="id")
    name: str = Field(alias="name")
    state: str = Field(default=None, alias="state")
    color: Color = Field(alias="color")

    def payload(self) -> dict:
        payload = self.dict(by_alias=True, exclude_unset=True, exclude={"id", "state"})
        payload["color"] = payload["color"].as_hex()
        return payload

    def dataframe(self):
        return pd.DataFrame([self.dict()])


class TagList(BaseModel):
    """A class used to represent a list of tags."""

    tag_list: List[Tag] = Field(default=None, alias="data")

    def dataframe(self):
        return pd.DataFrame.from_dict(self.dict().get("tag_list"))


class Team(BaseModel):
    """A class used to represent a team."""

    team_id: str = Field(default=None, alias="id")
    name: str = Field(default=None, alias="name")

    def payload(self) -> dict:
        return self.dict(by_alias=True, exclude_unset=True, exclude={"team_id"})

    def dataframe(self):
        return pd.DataFrame([self.dict()])


class TeamList(BaseModel):
    """A class used to represent a list of teams."""

    team_list: List[Team] = Field(default=None, alias="data")

    def dataframe(self):
        return pd.DataFrame.from_dict(self.dict().get("team_list"))


class Presence(BaseModel):
    """A class used to represent the presence of agents."""

    user_id: str = Field(default=None, alias="userId")
    request_time: datetime = Field(default=None, alias="requestTime")
    last_seen: datetime = Field(default=None, alias="lastSeen")
    presence_status: str = Field(default=None, alias="presenceStatus")
    connection_status: str = Field(default=None, alias="connectionStatus")
    active_channels: List[str] = Field(default=None, alias="activeChannels")

    def dataframe(self):
        return pd.DataFrame([self.dict()])


class PresenceList(BaseModel):
    """A class used to represent a list of agents' presence."""

    presence_list: List[Presence] = Field(default=None, alias="data")

    def dataframe(self):
        return pd.DataFrame.from_dict(self.dict().get("presence_list"))
