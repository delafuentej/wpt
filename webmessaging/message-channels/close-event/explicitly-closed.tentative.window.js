// META: title=Close event test when an entangled port is explicitly closed.
// META: script=/common/dispatcher/dispatcher.js
// META: script=/common/get-host-info.sub.js
// META: script=/common/utils.js
// META: script=/html/browsers/browsing-the-web/remote-context-helper/resources/remote-context-helper.js
// META: script=resources/helper.js

async_test(t => {
  const channel = new MessageChannel();
  channel.port1.start();
  channel.port2.start();
  channel.port2.onclose = t.step_func_done();
  channel.port1.close();
}, 'Close event on port2 is fired when port1 is explicitly closed');

async_test(t => {
  const channel = new MessageChannel();
  channel.port1.start();
  channel.port2.start();
  channel.port1.onclose =
      t.unreached_func('Should not fire a close event on port1');
  channel.port1.close();
  setTimeout(t.step_func_done(), 100);
}, 'Close event on port1 is not fired when port1 is explicitly closed');

promise_test(async t => {
  const waitForPort = expectMessagePortFromWindow(window);
  const helper = new RemoteContextHelper();
  const rc1 = await helper.addWindow();

  await rc1.executeScript(() => {
    const {port1, port2} = new MessageChannel();
    window.port = port1;
    window.opener.postMessage({}, '*', [port2]);
  });
  const port = await waitForPort;
  const closeEventPromise = new Promise(resolve => port.onclose = resolve);
  rc1.executeScript(() => window.port.close());
  await closeEventPromise;
}, 'Close event on port1 is fired when port2, which is in a different window, is explicitly closed.')
