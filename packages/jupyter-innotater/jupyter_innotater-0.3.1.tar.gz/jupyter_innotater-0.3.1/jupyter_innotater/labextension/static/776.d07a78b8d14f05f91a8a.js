(self.webpackChunkjupyter_innotater=self.webpackChunkjupyter_innotater||[]).push([[776],{3811:(n,e,t)=>{(e=t(3645)(!1)).push([n.id,'\ncanvas.jupyter-innotater-imagepad {\n    margin-left: auto; \n    margin-right: auto; \n    display: block;\n    cursor: default;\n    border: 1px solid black;\n}\n\ncanvas.jupyter-innotater-imagepad.is_bb_source {\n    cursor: crosshair;\n}\n\n.innotater-base {\n    outline: none;\n    margin: 10px 0px;\n}\n\n.innotater-controlbar .widget-slider .widget-readout{\n    border: 1px solid lightgray;\n}\n\n.innotater-controlbar {\n    margin-top: 5px;\n}\n\n.innotater-base .widget-textarea textarea, .innotater-base .widget-text input[type="text"] {\n    opacity: 1.0; /* Disabled TextInnotations still want to be highly readable */\n}\n\n.innotater-base .bounding-box-active {\n    border: green 1px solid;\n}\n\n.innotater-base .repeat-innotation {\n    padding: 10px 2px;\n}\n\n.innotater-base-vertical > div.widget-box > div.widget-vbox {\n    /* A bit more space between inputs/targets when stacked vertically */\n    margin-bottom: 20px;\n}\n\n/* Kaggle Overrides */\n\n.innotater-kaggle .widget-hbox {\n    width: 90% !important;\n    display: flex !important;\n}\n\n.innotater-kaggle .widget-inline-hbox {\n    display: flex !important;\n}\n',""]),n.exports=e},3645:n=>{"use strict";n.exports=function(n){var e=[];return e.toString=function(){return this.map((function(e){var t=function(n,e){var t,r,a,i=n[1]||"",o=n[3];if(!o)return i;if(e&&"function"==typeof btoa){var c=(t=o,r=btoa(unescape(encodeURIComponent(JSON.stringify(t)))),a="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(r),"/*# ".concat(a," */")),s=o.sources.map((function(n){return"/*# sourceURL=".concat(o.sourceRoot||"").concat(n," */")}));return[i].concat(s).concat([c]).join("\n")}return[i].join("\n")}(e,n);return e[2]?"@media ".concat(e[2]," {").concat(t,"}"):t})).join("")},e.i=function(n,t,r){"string"==typeof n&&(n=[[null,n,""]]);var a={};if(r)for(var i=0;i<this.length;i++){var o=this[i][0];null!=o&&(a[o]=!0)}for(var c=0;c<n.length;c++){var s=[].concat(n[c]);r&&a[s[0]]||(t&&(s[2]?s[2]="".concat(t," and ").concat(s[2]):s[2]=t),e.push(s))}},e}},2819:(n,e,t)=>{var r=t(3379),a=t(3811);"string"==typeof(a=a.__esModule?a.default:a)&&(a=[[n.id,a,""]]);r(a,{insert:"head",singleton:!1}),n.exports=a.locals||{}},3379:(n,e,t)=>{"use strict";var r,a=function(){var n={};return function(e){if(void 0===n[e]){var t=document.querySelector(e);if(window.HTMLIFrameElement&&t instanceof window.HTMLIFrameElement)try{t=t.contentDocument.head}catch(n){t=null}n[e]=t}return n[e]}}(),i=[];function o(n){for(var e=-1,t=0;t<i.length;t++)if(i[t].identifier===n){e=t;break}return e}function c(n,e){for(var t={},r=[],a=0;a<n.length;a++){var c=n[a],s=e.base?c[0]+e.base:c[0],u=t[s]||0,l="".concat(s," ").concat(u);t[s]=u+1;var d=o(l),p={css:c[1],media:c[2],sourceMap:c[3]};-1!==d?(i[d].references++,i[d].updater(p)):i.push({identifier:l,updater:g(p,e),references:1}),r.push(l)}return r}function s(n){var e=document.createElement("style"),r=n.attributes||{};if(void 0===r.nonce){var i=t.nc;i&&(r.nonce=i)}if(Object.keys(r).forEach((function(n){e.setAttribute(n,r[n])})),"function"==typeof n.insert)n.insert(e);else{var o=a(n.insert||"head");if(!o)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");o.appendChild(e)}return e}var u,l=(u=[],function(n,e){return u[n]=e,u.filter(Boolean).join("\n")});function d(n,e,t,r){var a=t?"":r.media?"@media ".concat(r.media," {").concat(r.css,"}"):r.css;if(n.styleSheet)n.styleSheet.cssText=l(e,a);else{var i=document.createTextNode(a),o=n.childNodes;o[e]&&n.removeChild(o[e]),o.length?n.insertBefore(i,o[e]):n.appendChild(i)}}function p(n,e,t){var r=t.css,a=t.media,i=t.sourceMap;if(a?n.setAttribute("media",a):n.removeAttribute("media"),i&&"undefined"!=typeof btoa&&(r+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(i))))," */")),n.styleSheet)n.styleSheet.cssText=r;else{for(;n.firstChild;)n.removeChild(n.firstChild);n.appendChild(document.createTextNode(r))}}var f=null,b=0;function g(n,e){var t,r,a;if(e.singleton){var i=b++;t=f||(f=s(e)),r=d.bind(null,t,i,!1),a=d.bind(null,t,i,!0)}else t=s(e),r=p.bind(null,t,e),a=function(){!function(n){if(null===n.parentNode)return!1;n.parentNode.removeChild(n)}(t)};return r(n),function(e){if(e){if(e.css===n.css&&e.media===n.media&&e.sourceMap===n.sourceMap)return;r(n=e)}else a()}}n.exports=function(n,e){(e=e||{}).singleton||"boolean"==typeof e.singleton||(e.singleton=(void 0===r&&(r=Boolean(window&&document&&document.all&&!window.atob)),r));var t=c(n=n||[],e);return function(n){if(n=n||[],"[object Array]"===Object.prototype.toString.call(n)){for(var r=0;r<t.length;r++){var a=o(t[r]);i[a].references--}for(var s=c(n,e),u=0;u<t.length;u++){var l=o(t[u]);0===i[l].references&&(i[l].updater(),i.splice(l,1))}t=s}}}},3776:(n,e,t)=>{"use strict";t.r(e),t(2819)}}]);