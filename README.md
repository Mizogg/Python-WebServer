# 🐍Python-WebServer🐍 and 🐒Tampermonkey🐒

Webserver_ice.py Hunt for Bitcoin Adresses starting 1, 3 and bc1 and ETH.

Webserver_4.9.1.py Hunt for Bitcoin. Just addresses starting with 1

Includes Auto Random and Auto Sequential. No NEED for tamper monkey. Amazing Program. 
```
search field added. To use:(paste and remove focus by clicking)
WIF search by WIF
1878574747  search by page number
@764523535  search page by privatekey decimal
$ffff or $FFFFF search page by privatekey hex
[123] change increment
(2345-8856464646) change random range
```
😊 😇 🙂Special THanks to Alex Curl for All his hard work😊 😇 🙂

https://user-images.githubusercontent.com/88630056/164995299-07b12034-c064-4133-bf87-d57b08239fb0.mp4

![image](https://user-images.githubusercontent.com/88630056/163732565-e298e77e-bb2c-46f7-9b77-e94a1be53a77.png)

![image](https://user-images.githubusercontent.com/88630056/163732575-846162fe-dc77-4160-a90b-4bac14696e26.png)

---------
# Requirements:
- Python3
- https://github.com/iceland2k14/secp256k1 files
- ice_secp256k1.dll
- ice_secp256k1.so
- secp256k1.py
- btcaddress.txt (One address per line)
- ethaddress.txt (One address per line)
- jquery-3.6.0.js
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
# Detailed Information from HEX

![image](https://user-images.githubusercontent.com/88630056/164998242-aec51051-1733-4d94-acc9-f5ef26506dd3.png)

---------

```
1100001011011110000110000011100000000000011111110111001001110001101001010010111101100000011110000000110100000101010011010111001110001011110101110101110101011111000101100111101011111011000001111011010001111110010110110101010000011001111000011111111100001111
(256 bits)

c2de1838007f7271a52f60780d054d738bd75d5f167afb07b47e5b5419e1ff0f

88141099825256245673553921999835541760225970015052508404838443368591216738063

Public ECDSA Key
x: 4774b0a2ac0b325e5ab7d4687b2a63c7540d2655dccab35f72c201da1149f68e

y: 9be0b93c52e19c16b95edd82fd009b8ce5a3840b23a9f720838c29486765a493

x: 32320385601912921618066559609108982423772771673443867077080816380047029565070

y: 70505543722316022944178389399213156382852026814587996716514675175858874197139

x: 034774b0a2ac0b325e5ab7d4687b2a63c7540d2655dccab35f72c201da1149f68e

Additive Inverse Point
3d21e7c7ff808d8e5ad09f87f2fab28b2ed77f8798cda5340b540338b6544232

x: 4774b0a2ac0b325e5ab7d4687b2a63c7540d2655dccab35f72c201da1149f68e

y: 641f46c3ad1e63e946a1227d02ff64731a5c7bf4dc5608df7c73d6b6989a579c

B:No  U: 1M3Wfm1qnyuZgKM5b4QBVUtro6KeVqgoLi  C: 19xbDGGGuqCyBcGTEbvZu16DinJqdjMHZ7

Two More Points same Y different X
x: 867e7fcddaca8b7f9f85a77c0cf81d02d5bd8066f07b318fe0d1f1e9ca29a01e

y: 9be0b93c52e19c16b95edd82fd009b8ce5a3840b23a9f720838c29486765a493

B:No  U: 1KxCXLZsDoTxhUhAFzxAb4dq1vooj1Zi1d  C: 1Avd9PfFq248v2M7MMSbXxNhfJhTY32ssN

x: 320ccf8f792a422205c2841b77dd7f35d635594332ba1b10ac6c0c3b248c6583

y: 9be0b93c52e19c16b95edd82fd009b8ce5a3840b23a9f720838c29486765a493

B:No  U: 1M2oE13jszzS6twUSBxotktgy8jWbbrSVm  C: 13q8qmXFYSeJqLqemFYyK3z7zwUtb78Uom

RIPEMD-160 Hash
U: 664f5c265188f85ba8b0e80b6c946a586d8b0663  C: 444c2585216c5e469ac860ad7dde21e8cbc58a55
```

---------
## 🐒Tampermonkey🐒 Auto Refresh (Get Tamper Monkey https://www.tampermonkey.net/)

For Older Websever.py Version. This Includes addresses starting3 bc1 and ETH.

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

Find Out More Join more Like me on Telegram https://t.me/CryptoCrackersUK
