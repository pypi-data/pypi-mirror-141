(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[9939],{49939:(e,o,t)=>{"use strict";t.r(o),t.d(o,{default:()=>C});var n,c=t(74912),i=t(72658),d=t(23933),r=t(14375),s=t(24318),l=t(36735);!function(e){e.invoke="completer:invoke",e.invokeConsole="completer:invoke-console",e.invokeNotebook="completer:invoke-notebook",e.invokeFile="completer:invoke-file",e.select="completer:select",e.selectConsole="completer:select-console",e.selectNotebook="completer:select-notebook",e.selectFile="completer:select-file"}(n||(n={}));const a={id:"@jupyterlab/completer-extension:manager",autoStart:!0,provides:c.ICompletionManager,activate:e=>{const o={};return e.commands.addCommand(n.invoke,{execute:e=>{const t=e&&e.id;if(!t)return;const n=o[t];n&&n.invoke()}}),e.commands.addCommand(n.select,{execute:e=>{const t=e&&e.id;if(!t)return;const n=o[t];n&&n.completer.selectActive()}}),{register:(e,t=c.Completer.defaultRenderer)=>{const{connector:n,editor:i,parent:d}=e,r=new c.CompleterModel,s=new c.Completer({editor:i,model:r,renderer:t}),a=new c.CompletionHandler({completer:s,connector:n}),m=d.id;return s.hide(),o[m]=a,a.editor=i,l.Widget.attach(s,document.body),d.disposed.connect((()=>{delete o[m],r.dispose(),s.dispose(),a.dispose()})),a}}}},m={id:"@jupyterlab/completer-extension:consoles",requires:[c.ICompletionManager,i.IConsoleTracker],autoStart:!0,activate:(e,o,t)=>{t.widgetAdded.connect(((e,t)=>{var n,i;const d=t.console,r=null!==(i=null===(n=d.promptCell)||void 0===n?void 0:n.editor)&&void 0!==i?i:null,s=d.sessionContext.session,l=new c.CompletionConnector({session:s,editor:r}),a=o.register({connector:l,editor:r,parent:t}),m=()=>{var e,o;const t=null!==(o=null===(e=d.promptCell)||void 0===e?void 0:e.editor)&&void 0!==o?o:null,n=d.sessionContext.session;a.editor=t,a.connector=new c.CompletionConnector({session:n,editor:t})};d.promptCellCreated.connect(m),d.sessionContext.sessionChanged.connect(m)})),e.commands.addCommand(n.invokeConsole,{execute:()=>{const o=t.currentWidget&&t.currentWidget.id;if(o)return e.commands.execute(n.invoke,{id:o})}}),e.commands.addCommand(n.selectConsole,{execute:()=>{const o=t.currentWidget&&t.currentWidget.id;if(o)return e.commands.execute(n.select,{id:o})}}),e.commands.addKeyBinding({command:n.selectConsole,keys:["Enter"],selector:".jp-ConsolePanel .jp-mod-completer-active"})}},u={id:"@jupyterlab/completer-extension:notebooks",requires:[c.ICompletionManager,r.INotebookTracker],autoStart:!0,activate:(e,o,t)=>{t.widgetAdded.connect(((e,t)=>{var n,i;const d=null!==(i=null===(n=t.content.activeCell)||void 0===n?void 0:n.editor)&&void 0!==i?i:null,r=t.sessionContext.session,s=new c.CompletionConnector({session:r,editor:d}),l=o.register({connector:s,editor:d,parent:t}),a=()=>{var e,o;const n=null!==(o=null===(e=t.content.activeCell)||void 0===e?void 0:e.editor)&&void 0!==o?o:null,i=t.sessionContext.session;l.editor=n,l.connector=new c.CompletionConnector({session:i,editor:n})};t.content.activeCellChanged.connect(a),t.sessionContext.sessionChanged.connect(a)})),e.commands.addCommand(n.invokeNotebook,{execute:()=>{var o;const c=t.currentWidget;if(c&&"code"===(null===(o=c.content.activeCell)||void 0===o?void 0:o.model.type))return e.commands.execute(n.invoke,{id:c.id})}}),e.commands.addCommand(n.selectNotebook,{execute:()=>{const o=t.currentWidget&&t.currentWidget.id;if(o)return e.commands.execute(n.select,{id:o})}}),e.commands.addKeyBinding({command:n.selectNotebook,keys:["Enter"],selector:".jp-Notebook .jp-mod-completer-active"})}},p={id:"@jupyterlab/completer-extension:files",requires:[c.ICompletionManager,d.IEditorTracker],autoStart:!0,activate:(e,o,t)=>{const i={};t.widgetAdded.connect(((t,n)=>{const d=e.serviceManager.sessions,r=n.content.editor,l=new c.ContextConnector({editor:r}),a=o.register({connector:l,editor:r,parent:n}),m=(e,o)=>{const t=i[n.id],m=(0,s.find)(o,(e=>e.path===n.context.path));if(m){if(t&&t.id===m.id)return;t&&(delete i[n.id],t.dispose());const e=d.connectTo({model:m});a.connector=new c.CompletionConnector({session:e,editor:r}),i[n.id]=e}else a.connector=l,t&&(delete i[n.id],t.dispose())};m(0,(0,s.toArray)(d.running())),d.runningChanged.connect(m),n.disposed.connect((()=>{d.runningChanged.disconnect(m);const e=i[n.id];e&&(delete i[n.id],e.dispose())}))})),e.commands.addCommand(n.invokeFile,{execute:()=>{const o=t.currentWidget&&t.currentWidget.id;if(o)return e.commands.execute(n.invoke,{id:o})}}),e.commands.addCommand(n.selectFile,{execute:()=>{const o=t.currentWidget&&t.currentWidget.id;if(o)return e.commands.execute(n.select,{id:o})}}),e.commands.addKeyBinding({command:n.selectFile,keys:["Enter"],selector:".jp-FileEditor .jp-mod-completer-active"})}},C=[a,m,u,p]}}]);