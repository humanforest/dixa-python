"""A Python module for interacting and consuming responses from Dixa."""
from typing import Optional, Union
from typing_extensions import Literal

from pydantic import Field
from requests import Response

from . import errors as e
from .base_client import BaseClient
from .models import User, UserList, TagList, Tag, Team, TeamList, Presence, PresenceList
from .utils import _next_cursor_is_present, _get_params, _previous_cursor_is_present


class DixaClient(BaseClient):
    base_url: str = Field(default="https://dev.dixa.io")

    def get_end_users(self,
                      *,
                      user_id: Optional[str] = None,
                      page_limit: Optional[int] = None,
                      page_key: Optional[str] = None,
                      email: Optional[str] = None,
                      phone_number: Optional[str] = None) -> Union[User, UserList]:
        """Return End Users.

        Args:
            user_id: (optional) The End User id.
            page_limit: (optional) Maximum number of results per page. May be used in combination with pageKey to
                change the number of results in between page requests.
            page_key: (optional) Base64 encoded form of pagination query parameters.
            email: (optional) The email of the End User.
            phone_number: (optional) The phone of the End User.

        Returns:
            User or UserList
        """
        return self._get_users("endusers",
                               user_id=user_id,
                               email=email,
                               phone_number=phone_number,
                               page_limit=page_limit,
                               page_key=page_key)

    def get_all_end_users(self, *, page_limit: Optional[int] = None) -> UserList:
        """List all End Users recursively.

        Args:
            page_limit: (optional) Maximum number of results per page.

        Returns:
            UserList
        """
        return self._get_all_users("endusers", page_limit=page_limit)

    def post_end_user(self, *, user: User) -> User:
        """Create a User in Dixa.

        Args:
            user: User object.

        Returns:
            Same User object created with the response data.
        """
        response = self.api_call("endusers", "POST", user.payload())
        return User(**response)

    def post_end_users_bulk(self, *, user_list: UserList) -> dict:
        """Create Users in Dixa via bulk upload.

        Args:
            user_list: UserList object.

        Returns:
            BulkAction data (dict).
        """
        return self.api_call("endusers/bulk", "POST", user_list.payload())

    def put_end_user(self,
                     *,
                     user_id: Optional[str] = None,
                     user_data: Optional[dict] = None,
                     user: Optional[User] = None,
                     user_list: Optional[UserList] = None) -> dict:
        """Update a User or UserList.

        Args:
            user_id: (optional) The User id to update.
            user_data: (optional) The data used to update the user data.
            user: (optional) User object.
            user_list: (optional) UserList object.

        Returns:
            dict
        """
        return self._edit_users("PUT", user_id=user_id, user_data=user_data, user=user, user_list=user_list)

    def patch_end_user(self,
                       *,
                       user_id: Optional[str] = None,
                       user_data: Optional[dict] = None,
                       user: Optional[User] = None,
                       user_list: Optional[UserList] = None) -> dict:
        """Update a User or UserList.

        Args:
            user_id: (optional) The User id to patch.
            user_data: (optional) The data used to patch the user data.
            user: (optional) User object.
            user_list: (optional) UserList object.

        Returns:
            dict
        """
        return self._edit_users("PATCH", user_id=user_id, user_data=user_data, user=user, user_list=user_list)

    def get_agents(self,
                   *,
                   agent_id: Optional[str] = None,
                   page_limit: Optional[int] = None,
                   page_key: Optional[str] = None) -> Union[User, UserList]:
        """Return Agents.

        Args:
            agent_id: (optional) The Agent id.
            page_limit: (optional) Maximum number of results per page. May be used in combination with pageKey to
                change the number of results in between page requests.
            page_key: (optional) Base64 encoded form of pagination query parameters.

        Returns:
            User or UserList
        """
        return self._get_users("agents", user_id=agent_id, page_limit=page_limit, page_key=page_key)

    def get_all_agents(self, *, page_limit: Optional[int] = None) -> UserList:
        """List all Agents recursively.

        Args:
            page_limit: (optional) Maximum number of results per page.

        Returns:
            UserList
        """
        return self._get_all_users("agents", page_limit=page_limit)

    def get_agents_presence(self, *, agent_id: Optional[str] = None) -> Union[Presence, PresenceList]:
        """List the Presence of one or all Agents.

        Args:
            agent_id: (optional) The Agent id.

        Returns:
            Presence or PresenceList
        """
        if agent_id is not None:
            return Presence(**self.api_call(f"agents/{agent_id}/presence"))
        return PresenceList(data=[Presence(**presence)
                                  for presence
                                  in self.api_call("agents/presence", return_data=False).json()])

    def get_agent_teams(self, *, agent_id: str, return_team=False) -> Union[list, Team, TeamList]:
        """Returns the list of teams where the agent belongs.

                Args:
                    agent_id: The Agent id.
                    return_team: (optional) If True, return the Team or TeamList object.

                Returns:

                """
        response = self.api_call(f"agents/{agent_id}/teams")
        if return_team:
            if len(response) > 1:
                return TeamList(data=[self.get_teams(team_id=team.get("id")) for team in response])
            return self.get_teams(team_id=response[0].get("id"))
        return response

    def get_tags(self, *, tag_id: Optional[str] = None) -> Union[Tag, TagList]:
        """Return Tags.

        Args:
            tag_id: (optional) The Tag id.

        Returns:
            Tag or TagList
        """
        if tag_id is not None:
            return Tag(**self.api_call(f"tags/{tag_id}"))
        return TagList(data=[Tag(**tag) for tag in self.api_call("tags")])

    def patch_tag(self,
                  *,
                  action: Literal["activate", "deactivate"],
                  tag_id: Optional[str] = None,
                  tag: Optional[Tag] = None) -> Response:
        """Activate or deactivate a Tag.

        Args:
            action: Either "activate" or "deactivate".
            tag_id: (optional) The Tag id.
            tag: (optional) A Tag object with tag_id specified.

        Returns:
            dict
        """
        if tag_id is not None:
            _tag_id = tag_id
        elif tag is not None:
            if tag.tag_id is not None:
                _tag_id = tag.tag_id
            else:
                raise ValueError("Couldn't find tag_id in Tag object.")
        else:
            raise ValueError("Can't specify both tag_id and Tag object.")
        return self.api_call(f"tags/{_tag_id}/{action}", "PATCH", return_data=False)

    def get_teams(self, *, team_id: Optional[str] = None) -> Union[Team, TeamList]:
        """Return Tags.

        Args:
            team_id: (optional) The Team id.

        Returns:
            Team or TeamList
        """
        if team_id is not None:
            return Team(**self.api_call(f"teams/{team_id}"))
        return TeamList(data=[Team(**team) for team in self.api_call("teams")])

    def get_team_agents(self, *, team_id: str) -> UserList:
        """Return the list of agents that belong to a team.

        Args:
            team_id: The Team id.

        Returns:
            UserList
        """
        return UserList(data=[User(**user, is_agent=True) for user in self.api_call(f"teams/{team_id}/agents")])

    def get_team_presence(self, *, team_id: str) -> PresenceList:
        """Return the list of agents' presence belonging to a team.

        Args:
            team_id: The Team id.

        Returns:
            PresenceList
        """
        return PresenceList(data=[Presence(**presence) for presence in self.api_call(f"teams/{team_id}/presence")])

    def post_team(self, *, team: Team) -> Team:
        """Create a Team in Dixa.

        Args:
            team: Team object.

        Returns:
            Same Team object created with the response data.
        """
        response = self.api_call("teams", "POST", team.payload())
        return Team(**response)

    def delete_team(self,
                    *,
                    team_id: Optional[str] = None,
                    team: Optional[Team] = None) -> Response:
        """Deletes a team.

        Args:
            team_id: (optional) The Team id.
            team: (optional) A Team object with team_id specified.

        Returns:
            dict
        """
        if team_id is not None:
            _team_id = team_id
        elif team is not None:
            if team.team_id is not None:
                _team_id = team.team_id
            else:
                raise ValueError("Couldn't find tag_id in Team object.")
        else:
            raise ValueError("Can't specify both tag_id and Team object.")
        return self.api_call(f"teams/{_team_id}", "DELETE", return_data=False)

    def _get_users(self,
                   endpoint: Literal["agents", "endusers"],
                   user_id: Optional[str] = None,
                   email: Optional[str] = None,
                   phone_number: Optional[str] = None,
                   page_limit: Optional[int] = None,
                   page_key: Optional[str] = None,
                   **kwargs
                   ) -> Union[User, UserList]:
        """Base function to get a User or UserList."""
        if user_id is not None:
            return User(**self.api_call(f"{endpoint}/{user_id}"), is_agent=endpoint == "agents")
        if email is not None and phone_number is not None:
            raise e.DixaRequestError("The endpoint can take only one parameter. "
                                     "Please choose between email and phone number.")
        if email is not None or phone_number is not None:
            kwargs.update({"email": email})
            kwargs.update({"phone": phone_number})
            return User(**self.api_call(endpoint, params=kwargs)[0], is_agent=endpoint == "agents")
        if page_limit is not None:
            kwargs.update({"pageLimit": page_limit, "pageKey": page_key})

        response = self.api_call(endpoint, params=kwargs, return_data=False).json()
        next_page_key = None
        previous_page_key = None
        if _next_cursor_is_present(response) or _previous_cursor_is_present(response):
            next_page_key = response.get("meta", {}).get("next")
            previous_page_key = response.get("meta", {}).get("previous")
            if next_page_key is not None:
                next_page_key = _get_params(next_page_key).get("pageKey")[0]
            if previous_page_key is not None:
                previous_page_key = _get_params(previous_page_key).get("pageKey")[0]

        return UserList(
            data=[User(**user, is_agent=endpoint == "agents") for user in response.get("data")],
            next_page_key=next_page_key,
            previous_page_key=previous_page_key
        )

    def _get_all_users(self,
                       endpoint: Literal["agents", "endusers"],
                       data: Optional[list] = None,
                       page_limit: Optional[int] = None,
                       **kwargs) -> UserList:
        """Recursive function to get all elements using pagination cursor."""
        pagination = True
        if page_limit is not None:
            kwargs.update({"pageLimit": page_limit})
        if data is None:
            data = []
            pagination = False
        response = self.api_call(
            endpoint=endpoint,
            return_data=False,
            pagination=pagination,
            params=kwargs).json()
        data.extend(response.get("data"))
        if _next_cursor_is_present(response):
            next_path = response.get("meta", {}).get("next")
            if next_path is not None:
                self._get_all_users(next_path, data)
        return UserList(data=[User(**user, is_agent=endpoint == "agents") for user in data])

    def _edit_users(self,
                    method: Literal["PUT", "PATCH"],
                    user_id: Optional[str] = None,
                    user_data: Optional[dict] = None,
                    user: Optional[User] = None,
                    user_list: Optional[UserList] = None) -> dict:
        """Function to PATCH or PUT end user data."""
        if user_id is not None and user_data is not None:
            return self.api_call(f"endusers/{user_id}", method, json=user_data)
        if user is not None:
            return self.api_call(f"endusers/{user.user_id}", method, json=user.payload())
        if user_list is not None:
            return self.api_call("endusers", "PUT", json=user_list.payload())
        raise e.DixaRequestError("Missing arguments: user_id and data, user, or user_list are required.")
