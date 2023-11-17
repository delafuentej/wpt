// META: timeout=long
// META: script=/resources/test-only-api.js
// META: script=resources/pressure-helpers.js
// META: global=window,dedicatedworker,sharedworker

'use strict';

pressure_test(async (t, mockPressureService) => {
  const sampleRateInHz = 25;
  let gotPenalty = false;
  const readings = ['nominal', 'fair', 'serious', 'critical'];
  // Normative values for rate obfuscation parameters.
  // https://w3c.github.io/compute-pressure/#rate-obfuscation-normative-parameters.
  const minPenaltyTimeInMs = 5000;
  const maxChangesThreshold = 100;
  const minChangesThreshold = 50;
  const changes = await new Promise(async resolve => {
    const observerChanges = [];
    const observer = new PressureObserver(changes => {
      let lastSample;
      if (observerChanges.length > 0) {
        lastSample = observerChanges[(observerChanges.length) - 1][0].time;
        if (((changes[0].time - lastSample) >= minPenaltyTimeInMs) &&
            observerChanges.length >= minChangesThreshold) {
          gotPenalty = true;
          resolve(observerChanges);
        }
      }
      observerChanges.push(changes);
    }, {sampleRate: sampleRateInHz});

    observer.observe('cpu');
    mockPressureService.startPlatformCollector(sampleRateInHz);
    let i = 0;
    // mockPressureService.updatesDelivered() does not necessarily match
    // pressureChanges.length, as system load and browser optimizations can
    // cause the actual timer used by mockPressureService to deliver readings
    // to be a bit slower or faster than requested.
    while (observerChanges.length <= maxChangesThreshold) {
      mockPressureService.setPressureUpdate(
          'cpu', readings[i++ % readings.length]);
      await t.step_wait(
          () => mockPressureService.updatesDelivered() >= i,
          `At least ${i} readings have been delivered`);
      if (gotPenalty == true) {
        break;
      }
    }
    observer.disconnect();
    assert_true(gotPenalty);
  });
}, 'Rate obfuscation mitigation should have been triggered, when changes is higher than minimum changes before penalty');
