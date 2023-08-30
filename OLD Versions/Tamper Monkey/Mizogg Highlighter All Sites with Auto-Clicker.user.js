// ==UserScript==
// @name          Mizogg Highlighter All Sites with Auto-Clicker
// @namespace     https://mizogg.co.uk
// @author        mizogg.co.uk
// @version       2.1
// @description   Highlights BTC Addresses and Auto-Clicker
// @match         https://*/*
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

            // Check for the number of keywords
            var numKeywords = val.split(sep).length;
            if (numKeywords > 300) {
                alert("Warning: You have provided a large number of keywords (" + numKeywords + "). This may slow down the script's performance. It's recommended to keep the number of keywords below 300.");
            }

            GM_setValue(varName, val);
            if (varName === 'clickInterval') {
                startAutoClicker(Number(val));
            } else {
                if (!document.body.querySelector(".mizogg-highlight")) THmo_doHighlight(document.body);
                else location.reload();
            }
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

    setUserPref(
        'showAlert',
        'true',
        'Toggle Alert for Found Keywords',
        'Do you want to be alerted when keywords are found? (true/false)'
    );

    setUserPref(
        'clickInterval',
        '1000',
        'Set Auto-Clicker Interval (ms)',
        'Set the interval for auto-clicker (in milliseconds, e.g., 1000 for 1 second)'
    );

    let currentMousePos = { x: -1, y: -1 };
    document.addEventListener('mousemove', function(event) {
        currentMousePos.x = event.pageX;
        currentMousePos.y = event.pageY;
    });

    let autoClickerInterval = null;
    let autoClickerActive = GM_getValue('autoClickerState', false); // Get the saved state on script start

    function toggleAutoClicker() {
        autoClickerActive = !autoClickerActive;
        GM_setValue('autoClickerState', autoClickerActive);  // Save the state
        if (autoClickerActive) {
            let clickInterval = GM_getValue('clickInterval', 1000);
            startAutoClicker(clickInterval);
        } else {
            if (autoClickerInterval) {
                clearInterval(autoClickerInterval);
                autoClickerInterval = null;
            }
        }
    }

    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey) {
            toggleAutoClicker();
            alert(`Auto-clicker is now ${autoClickerActive ? 'ON' : 'OFF'}`);
        }
    });

    function startAutoClicker(interval) {
        console.log('Starting auto-clicker with an interval of', interval, 'milliseconds.'); // Debugging line
        autoClickerInterval = setInterval(() => {
            if (autoClickerActive && currentMousePos.x > -1 && currentMousePos.y > -1) {
                console.log('Attempting to click at position:', currentMousePos.x, currentMousePos.y); // Debugging line
                var element = document.elementFromPoint(currentMousePos.x, currentMousePos.y);
                if (element) {
                    console.log("Auto-clicking element:", element);
                    var clickEvent = new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true
                    });
                    element.dispatchEvent(clickEvent);
                } else {
                    console.log("No element found under cursor.");
                }
            }
        }, interval);
    }

    // Start the auto-clicker if it was previously active
    if (autoClickerActive) {
        let clickInterval = GM_getValue('clickInterval', 1000);
        startAutoClicker(clickInterval);
    }

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

        var foundKeywords = [];

        for (var i = 0, len = snapElements.snapshotLength; i < len; i++) {
            var node = snapElements.snapshotItem(i);
            if (pat.test(node.nodeValue)) {
                if (node.className != "mizogg-highlight" && node.parentNode.className != "mizogg-highlight"){
                    var sp = span.cloneNode(true);
                    sp.innerHTML = node.nodeValue.replace(pat, function(matched){
                        foundKeywords.push(matched);
                        return '<span style="' + highlightStyle + '" class="mizogg-highlight">' + matched + '</span>';
                    });
                    node.parentNode.replaceChild(sp, node);
                }
            }
        }

        var showAlert = GM_getValue('showAlert') === 'true';
        if(showAlert && foundKeywords.length) {
            alert("NICE ONE BITCOINS FOUND!!!!!\n\n" + foundKeywords.join(", "));
        }
    }

    THmo_doHighlight(document.body);
})();
