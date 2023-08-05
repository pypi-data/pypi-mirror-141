(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[3004],{78027:(r,e,o)=>{"use strict";o.r(e),o.d(e,{default:()=>c});var n=o(93476),t=o.n(n)()((function(r){return r[1]}));t.push([r.id,"/*\n  Name:       lucario\n  Author:     Raphael Amorim\n\n  Original Lucario color scheme (https://github.com/raphamorim/lucario)\n*/\n\n.cm-s-lucario.CodeMirror, .cm-s-lucario .CodeMirror-gutters {\n  background-color: #2b3e50 !important;\n  color: #f8f8f2 !important;\n  border: none;\n}\n.cm-s-lucario .CodeMirror-gutters { color: #2b3e50; }\n.cm-s-lucario .CodeMirror-cursor { border-left: solid thin #E6C845; }\n.cm-s-lucario .CodeMirror-linenumber { color: #f8f8f2; }\n.cm-s-lucario .CodeMirror-selected { background: #243443; }\n.cm-s-lucario .CodeMirror-line::selection, .cm-s-lucario .CodeMirror-line > span::selection, .cm-s-lucario .CodeMirror-line > span > span::selection { background: #243443; }\n.cm-s-lucario .CodeMirror-line::-moz-selection, .cm-s-lucario .CodeMirror-line > span::-moz-selection, .cm-s-lucario .CodeMirror-line > span > span::-moz-selection { background: #243443; }\n.cm-s-lucario span.cm-comment { color: #5c98cd; }\n.cm-s-lucario span.cm-string, .cm-s-lucario span.cm-string-2 { color: #E6DB74; }\n.cm-s-lucario span.cm-number { color: #ca94ff; }\n.cm-s-lucario span.cm-variable { color: #f8f8f2; }\n.cm-s-lucario span.cm-variable-2 { color: #f8f8f2; }\n.cm-s-lucario span.cm-def { color: #72C05D; }\n.cm-s-lucario span.cm-operator { color: #66D9EF; }\n.cm-s-lucario span.cm-keyword { color: #ff6541; }\n.cm-s-lucario span.cm-atom { color: #bd93f9; }\n.cm-s-lucario span.cm-meta { color: #f8f8f2; }\n.cm-s-lucario span.cm-tag { color: #ff6541; }\n.cm-s-lucario span.cm-attribute { color: #66D9EF; }\n.cm-s-lucario span.cm-qualifier { color: #72C05D; }\n.cm-s-lucario span.cm-property { color: #f8f8f2; }\n.cm-s-lucario span.cm-builtin { color: #72C05D; }\n.cm-s-lucario span.cm-variable-3, .cm-s-lucario span.cm-type { color: #ffb86c; }\n\n.cm-s-lucario .CodeMirror-activeline-background { background: #243443; }\n.cm-s-lucario .CodeMirror-matchingbracket { text-decoration: underline; color: white !important; }\n",""]);const c=t},93476:r=>{"use strict";r.exports=function(r){var e=[];return e.toString=function(){return this.map((function(e){var o=r(e);return e[2]?"@media ".concat(e[2]," {").concat(o,"}"):o})).join("")},e.i=function(r,o,n){"string"==typeof r&&(r=[[null,r,""]]);var t={};if(n)for(var c=0;c<this.length;c++){var a=this[c][0];null!=a&&(t[a]=!0)}for(var i=0;i<r.length;i++){var s=[].concat(r[i]);n&&t[s[0]]||(o&&(s[2]?s[2]="".concat(o," and ").concat(s[2]):s[2]=o),e.push(s))}},e}},43004:(r,e,o)=>{var n=o(78027);"string"==typeof(n=n.__esModule?n.default:n)&&(n=[[r.id,n,""]]);o(1892)(n,{insert:"head",singleton:!1}),n.locals&&(r.exports=n.locals)},1892:(r,e,o)=>{"use strict";var n,t={},c=function(){var r={};return function(e){if(void 0===r[e]){var o=document.querySelector(e);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement)try{o=o.contentDocument.head}catch(r){o=null}r[e]=o}return r[e]}}();function a(r,e){for(var o=[],n={},t=0;t<r.length;t++){var c=r[t],a=e.base?c[0]+e.base:c[0],i={css:c[1],media:c[2],sourceMap:c[3]};n[a]?n[a].parts.push(i):o.push(n[a]={id:a,parts:[i]})}return o}function i(r,e){for(var o=0;o<r.length;o++){var n=r[o],c=t[n.id],a=0;if(c){for(c.refs++;a<c.parts.length;a++)c.parts[a](n.parts[a]);for(;a<n.parts.length;a++)c.parts.push(h(n.parts[a],e))}else{for(var i=[];a<n.parts.length;a++)i.push(h(n.parts[a],e));t[n.id]={id:n.id,refs:1,parts:i}}}}function s(r){var e=document.createElement("style");if(void 0===r.attributes.nonce){var n=o.nc;n&&(r.attributes.nonce=n)}if(Object.keys(r.attributes).forEach((function(o){e.setAttribute(o,r.attributes[o])})),"function"==typeof r.insert)r.insert(e);else{var t=c(r.insert||"head");if(!t)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");t.appendChild(e)}return e}var l,u=(l=[],function(r,e){return l[r]=e,l.filter(Boolean).join("\n")});function f(r,e,o,n){var t=o?"":n.css;if(r.styleSheet)r.styleSheet.cssText=u(e,t);else{var c=document.createTextNode(t),a=r.childNodes;a[e]&&r.removeChild(a[e]),a.length?r.insertBefore(c,a[e]):r.appendChild(c)}}function m(r,e,o){var n=o.css,t=o.media,c=o.sourceMap;if(t&&r.setAttribute("media",t),c&&btoa&&(n+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(c))))," */")),r.styleSheet)r.styleSheet.cssText=n;else{for(;r.firstChild;)r.removeChild(r.firstChild);r.appendChild(document.createTextNode(n))}}var d=null,p=0;function h(r,e){var o,n,t;if(e.singleton){var c=p++;o=d||(d=s(e)),n=f.bind(null,o,c,!1),t=f.bind(null,o,c,!0)}else o=s(e),n=m.bind(null,o,e),t=function(){!function(r){if(null===r.parentNode)return!1;r.parentNode.removeChild(r)}(o)};return n(r),function(e){if(e){if(e.css===r.css&&e.media===r.media&&e.sourceMap===r.sourceMap)return;n(r=e)}else t()}}r.exports=function(r,e){(e=e||{}).attributes="object"==typeof e.attributes?e.attributes:{},e.singleton||"boolean"==typeof e.singleton||(e.singleton=(void 0===n&&(n=Boolean(window&&document&&document.all&&!window.atob)),n));var o=a(r,e);return i(o,e),function(r){for(var n=[],c=0;c<o.length;c++){var s=o[c],l=t[s.id];l&&(l.refs--,n.push(l))}r&&i(a(r,e),e);for(var u=0;u<n.length;u++){var f=n[u];if(0===f.refs){for(var m=0;m<f.parts.length;m++)f.parts[m]();delete t[f.id]}}}}}}]);