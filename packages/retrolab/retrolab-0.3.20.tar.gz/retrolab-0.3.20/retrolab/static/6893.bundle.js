(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[6893,7684],{56893:(t,e,o)=>{"use strict";o.r(e),o.d(e,{CommandIDs:()=>n,default:()=>l});var n,a=o(21521),r=o(71574),u=o(58291),s=o(56615);!function(t){t.controlPanel="hub:control-panel",t.logout="hub:logout",t.restart="hub:restart"}(n||(n={}));const l=[{activate:function(t,e,o,a){const r=o.load("jupyterlab"),s=e.urls.hubHost||"",l=e.urls.hubPrefix||"",i=e.urls.hubUser||"",c=e.urls.hubServerName||"",b=e.urls.base;if(!l)return;console.debug("hub-extension: Found configuration ",{hubHost:s,hubPrefix:l});const d=c?s+u.URLExt.join(l,"spawn",i,c):s+u.URLExt.join(l,"spawn"),{commands:_}=t;if(_.addCommand(n.restart,{label:r.__("Restart Server"),caption:r.__("Request that the Hub restart this server"),execute:()=>{window.open(d,"_blank")}}),_.addCommand(n.controlPanel,{label:r.__("Hub Control Panel"),caption:r.__("Open the Hub control panel in a new browser tab"),execute:()=>{window.open(s+u.URLExt.join(l,"home"),"_blank")}}),_.addCommand(n.logout,{label:r.__("Log Out"),caption:r.__("Log out of the Hub"),execute:()=>{window.location.href=s+u.URLExt.join(b,"logout")}}),a){const t=r.__("Hub");a.addItem({category:t,command:n.controlPanel}),a.addItem({category:t,command:n.logout})}},id:"jupyter.extensions.hub-extension",requires:[a.JupyterFrontEnd.IPaths,s.ITranslator],optional:[r.ICommandPalette],autoStart:!0},{activate:()=>{},id:"jupyter.extensions.hub-extension:plugin",autoStart:!0},{id:"@jupyterlab/apputils-extension:connectionlost",requires:[a.JupyterFrontEnd.IPaths,s.ITranslator],activate:(t,e,o)=>{const u=o.load("jupyterlab"),s=e.urls.hubPrefix||"",l=e.urls.base;if(!s)return a.ConnectionLost;let i=!1;return async(e,o)=>{if(i)return;i=!0;const a=await(0,r.showDialog)({title:u.__("Server unavailable or unreachable"),body:u.__("Your server at %1 is not running.\nWould you like to restart it?",l),buttons:[r.Dialog.okButton({label:u.__("Restart")}),r.Dialog.cancelButton({label:u.__("Dismiss")})]});i=!1,a.button.accept&&await t.commands.execute(n.restart)}},autoStart:!0,provides:a.IConnectionLost}]}}]);