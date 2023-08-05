(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[6256],{86256:(e,n,t)=>{"use strict";t.r(n),t.d(n,{default:()=>_});var o=t(21521),r=t(71574),a=t(95064),s=t(72658),l=t(10172),c=t(33856),i=t(15872),d=t(53966),u=t(67215),p=t(56615),C=t(88706),m=t(24318),g=t(76943),b=t(78429),k=t(85751);const h={id:"@jupyterlab/console-extension:foreign",requires:[s.IConsoleTracker,u.ISettingRegistry,p.ITranslator],optional:[r.ICommandPalette],activate:function(e,n,t,o,r){const a=o.load("jupyterlab"),{shell:l}=e;n.widgetAdded.connect(((e,n)=>{const o=n.console,r=new s.ForeignHandler({sessionContext:o.sessionContext,parent:o});v.foreignHandlerProperty.set(o,r),t.get("@jupyterlab/console-extension:tracker","showAllKernelActivity").then((({composite:e})=>{const n=e;r.enabled=n})),o.disposed.connect((()=>{r.dispose()}))}));const{commands:c}=e,i=a.__("Console"),d="console:toggle-show-all-kernel-activity";c.addCommand(d,{label:e=>a.__("Show All Kernel Activity"),execute:e=>{const t=function(e){const t=n.currentWidget;return!1!==e.activate&&t&&l.activateById(t.id),t}(e);if(!t)return;const o=v.foreignHandlerProperty.get(t.console);o&&(o.enabled=!o.enabled)},isToggled:()=>{var e;return null!==n.currentWidget&&!!(null===(e=v.foreignHandlerProperty.get(n.currentWidget.console))||void 0===e?void 0:e.enabled)},isEnabled:()=>null!==n.currentWidget&&n.currentWidget===l.currentWidget}),r&&r.addItem({command:d,category:i,args:{isPalette:!0}})},autoStart:!0};var v,f;!function(e){e.foreignHandlerProperty=new k.AttachedProperty({name:"foreignHandler",create:()=>{}})}(v||(v={})),function(e){e.autoClosingBrackets="console:toggle-autoclosing-brackets",e.create="console:create",e.clear="console:clear",e.runUnforced="console:run-unforced",e.runForced="console:run-forced",e.linebreak="console:linebreak",e.interrupt="console:interrupt-kernel",e.restart="console:restart-kernel",e.closeAndShutdown="console:close-and-shutdown",e.open="console:open",e.inject="console:inject",e.changeKernel="console:change-kernel",e.enterToExecute="console:enter-to-execute",e.shiftEnterToExecute="console:shift-enter-to-execute",e.interactionMode="console:interaction-mode",e.replaceSelection="console:replace-selection"}(f||(f={}));const y={id:"@jupyterlab/console-extension:tracker",provides:s.IConsoleTracker,requires:[s.ConsolePanel.IContentFactory,a.IEditorServices,d.IRenderMimeRegistry,u.ISettingRegistry,p.ITranslator],optional:[o.ILayoutRestorer,l.IFileBrowserFactory,i.IMainMenu,r.ICommandPalette,c.ILauncher,o.ILabStatus,r.ISessionContextDialogs],activate:async function(e,n,t,o,a,l,c,i,d,u,p,k,h){const v=l.load("jupyterlab"),y=e.serviceManager,{commands:_,shell:x}=e,w=v.__("Console");h=null!=h?h:r.sessionContextDialogs;const S=new r.WidgetTracker({namespace:"console"});async function B(e){var r;await y.ready;const c=new s.ConsolePanel(Object.assign({manager:y,contentFactory:n,mimeTypeService:t.mimeTypeService,rendermime:o,translator:l,setBusy:null!==(r=k&&(()=>k.setBusy()))&&void 0!==r?r:void 0},e)),i=(await a.get("@jupyterlab/console-extension:tracker","interactionMode")).composite;return c.console.node.dataset.jpInteractionMode=i,await S.add(c),c.sessionContext.propertyChanged.connect((()=>{S.save(c)})),x.add(c,"main",{ref:e.ref,mode:e.insertMode,activate:!1!==e.activate}),c}c&&c.restore(S,{command:f.create,args:e=>{const{path:n,name:t,kernelPreference:o}=e.console.sessionContext;return{path:n,name:t,kernelPreference:Object.assign({},o)}},name:e=>{var n;return null!==(n=e.console.sessionContext.path)&&void 0!==n?n:g.UUID.uuid4()},when:y.ready}),p&&y.ready.then((()=>{let e=null;const n=()=>{e&&(e.dispose(),e=null);const n=y.kernelspecs.specs;if(n){e=new b.DisposableSet;for(const t in n.kernelspecs){const o=t===n.default?0:1/0,r=n.kernelspecs[t];let a=r.resources["logo-64x64"];e.add(p.add({command:f.create,args:{isLauncher:!0,kernelPreference:{name:t}},category:v.__("Console"),rank:o,kernelIconUrl:a,metadata:{kernel:g.JSONExt.deepCopy(r.metadata||{})}}))}}};n(),y.kernelspecs.specsChanged.connect(n)}));const I=(e,n,t)=>{if(void 0!==n[t])switch(t){case"autoClosingBrackets":e.setOption("autoClosingBrackets",n.autoClosingBrackets);break;case"cursorBlinkRate":e.setOption("cursorBlinkRate",n.cursorBlinkRate);break;case"fontFamily":e.setOption("fontFamily",n.fontFamily);break;case"fontSize":e.setOption("fontSize",n.fontSize);break;case"lineHeight":e.setOption("lineHeight",n.lineHeight);break;case"lineNumbers":e.setOption("lineNumbers",n.lineNumbers);break;case"lineWrap":e.setOption("lineWrap",n.lineWrap);break;case"matchBrackets":e.setOption("matchBrackets",n.matchBrackets);break;case"readOnly":e.setOption("readOnly",n.readOnly);break;case"insertSpaces":e.setOption("insertSpaces",n.insertSpaces);break;case"tabSize":e.setOption("tabSize",n.tabSize);break;case"wordWrapColumn":e.setOption("wordWrapColumn",n.wordWrapColumn);break;case"rulers":e.setOption("rulers",n.rulers);break;case"codeFolding":e.setOption("codeFolding",n.codeFolding)}},P="@jupyterlab/console-extension:tracker";let E,O;async function M(e){E=(await a.get(P,"interactionMode")).composite,O=(await a.get(P,"promptCellConfig")).composite;const n=e=>{var n,t,o;e.console.node.dataset.jpInteractionMode=E,t=null===(n=e.console.promptCell)||void 0===n?void 0:n.editor,o=O,void 0!==t&&(I(t,o,"autoClosingBrackets"),I(t,o,"cursorBlinkRate"),I(t,o,"fontFamily"),I(t,o,"fontSize"),I(t,o,"lineHeight"),I(t,o,"lineNumbers"),I(t,o,"lineWrap"),I(t,o,"matchBrackets"),I(t,o,"readOnly"),I(t,o,"insertSpaces"),I(t,o,"tabSize"),I(t,o,"wordWrapColumn"),I(t,o,"rulers"),I(t,o,"codeFolding"))};e?n(e):S.forEach(n)}function A(){return null!==S.currentWidget&&S.currentWidget===x.currentWidget}a.pluginChanged.connect(((e,n)=>{n===P&&M()})),await M(),S.widgetAdded.connect(((e,n)=>{M(n)})),_.addCommand(f.autoClosingBrackets,{execute:async e=>{var n;O.autoClosingBrackets=!!(null!==(n=e.force)&&void 0!==n?n:!O.autoClosingBrackets),await a.set(P,"promptCellConfig",O)},label:v.__("Auto Close Brackets for Code Console Prompt"),isToggled:()=>O.autoClosingBrackets});let F=f.open;function R(e){const n=S.currentWidget;return!1!==e.activate&&n&&x.activateById(n.id),null!=n?n:null}_.addCommand(F,{execute:e=>{const n=e.path,t=S.find((e=>{var t;return(null===(t=e.console.sessionContext.session)||void 0===t?void 0:t.path)===n}));return t?(!1!==e.activate&&x.activateById(t.id),t):y.ready.then((()=>(0,m.find)(y.sessions.running(),(e=>e.path===n))?B(e):Promise.reject(`No running kernel session for path: ${n}`)))}}),F=f.create,_.addCommand(F,{label:e=>{var n,t,o,r;if(e.isPalette)return v.__("New Console");if(e.isLauncher&&e.kernelPreference){const a=e.kernelPreference;return null!==(r=null===(o=null===(t=null===(n=y.kernelspecs)||void 0===n?void 0:n.specs)||void 0===t?void 0:t.kernelspecs[a.name||""])||void 0===o?void 0:o.display_name)&&void 0!==r?r:""}return v.__("Console")},icon:e=>e.isPalette?void 0:C.consoleIcon,execute:e=>{var n;const t=null!==(n=e.basePath||e.cwd||(null==i?void 0:i.defaultBrowser.model.path))&&void 0!==n?n:"";return B(Object.assign({basePath:t},e))}}),_.addCommand(f.clear,{label:v.__("Clear Console Cells"),execute:e=>{const n=R(e);n&&n.console.clear()},isEnabled:A}),_.addCommand(f.runUnforced,{label:v.__("Run Cell (unforced)"),execute:e=>{const n=R(e);if(n)return n.console.execute()},isEnabled:A}),_.addCommand(f.runForced,{label:v.__("Run Cell (forced)"),execute:e=>{const n=R(e);if(n)return n.console.execute(!0)},isEnabled:A}),_.addCommand(f.linebreak,{label:v.__("Insert Line Break"),execute:e=>{const n=R(e);n&&n.console.insertLinebreak()},isEnabled:A}),_.addCommand(f.replaceSelection,{label:v.__("Replace Selection in Console"),execute:e=>{const n=R(e);if(!n)return;const t=e.text||"";n.console.replaceSelection(t)},isEnabled:A}),_.addCommand(f.interrupt,{label:v.__("Interrupt Kernel"),execute:e=>{var n;const t=R(e);if(!t)return;const o=null===(n=t.console.sessionContext.session)||void 0===n?void 0:n.kernel;return o?o.interrupt():void 0},isEnabled:A}),_.addCommand(f.restart,{label:v.__("Restart Kernel…"),execute:e=>{const n=R(e);if(n)return h.restart(n.console.sessionContext,l)},isEnabled:A}),_.addCommand(f.closeAndShutdown,{label:v.__("Close and Shut Down…"),execute:e=>{const n=R(e);if(n)return(0,r.showDialog)({title:v.__("Shut down the console?"),body:v.__('Are you sure you want to close "%1"?',n.title.label),buttons:[r.Dialog.cancelButton(),r.Dialog.warnButton()]}).then((e=>!!e.button.accept&&n.console.sessionContext.shutdown().then((()=>(n.dispose(),!0)))))},isEnabled:A}),_.addCommand(f.inject,{execute:e=>{const n=e.path;S.find((t=>{var o;return(null===(o=t.console.sessionContext.session)||void 0===o?void 0:o.path)===n&&(!1!==e.activate&&x.activateById(t.id),t.console.inject(e.code,e.metadata),!0)}))},isEnabled:A}),_.addCommand(f.changeKernel,{label:v.__("Change Kernel…"),execute:e=>{const n=R(e);if(n)return h.selectKernel(n.console.sessionContext,l)},isEnabled:A}),u&&[f.create,f.linebreak,f.clear,f.runUnforced,f.runForced,f.restart,f.interrupt,f.changeKernel,f.closeAndShutdown].forEach((e=>{u.addItem({command:e,category:w,args:{isPalette:!0}})})),d&&(d.fileMenu.closeAndCleaners.add({tracker:S,closeAndCleanupLabel:e=>v.__("Shutdown Console"),closeAndCleanup:e=>(0,r.showDialog)({title:v.__("Shut down the Console?"),body:v.__('Are you sure you want to close "%1"?',e.title.label),buttons:[r.Dialog.cancelButton(),r.Dialog.warnButton()]}).then((n=>n.button.accept?e.console.sessionContext.shutdown().then((()=>{e.dispose()})):void 0))}),d.kernelMenu.kernelUsers.add({tracker:S,restartKernelAndClearLabel:e=>v.__("Restart Kernel and Clear Console"),interruptKernel:e=>{var n;const t=null===(n=e.console.sessionContext.session)||void 0===n?void 0:n.kernel;return t?t.interrupt():Promise.resolve(void 0)},restartKernel:e=>h.restart(e.console.sessionContext,l),restartKernelAndClear:e=>h.restart(e.console.sessionContext).then((n=>(n&&e.console.clear(),n))),changeKernel:e=>h.selectKernel(e.console.sessionContext,l),shutdownKernel:e=>e.console.sessionContext.shutdown()}),d.runMenu.codeRunners.add({tracker:S,runLabel:e=>v.__("Run Cell"),run:e=>e.console.execute(!0)}),d.editMenu.clearers.add({tracker:S,clearCurrentLabel:e=>v.__("Clear Console Cell"),clearCurrent:e=>e.console.clear()}));const W={notebook:v.__("Execute with Shift+Enter"),terminal:v.__("Execute with Enter")};return _.addCommand(f.interactionMode,{label:e=>W[e.interactionMode]||"",execute:async e=>{try{await a.set(P,"interactionMode",e.interactionMode)}catch(e){console.error(`Failed to set ${P}:keyMap - ${e.message}`)}},isToggled:e=>e.interactionMode===E}),d&&d.helpMenu.kernelUsers.add({tracker:S,getKernel:e=>{var n;return null===(n=e.sessionContext.session)||void 0===n?void 0:n.kernel}}),S},autoStart:!0},_=[{id:"@jupyterlab/console-extension:factory",provides:s.ConsolePanel.IContentFactory,requires:[a.IEditorServices],autoStart:!0,activate:(e,n)=>{const t=n.factoryService.newInlineEditor;return new s.ConsolePanel.ContentFactory({editorFactory:t})}},y,h]}}]);