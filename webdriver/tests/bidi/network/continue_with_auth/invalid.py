import asyncio
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
        await bidi_session.network.continue_with_auth(request=request,
                                                      action="cancel")


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_action_invalid_type(bidi_session, setup_network_test,
                                          url, fetch, wait_for_event,
                                          add_intercept, value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(request=request,
                                                      action=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_action_invalid_value(bidi_session, setup_network_test,
                                           url, fetch, wait_for_event,
                                           add_intercept, value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(request=request,
                                                      action=value)


@pytest.mark.parametrize("value", [
    {
        "password": "foo"
    },
    {
        "username": "foo"
    },
    {},
    None,
],
                         ids=[
                             "missing username",
                             "missing password",
                             "missing username and password",
                             "missing credentials",
                         ])
async def test_params_action_provideCredentials_invalid_credentials(
        bidi_session, setup_network_test, url, fetch, wait_for_event,
        add_intercept, value):
    request = await setup_blocked_request_test(setup_network_test, url,
                                               add_intercept, fetch,
                                               wait_for_event)

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.continue_with_auth(
            request=request, action="provideCredentials", credentials=value)


async def setup_blocked_request_test(setup_network_test, url, add_intercept,
                                     fetch, wait_for_event):
    await setup_network_test(events=["network.authRequired"])

    text_url = url(PAGE_EMPTY_TEXT)
    await add_intercept(
        phases=["authRequired"],
        url_patterns=[{
            "type": "string",
            "pattern": text_url,
        }],
    )

    asyncio.ensure_future(fetch(text_url))
    event = await wait_for_event("network.authRequired")
    request = event["request"]["request"]

    return request
