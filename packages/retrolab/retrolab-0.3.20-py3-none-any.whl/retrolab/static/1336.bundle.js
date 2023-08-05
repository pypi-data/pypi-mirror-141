(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[1336],{85073:(r,t,o)=>{"use strict";o.r(t),o.d(t,{default:()=>i});var n=o(93476),e=o.n(n)()((function(r){return r[1]}));e.push([r.id,"/*\n\n    Name:       Tomorrow Night - Bright\n    Author:     Chris Kempson\n\n    Port done by Gerard Braad <me@gbraad.nl>\n\n*/\n\n.cm-s-tomorrow-night-bright.CodeMirror { background: #000000; color: #eaeaea; }\n.cm-s-tomorrow-night-bright div.CodeMirror-selected { background: #424242; }\n.cm-s-tomorrow-night-bright .CodeMirror-gutters { background: #000000; border-right: 0px; }\n.cm-s-tomorrow-night-bright .CodeMirror-guttermarker { color: #e78c45; }\n.cm-s-tomorrow-night-bright .CodeMirror-guttermarker-subtle { color: #777; }\n.cm-s-tomorrow-night-bright .CodeMirror-linenumber { color: #424242; }\n.cm-s-tomorrow-night-bright .CodeMirror-cursor { border-left: 1px solid #6A6A6A; }\n\n.cm-s-tomorrow-night-bright span.cm-comment { color: #d27b53; }\n.cm-s-tomorrow-night-bright span.cm-atom { color: #a16a94; }\n.cm-s-tomorrow-night-bright span.cm-number { color: #a16a94; }\n\n.cm-s-tomorrow-night-bright span.cm-property, .cm-s-tomorrow-night-bright span.cm-attribute { color: #99cc99; }\n.cm-s-tomorrow-night-bright span.cm-keyword { color: #d54e53; }\n.cm-s-tomorrow-night-bright span.cm-string { color: #e7c547; }\n\n.cm-s-tomorrow-night-bright span.cm-variable { color: #b9ca4a; }\n.cm-s-tomorrow-night-bright span.cm-variable-2 { color: #7aa6da; }\n.cm-s-tomorrow-night-bright span.cm-def { color: #e78c45; }\n.cm-s-tomorrow-night-bright span.cm-bracket { color: #eaeaea; }\n.cm-s-tomorrow-night-bright span.cm-tag { color: #d54e53; }\n.cm-s-tomorrow-night-bright span.cm-link { color: #a16a94; }\n.cm-s-tomorrow-night-bright span.cm-error { background: #d54e53; color: #6A6A6A; }\n\n.cm-s-tomorrow-night-bright .CodeMirror-activeline-background { background: #2a2a2a; }\n.cm-s-tomorrow-night-bright .CodeMirror-matchingbracket { text-decoration: underline; color: white !important; }\n",""]);const i=e},93476:r=>{"use strict";r.exports=function(r){var t=[];return t.toString=function(){return this.map((function(t){var o=r(t);return t[2]?"@media ".concat(t[2]," {").concat(o,"}"):o})).join("")},t.i=function(r,o,n){"string"==typeof r&&(r=[[null,r,""]]);var e={};if(n)for(var i=0;i<this.length;i++){var a=this[i][0];null!=a&&(e[a]=!0)}for(var s=0;s<r.length;s++){var c=[].concat(r[s]);n&&e[c[0]]||(o&&(c[2]?c[2]="".concat(o," and ").concat(c[2]):c[2]=o),t.push(c))}},t}},21336:(r,t,o)=>{var n=o(85073);"string"==typeof(n=n.__esModule?n.default:n)&&(n=[[r.id,n,""]]);o(1892)(n,{insert:"head",singleton:!1}),n.locals&&(r.exports=n.locals)},1892:(r,t,o)=>{"use strict";var n,e={},i=function(){var r={};return function(t){if(void 0===r[t]){var o=document.querySelector(t);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement)try{o=o.contentDocument.head}catch(r){o=null}r[t]=o}return r[t]}}();function a(r,t){for(var o=[],n={},e=0;e<r.length;e++){var i=r[e],a=t.base?i[0]+t.base:i[0],s={css:i[1],media:i[2],sourceMap:i[3]};n[a]?n[a].parts.push(s):o.push(n[a]={id:a,parts:[s]})}return o}function s(r,t){for(var o=0;o<r.length;o++){var n=r[o],i=e[n.id],a=0;if(i){for(i.refs++;a<i.parts.length;a++)i.parts[a](n.parts[a]);for(;a<n.parts.length;a++)i.parts.push(p(n.parts[a],t))}else{for(var s=[];a<n.parts.length;a++)s.push(p(n.parts[a],t));e[n.id]={id:n.id,refs:1,parts:s}}}}function c(r){var t=document.createElement("style");if(void 0===r.attributes.nonce){var n=o.nc;n&&(r.attributes.nonce=n)}if(Object.keys(r.attributes).forEach((function(o){t.setAttribute(o,r.attributes[o])})),"function"==typeof r.insert)r.insert(t);else{var e=i(r.insert||"head");if(!e)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");e.appendChild(t)}return t}var l,h=(l=[],function(r,t){return l[r]=t,l.filter(Boolean).join("\n")});function u(r,t,o,n){var e=o?"":n.css;if(r.styleSheet)r.styleSheet.cssText=h(t,e);else{var i=document.createTextNode(e),a=r.childNodes;a[t]&&r.removeChild(a[t]),a.length?r.insertBefore(i,a[t]):r.appendChild(i)}}function m(r,t,o){var n=o.css,e=o.media,i=o.sourceMap;if(e&&r.setAttribute("media",e),i&&btoa&&(n+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(i))))," */")),r.styleSheet)r.styleSheet.cssText=n;else{for(;r.firstChild;)r.removeChild(r.firstChild);r.appendChild(document.createTextNode(n))}}var d=null,g=0;function p(r,t){var o,n,e;if(t.singleton){var i=g++;o=d||(d=c(t)),n=u.bind(null,o,i,!1),e=u.bind(null,o,i,!0)}else o=c(t),n=m.bind(null,o,t),e=function(){!function(r){if(null===r.parentNode)return!1;r.parentNode.removeChild(r)}(o)};return n(r),function(t){if(t){if(t.css===r.css&&t.media===r.media&&t.sourceMap===r.sourceMap)return;n(r=t)}else e()}}r.exports=function(r,t){(t=t||{}).attributes="object"==typeof t.attributes?t.attributes:{},t.singleton||"boolean"==typeof t.singleton||(t.singleton=(void 0===n&&(n=Boolean(window&&document&&document.all&&!window.atob)),n));var o=a(r,t);return s(o,t),function(r){for(var n=[],i=0;i<o.length;i++){var c=o[i],l=e[c.id];l&&(l.refs--,n.push(l))}r&&s(a(r,t),t);for(var h=0;h<n.length;h++){var u=n[h];if(0===u.refs){for(var m=0;m<u.parts.length;m++)u.parts[m]();delete e[u.id]}}}}}}]);