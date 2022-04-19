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