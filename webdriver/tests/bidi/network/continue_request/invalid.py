import pytest
import webdriver.bidi.error as error

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_request_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_request(request=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_request_invalid_value(bidi_session, value):
    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.continue_request(request=value)


@pytest.mark.parametrize("value", [False, 42, {}, []])
async def test_params_method_invalid_type(setup_blocked_request, bidi_session,
                                          value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_request(request=request,
                                                    method=value)


@pytest.mark.parametrize("value", [False, 42, {}, []])
async def test_params_url_invalid_type(setup_blocked_request, bidi_session, value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_request(request=request, url=value)


@pytest.mark.parametrize("protocol", ["http", "https"])
@pytest.mark.parametrize("value", [":invalid", "#invalid"])
async def test_params_url_invalid_value(setup_blocked_request, bidi_session, protocol, value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_request(
            request=request, url=f"{protocol}://{value}")


# TODO: Add body.
# TODO: Add cookies.
# TODO: Add headers.
