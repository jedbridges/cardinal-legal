/* Motion for every page that is not the home page.
 *
 * The site has one motion idea worth having, and it belongs to the product:
 * a highlight is made by dragging across words, so the mark draws itself left
 * to right at the speed of a drag. That is the whole thesis. Everything else
 * That is the whole of it. An earlier draft also faded lazy screenshots in on
 * decode; it hid two of them when the decode never came, which is the exact
 * failure a motion layer must not have, and it was not carrying meaning.
 *
 * Deliberately not here: a reveal on every section. Eight stacked entrances
 * is not a motion language, it is the same entrance eight times.
 */
(function () {
  'use strict';

  var reduce = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // ---- The mark draws itself, once ---------------------------------------
  // Held until the sentence is on screen and has settled, so it reads as a
  // hand passing over the words rather than as a page load. Threshold 1 so a
  // phrase that is half on screen does not start drawing off the edge.
  (function () {
    var marks = document.querySelectorAll('.marker');
    if (!marks.length) return;

    if (reduce || !hasIO) {
      // No sweep, but the phrase still ends up marked: the meaning is the
      // mark, and only the drawing of it is the flourish.
      for (var i = 0; i < marks.length; i++) marks[i].classList.add('drawn');
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        setTimeout(function () { e.target.classList.add('drawn'); }, 260);
      });
    }, { threshold: 1, rootMargin: '0px 0px -12% 0px' });

    for (var j = 0; j < marks.length; j++) io.observe(marks[j]);
  })();

})();
