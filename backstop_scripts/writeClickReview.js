module.exports = function(casper, scenario, vp) {

  // write a comment link click
  casper.then(function () {
    this.click('.activate-write a');
  });

  // fill in comment box in prosemirror form
  casper.evaluate(function () {
    $('.ProseMirror-content p').html('<span pm-offset="0" pm-leaf="4">test</span>');
  });

  // save comment
  casper.then(function () {
    this.click('.comment-submission');
  });

  // review and submit
  casper.then(function () {
    this.click('.comment-index-review');
  });

}
