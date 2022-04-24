# 🐍Python-WebServer🐍 and 🐒Tampermonkey🐒

![image](https://user-images.githubusercontent.com/88630056/163732565-e298e77e-bb2c-46f7-9b77-e94a1be53a77.png)

![image](https://user-images.githubusercontent.com/88630056/163732575-846162fe-dc77-4160-a90b-4bac14696e26.png)
---------
# Requirements:
- Python3
- "Bit" python module
- https://github.com/iceland2k14/secp256k1 files
- ice_secp256k1.dll
- ice_secp256k1.so
- secp256k1.py
- btcaddress.txt (One address per line)
- ethaddress.txt (One address per line)
---------
To install "Bit Library":
> pip install bit
---------
To Start 🐍Python-WebServer🐍:
> python webserver.py
---------
Start Searching in your Web browser:
- localhost:3333/1 (start from first page)
- localhost:3333/1[256] (change next increment)
- localhost:3333/1(100-500) (change random range)
- Puzzle 64 Start = 144115188075855873 Page
- Puzzle 64 Stop = 288230376151711745 Page
- Random Puzzle 64=  http://localhost:3333/1(144115188075855873-288230376151711745) (change random range)

- wif search = http://localhost:3333/L3VVpPhkahdq7S3DQovZYXXLfFX96o4nfGAgGpGZyJXVw2Fx4XvV
- or http://localhost:3333/5HpHagT65TZzG1PH3CSu64HcGh19CVFzq1pFa44r8FXZrQAaefe

- Dec search = http://localhost:3333/73824873287973477289749872
- or Dec search and Highlight found  http://localhost:3333/@73824873287973477289749872

- HEX Search and Highlight found = http://localhost:3333/$fffffffff 
- or http://localhost:3333/$FFFFF
---------
## 🐒Tampermonkey🐒 Auto Refresh (Get Tamper Monkey https://www.tampermonkey.net/)
---------

https://user-images.githubusercontent.com/88630056/164071903-a00dc295-c287-4934-90c2-07ef6317382b.mp4

---------
![image](https://user-images.githubusercontent.com/88630056/164068392-cecd6564-2316-4d0b-8c3e-362c1869f833.png)
---------
```
// ==UserScript==
// @name         Reload Server
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Reload the Server, find the Key
// @author       AlphaCentury
// @match        http://localhost:3333/*
// @grant        none
// ==/UserScript==
/* global BigInt */
(function() {
    console.log('Go');
    let val = 0n;
      while (val < 1n || val > 904625697166532776746648320380374280100293470930272690489102837043110636674n) {
        let num = '';
        for (let i = 0; i < 75; i++) {
          num += Math.floor(Math.random() * 10);
        }
        val = BigInt(num);
      }
    setTimeout(function() {
        if (document.getElementsByClassName('filled').length !== 0 || document.getElementsByClassName('used').length !== 0) {
            alert('Address found!');
        return;
        };
        document.location.href = val.toString();
    },50);
})();
```
---------
## 🐒Tampermonkey🐒 Highlight and Stop.To find out more on how to use this visit https://mizogg.co.uk/tampermonkey/ ) 

Or Join Telegram Cryptocracker https://t.me/CryptoCrackersUK for instant updates and changes bigger database files to help with your hunt.
---------
```
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
```
