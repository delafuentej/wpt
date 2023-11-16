import pytest
import webdriver.bidi.error as error

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_request_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_request_invalid_value(bidi_session, value):
    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.continue_response(request=value)


@pytest.mark.parametrize("value", [False, 42, {}, []])
async def test_params_reason_phrase_invalid_type(setup_blocked_request, bidi_session,
                                                 value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     reason_phrase=value)


@pytest.mark.parametrize("value", [False, "foo", {}, []])
async def test_params_status_code_invalid_type(setup_blocked_request, bidi_session,
                                               value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     status_code=value)


@pytest.mark.parametrize("value", [-1, 4.3, 600])
async def test_params_status_code_invalid_value(setup_blocked_request, bidi_session,
                                                value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     status_code=value)


# TODO: Add cookies.
# TODO: Add credentials.
# TODO: Add headers.
