(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[7906,4382],{54382:(e,t,r)=>{"use strict";r.r(t),r.d(t,{default:()=>i});var n=r(12033),a=r(67215),s=r(10372);const c="jp-mod-searchable",i=[{id:"@retrolab/documentsearch-extension:disableShortcut",requires:[a.ISettingRegistry],autoStart:!0,activate:async(e,t)=>{var r,n;const a=null===(n=null===(r=t.plugins["@jupyterlab/documentsearch-extension:plugin"])||void 0===r?void 0:r.schema["jupyter.lab.shortcuts"])||void 0===n?void 0:n.find((e=>"documentsearch:start"===e.command));a&&(a.disabled=!0,a.keys=[])}},{id:"@retrolab/documentsearch-extension:retroShellWidgetListener",requires:[s.IRetroShell,n.ISearchProviderRegistry],autoStart:!0,activate:(e,t,r)=>{const n=e=>{if(!e)return;const t=r.getProviderForWidget(e);t&&e.addClass(c),t||e.removeClass(c)};r.changed.connect((()=>n(t.currentWidget))),t.currentChanged.connect(((e,r)=>{t.currentWidget&&n(t.currentWidget)}))}}]}}]);