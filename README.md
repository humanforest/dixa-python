# Python Dixa SDK

A Python implementation of the Dixa API.

## Installation

Install the package with pip

```bash
pip install dixa
```

## Usage/Examples

### Initialization
```python
from dixa import DixaClient

client = DixaClient(api_key="<DIXA_API_KEY>")
```

### Getting user data
```python
# Get users by id, email or phone
user_by_id = client.get_end_users(user_id="abcd1234")
user_by_email = client.get_end_users(email="john.doe@example.com")
user_by_phone = client.get_end_users(phone_number="+447357000000")

# Get all users
all_users = client.get_all_end_users()
```

### Upload bulk user data
```python
from dixa import User, UserList

user1 = {
    "displayName": "John Doe",
    "email": "john.doe@example.com",
    "middleNames": ["Bob", "Patrick"]
}

user2 = {
    "givenName": "Juan",
    "familyName": "Perez",
    "displayName": "Juan Perez",
    "phoneNumber": "+447777000000"
}

users = UserList(
    data=[
        User(**user1),
        User(**user2)
    ]
)

client.post_end_users_bulk(user_list=users)
```

### Create a Team
```python
from dixa import Team

client.post_team(team=Team(name="New Team"))
```

## Features

- Get users and agents by id, email or phone.
- Upload, patch and modify users and agents.
- Bulk upload of users.
- Get agents' presence.
- Activate and deactivate tags.


## Ported Endpoints

### Agents

- [x] `GET /v1/agents/presence`
- [x] `GET /v1/agents/{agent_id}/teams`
- [x] `GET /v1/agents/{agent_id}/presence`
- [x] `POST /v1/agents/bulk`
- [x] `GET /v1/agents`
- [ ] `PUT /v1/agents`
- [ ] `POST /v1/agents`
- [ ] `PATCH /v1/agents`
- [x] `GET /v1/agents/{agent_id}`
- [ ] `PUT /v1/agents/{agent_id}`
- [ ] `POST /v1/agents/{agent_id}`
- [ ] `PATCH /v1/agents/{agent_id}`

### End Users

- [x] `POST /v1/endusers/bulk`
- [x] `GET /v1/endusers/{user_id}`
- [x] `PATCH /v1/endusers/{user_id}`
- [x] `GET /v1/endusers`
- [x] `PUT /v1/endusers`
- [x] `POST /v1/endusers`
- [x] `PATCH /v1/endusers`
- [x] `PUT /v1/endusers/{enduser_id}`

### Teams
- [x] `GET /v1/teams`
- [x] `POST /v1/teams`
- [x] `GET /v1/teams/{teamId}/agents`
- [x] `GET /v1/teams/{teamId}/presence`
- [x] `GET /v1/teams/{team_id}`
- [x] `DELETE /v1/teams/{team_id}`
- [ ] `DELETE /v1/teams/{team_id}/agents`
- [ ] `PATCH /v1/teams/{team_id}/agents`

### Conversations
- [ ] `PUT /v1/conversations/{conversationId}/close`
- [ ] `PUT /v1/conversations/{conversationId}/reopen`
- [ ] `PUT /v1/conversations/{conversationId}/transfer/queue`
- [ ] `POST /v1/conversations/{conversationId}/notes/bulk`
- [ ] `POST /v1/conversations/{conversationId}/notes`
- [ ] `GET /v1/conversations/{csid}/rating`
- [ ] `PUT /v1/conversations/{conversationId}/tags/{tagId}`
- [ ] `DELETE /v1/conversations/{conversationId}/tags/{tagId}`
- [ ] `GET /v1/conversations/{csid}/tags`
- [ ] `POST /v1/conversations/{conversationId}/messages`
- [ ] `POST /v1/conversations`
- [ ] `PUT /v1/conversations/{conversationId}/claim`
- [ ] `GET /v1/conversations/{csid}`
- [ ] `GET /v1/conversations/{csid}/activitylog`
- [ ] `GET /v1/conversations/activitylog`

### Queues
- [ ] `GET /v1/queues/{queue_id}/members`
- [ ] `DELETE /v1/queues/{queueId}/members`
- [ ] `PATCH /v1/queues/{queueId}/members`
- [ ] `GET /v1/queues`
- [ ] `POST /v1/queues`
- [ ] `GET /v1/queues/{queue_id}`

### Tags
- [x] `GET /v1/tags/{tagId}`
- [x] `GET /v1/tags`
- [ ] `POST /v1/tags`
- [x] `PATCH/v1/tags/{tagId}/deactivate`
- [x] `PATCH /v1/tags/{tagId}/activate`


## Reference
[REST API Reference](https://docs.dixa.io/reference/)