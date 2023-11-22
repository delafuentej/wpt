/**
 * Create a new promise that resolves when the window receives
 * the MessagePort and starts it.
 *
 * @param {Window} window - The window to wait for the MessagePort.
 * @returns {Promise<MessagePort>} A promise you should await to ensure the
 *     window
 * receives the MessagePort.
 */
function expectMessagePortFromWindow(window) {
  return new Promise(resolve => {
    window.onmessage = e => {
      assert_true(e.ports[0] instanceof window.MessagePort);
      e.ports[0].start();
      resolve(e.ports[0]);
    };
  });
}
