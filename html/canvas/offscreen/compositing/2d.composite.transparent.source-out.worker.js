// DO NOT EDIT! This test has been generated by /html/canvas/tools/gentest.py.
// OffscreenCanvas test in a worker:2d.composite.transparent.source-out
// Description:
// Note:

importScripts("/resources/testharness.js");
importScripts("/html/canvas/resources/canvas-tests.js");

var t = async_test("");
var t_pass = t.done.bind(t);
var t_fail = t.step_func(function(reason) {
    throw reason;
});
t.step(function() {

var canvas = new OffscreenCanvas(100, 50);
var ctx = canvas.getContext('2d');


ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
ctx.fillRect(0, 0, 100, 50);
ctx.globalCompositeOperation = 'source-out';
ctx.fillStyle = 'rgba(0, 0, 255, 0.75)';
ctx.fillRect(0, 0, 100, 50);
_assertPixelApprox(canvas, 50,25, 0,0,255,96, "50,25", "0,0,255,96", 5);
t.done();

});
done();