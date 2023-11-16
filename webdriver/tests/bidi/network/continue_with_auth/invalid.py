import pytest
import webdriver.bidi.error as error

pytestmark = pytest.mark.asyncio

PAGE_EMPTY_TEXT = "/webdriver/tests/bidi/network/support/empty.txt"


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_request_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(request=value,
                                                      action="cancel")


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_request_invalid_value(bidi_session, value):
    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.continue_with_auth(request=value,
                                                      action="cancel")


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_action_invalid_type(setup_blocked_request, bidi_session, value):
    request = await setup_blocked_request("authRequired")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(request=request,
                                                      action=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_action_invalid_value(setup_blocked_request, bidi_session, value):
    request = await setup_blocked_request("authRequired")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(request=request,
                                                      action=value)


@pytest.mark.parametrize("value", [
    {
        "type": "password",
        "password": "foo"
    },
    {
        "type": "password",
        "username": "foo"
    },
    {
        "type": "password",
    },
    {
        "username": "foo",
        "password": "bar",
    },
    None,
],
                         ids=[
                             "missing username",
                             "missing password",
                             "missing username and password",
                             "missing type",
                             "missing credentials",
                         ])
async def test_params_action_provideCredentials_invalid_credentials(setup_blocked_request, bidi_session, value):
    request = await setup_blocked_request("authRequired")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(
            request=request, action="provideCredentials", credentials=value)
