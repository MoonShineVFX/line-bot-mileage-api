from dataclasses import dataclass


def create_mock_event(body: str):
    source = MockSource(
        type='user',
        user_id='user_id'
    )
    message = MockMessage(
        id='debug_id',
        text=body
    )
    return MockEvent(source=source, message=message)


@dataclass
class MockSource:
    type: str
    user_id: str
    group_id: str = None


@dataclass
class MockMessage:
    id: str
    text: str


@dataclass
class MockEvent:
    source: MockSource
    message: MockMessage
    reply_token: str = 'debug_reply_token'
