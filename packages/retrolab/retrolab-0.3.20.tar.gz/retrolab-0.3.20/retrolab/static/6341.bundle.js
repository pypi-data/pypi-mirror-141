(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[6341],{12091:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>o});var r=n(93476),s=n.n(r)()((function(e){return e[1]}));s.push([e.id,".cm-s-ssms span.cm-keyword { color: blue; }\n.cm-s-ssms span.cm-comment { color: darkgreen; }\n.cm-s-ssms span.cm-string { color: red; }\n.cm-s-ssms span.cm-def { color: black; }\n.cm-s-ssms span.cm-variable { color: black; }\n.cm-s-ssms span.cm-variable-2 { color: black; }\n.cm-s-ssms span.cm-atom { color: darkgray; }\n.cm-s-ssms .CodeMirror-linenumber { color: teal; }\n.cm-s-ssms .CodeMirror-activeline-background { background: #ffffff; }\n.cm-s-ssms span.cm-string-2 { color: #FF00FF; }\n.cm-s-ssms span.cm-operator, \n.cm-s-ssms span.cm-bracket, \n.cm-s-ssms span.cm-punctuation { color: darkgray; }\n.cm-s-ssms .CodeMirror-gutters { border-right: 3px solid #ffee62; background-color: #ffffff; }\n.cm-s-ssms div.CodeMirror-selected { background: #ADD6FF; }\n\n",""]);const o=s},93476:e=>{"use strict";e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n=e(t);return t[2]?"@media ".concat(t[2]," {").concat(n,"}"):n})).join("")},t.i=function(e,n,r){"string"==typeof e&&(e=[[null,e,""]]);var s={};if(r)for(var o=0;o<this.length;o++){var a=this[o][0];null!=a&&(s[a]=!0)}for(var i=0;i<e.length;i++){var c=[].concat(e[i]);r&&s[c[0]]||(n&&(c[2]?c[2]="".concat(n," and ").concat(c[2]):c[2]=n),t.push(c))}},t}},56341:(e,t,n)=>{var r=n(12091);"string"==typeof(r=r.__esModule?r.default:r)&&(r=[[e.id,r,""]]);n(1892)(r,{insert:"head",singleton:!1}),r.locals&&(e.exports=r.locals)},1892:(e,t,n)=>{"use strict";var r,s={},o=function(){var e={};return function(t){if(void 0===e[t]){var n=document.querySelector(t);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}e[t]=n}return e[t]}}();function a(e,t){for(var n=[],r={},s=0;s<e.length;s++){var o=e[s],a=t.base?o[0]+t.base:o[0],i={css:o[1],media:o[2],sourceMap:o[3]};r[a]?r[a].parts.push(i):n.push(r[a]={id:a,parts:[i]})}return n}function i(e,t){for(var n=0;n<e.length;n++){var r=e[n],o=s[r.id],a=0;if(o){for(o.refs++;a<o.parts.length;a++)o.parts[a](r.parts[a]);for(;a<r.parts.length;a++)o.parts.push(h(r.parts[a],t))}else{for(var i=[];a<r.parts.length;a++)i.push(h(r.parts[a],t));s[r.id]={id:r.id,refs:1,parts:i}}}}function c(e){var t=document.createElement("style");if(void 0===e.attributes.nonce){var r=n.nc;r&&(e.attributes.nonce=r)}if(Object.keys(e.attributes).forEach((function(n){t.setAttribute(n,e.attributes[n])})),"function"==typeof e.insert)e.insert(t);else{var s=o(e.insert||"head");if(!s)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");s.appendChild(t)}return t}var l,u=(l=[],function(e,t){return l[e]=t,l.filter(Boolean).join("\n")});function f(e,t,n,r){var s=n?"":r.css;if(e.styleSheet)e.styleSheet.cssText=u(t,s);else{var o=document.createTextNode(s),a=e.childNodes;a[t]&&e.removeChild(a[t]),a.length?e.insertBefore(o,a[t]):e.appendChild(o)}}function d(e,t,n){var r=n.css,s=n.media,o=n.sourceMap;if(s&&e.setAttribute("media",s),o&&btoa&&(r+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")),e.styleSheet)e.styleSheet.cssText=r;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(r))}}var m=null,p=0;function h(e,t){var n,r,s;if(t.singleton){var o=p++;n=m||(m=c(t)),r=f.bind(null,n,o,!1),s=f.bind(null,n,o,!0)}else n=c(t),r=d.bind(null,n,t),s=function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(n)};return r(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;r(e=t)}else s()}}e.exports=function(e,t){(t=t||{}).attributes="object"==typeof t.attributes?t.attributes:{},t.singleton||"boolean"==typeof t.singleton||(t.singleton=(void 0===r&&(r=Boolean(window&&document&&document.all&&!window.atob)),r));var n=a(e,t);return i(n,t),function(e){for(var r=[],o=0;o<n.length;o++){var c=n[o],l=s[c.id];l&&(l.refs--,r.push(l))}e&&i(a(e,t),t);for(var u=0;u<r.length;u++){var f=r[u];if(0===f.refs){for(var d=0;d<f.parts.length;d++)f.parts[d]();delete s[f.id]}}}}}}]);