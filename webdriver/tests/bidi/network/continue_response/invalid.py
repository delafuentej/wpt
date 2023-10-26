import asyncio
import pytest
import webdriver.bidi.error as error

pytestmark = pytest.mark.asyncio

PAGE_EMPTY_TEXT = "/webdriver/tests/bidi/network/support/empty.txt"


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_request_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_request_invalid_value(bidi_session, value):
    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.continue_response(request=value)


async def test_params_request_no_such_request(bidi_session, setup_network_test,
                                              wait_for_event, fetch, url):
    await setup_network_test(events=[
        "network.responseCompleted",
    ])
    on_response_completed = wait_for_event("network.responseCompleted")

    text_url = url(PAGE_EMPTY_TEXT)
    await fetch(text_url)

    response_completed_event = await on_response_completed
    request = response_completed_event["request"]["request"]

    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.continue_response(request=request)


@pytest.mark.parametrize("value", [False, 42, {}, []])
async def test_params_reason_phrase_invalid_type(bidi_session,
                                                 setup_network_test, url,
                                                 fetch, wait_for_event,
                                                 add_intercept, value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     reason_phrase=value)


@pytest.mark.parametrize("value", [False, "s", {}, []])
async def test_params_status_code_invalid_type(bidi_session,
                                               setup_network_test, url, fetch,
                                               wait_for_event, add_intercept,
                                               value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     status_code=value)


@pytest.mark.parametrize("value", [-1, 4.3])
async def test_params_status_code_invalid_value(bidi_session,
                                                setup_network_test, url, fetch,
                                                wait_for_event, add_intercept,
                                                value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_response(request=request,
                                                     status_code=value)


# TODO: Add cookies.
# TODO: Add credentials.
# TODO: Add headers.


async def setup_blocked_request_test(setup_network_test, url, add_intercept,
                                     fetch, wait_for_event):
    await setup_network_test(events=["network.responseStarted"])

    text_url = url(PAGE_EMPTY_TEXT)
    await add_intercept(
        phases=["responseStarted"],
        url_patterns=[{
            "type": "string",
            "pattern": text_url,
        }],
    )

    asyncio.ensure_future(fetch(text_url))
    event = await wait_for_event("network.beforeRequestSent")
    request = event["request"]["request"]

    return request
