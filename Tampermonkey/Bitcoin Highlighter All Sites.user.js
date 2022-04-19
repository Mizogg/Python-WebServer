// ==UserScript==
// @name          Bitcoin Highlighter All Sites
// @namespace     https://mizogg.co.uk
// @author        mizogg.co.uk
// @version       1.0
// @description   Highlights BTC Addresses
// @match       https://*
// @grant         GM_registerMenuCommand
// @grant         GM_setValue
// @grant         GM_getValue
// ==/UserScript==


(function() {
  'use strict';

  if (window.self !== window.top) { return; }

  function setUserPref(varName, defaultVal, menuText, promtText, sep){
    GM_registerMenuCommand(menuText, function() {
      var val = prompt(promtText, GM_getValue(varName, defaultVal));
      if (val === null) { return; }
      if (sep && val){
        var pat1 = new RegExp('\\s*' + sep + '+\\s*', 'g');
        var pat2 = new RegExp('(?:^' + sep + '+|' + sep + '+$)', 'g');
        val = val.replace(pat1, sep).replace(pat2, '');
      }
      val = val.replace(/\s{2,}/g, ' ').trim();
      GM_setValue(varName, val);
      if(!document.body.querySelector(".THmo")) THmo_doHighlight(document.body);
      else location.reload();
    });
  }

  setUserPref(
  'keywords',
  'word 1,word 2,word 3',
  'Set Keywords',
  'Set keywords separated by comma\t\t\t\t\t\t\t\r\n\r\nExample:\r\nword 1,word 2,word 3',
  ','
  );

  setUserPref(
  'highlightStyle',
  'color: #f00; background-color: #ffebcd;',
  'Set Highlight Style',
  'Set the Highlight Style (use proper CSS)\r\n\r\nExample:\r\ncolor: #f00; font-weight: bold; background-color: #ffe4b5;'
  );

  var THmo_MutOb = (window.MutationObserver) ? window.MutationObserver : window.WebKitMutationObserver;
  if (THmo_MutOb){
    var THmo_chgMon = new THmo_MutOb(function(mutationSet){
      mutationSet.forEach(function(mutation){
        for (var i=0; i<mutation.addedNodes.length; i++){
          if (mutation.addedNodes[i].nodeType == 1){
            THmo_doHighlight(mutation.addedNodes[i]);
          }
        }
      });
    });
    var opts = {childList: true, subtree: true};
    THmo_chgMon.observe(document.body, opts);
  }
  function THmo_doHighlight(el){
    var keywords = GM_getValue('keywords');
    if(!keywords) { return; }
    var highlightStyle = GM_getValue('highlightStyle');
    if (!highlightStyle) highlightStyle = "color:#00f; font-weight:bold; background-color: #0f0;"

    var rQuantifiers = /[-\/\\^$*+?.()|[\]{}]/g;
    keywords = keywords.replace(rQuantifiers, '\\$&').split(',').join('|');
    var pat = new RegExp('(' + keywords + ')', 'gi');
    var span = document.createElement('span');
    var snapElements = document.evaluate(
        './/text()[normalize-space() != "" ' +
        'and not(ancestor::style) ' +
        'and not(ancestor::script) ' +
        'and not(ancestor::textarea) ' +
        'and not(ancestor::code) ' +
        'and not(ancestor::pre)]',
        el, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);

    if (!snapElements.snapshotItem(0)) { return; }

    for (var i = 0, len = snapElements.snapshotLength; i < len; i++) {
      var node = snapElements.snapshotItem(i);
      if (pat.test(node.nodeValue)) {
        if (node.className != "THmo" && node.parentNode.className != "THmo"){
          var sp = span.cloneNode(true);
          sp.innerHTML = node.nodeValue.replace(pat, '<span style="' + highlightStyle + '" class="THmo">$1</span>');
          node.parentNode.replaceChild(sp, node);
		     alert("NICE ONE BITCOINS FOUND!!!!!")
        }
      }
    }
  }
  THmo_doHighlight(document.body);
})();