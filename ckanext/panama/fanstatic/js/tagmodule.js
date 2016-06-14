'use strict';

ckan.module('tagmodule', function ($, _) {
  return {
    initialize: function () {
      console.log(this.el.context.id);
      (function () {
        try {
          TagCanvas.Start('myCanvas', 'tags', {
            textColour: '#000000',
            outlineColour: '#2d3f53',
            reverse: true,
            depth: 0.5,
            maxSpeed: 0.03,
            wheelZoom: false
          });
        } catch (e) {
          // something went wrong, hide the canvas container
          console.log(e);
          $('#myCanvasContainer').style.display = 'none';
        }
      })();
    }
  }
});