(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[2067],{32067:(e,t,s)=>{"use strict";s.r(t),s.d(t,{CodeConsole:()=>f,ConsoleHistory:()=>l,ConsolePanel:()=>D,ForeignHandler:()=>i,IConsoleTracker:()=>F});var n,o=s(12291);class i{constructor(e){this._enabled=!1,this._isDisposed=!1,this.sessionContext=e.sessionContext,this.sessionContext.iopubMessage.connect(this.onIOPubMessage,this),this._parent=e.parent}get enabled(){return this._enabled}set enabled(e){this._enabled=e}get parent(){return this._parent}get isDisposed(){return this._isDisposed}dispose(){this.isDisposed||(this._isDisposed=!0,o.Signal.clearData(this))}onIOPubMessage(e,t){var s;if(!this._enabled)return!1;const n=null===(s=this.sessionContext.session)||void 0===s?void 0:s.kernel;if(!n)return!1;const o=this._parent;if(t.parent_header.session===n.clientId)return!1;const i=t.header.msg_type,l=t.parent_header.msg_id;let r;switch(i){case"execute_input":{const e=t;r=this._newCell(l);const s=r.model;return s.executionCount=e.content.execution_count,s.value.text=e.content.code,s.trusted=!0,o.update(),!0}case"execute_result":case"display_data":case"stream":case"error":{if(r=this._parent.getCell(l),!r)return!1;const e=Object.assign(Object.assign({},t.content),{output_type:i});return r.model.outputs.add(e),o.update(),!0}case"clear_output":{const e=t.content.wait;return r=this._parent.getCell(l),r&&r.model.outputs.clear(e),!0}default:return!1}}_newCell(e){const t=this.parent.createCodeCell();return t.addClass("jp-CodeConsole-foreignCell"),this._parent.addCell(t,e),t}}class l{constructor(e){this._cursor=0,this._hasSession=!1,this._history=[],this._placeholder="",this._setByHistory=!1,this._isDisposed=!1,this._editor=null,this._filtered=[],this.sessionContext=e.sessionContext,this._handleKernel(),this.sessionContext.kernelChanged.connect(this._handleKernel,this)}get editor(){return this._editor}set editor(e){if(this._editor===e)return;const t=this._editor;t&&(t.edgeRequested.disconnect(this.onEdgeRequest,this),t.model.value.changed.disconnect(this.onTextChange,this)),this._editor=e,e&&(e.edgeRequested.connect(this.onEdgeRequest,this),e.model.value.changed.connect(this.onTextChange,this))}get placeholder(){return this._placeholder}get isDisposed(){return this._isDisposed}dispose(){this._isDisposed=!0,this._history.length=0,o.Signal.clearData(this)}back(e){this._hasSession||(this._hasSession=!0,this._placeholder=e,this.setFilter(e),this._cursor=this._filtered.length-1),--this._cursor,this._cursor=Math.max(0,this._cursor);const t=this._filtered[this._cursor];return Promise.resolve(t)}forward(e){this._hasSession||(this._hasSession=!0,this._placeholder=e,this.setFilter(e),this._cursor=this._filtered.length),++this._cursor,this._cursor=Math.min(this._filtered.length-1,this._cursor);const t=this._filtered[this._cursor];return Promise.resolve(t)}push(e){e&&e!==this._history[this._history.length-1]&&this._history.push(e),this.reset()}reset(){this._cursor=this._history.length,this._hasSession=!1,this._placeholder=""}onHistory(e){this._history.length=0;let t="",s="";if("ok"===e.content.status)for(let n=0;n<e.content.history.length;n++)s=e.content.history[n][2],s!==t&&this._history.push(t=s);this._cursor=this._history.length}onTextChange(){this._setByHistory?this._setByHistory=!1:this.reset()}onEdgeRequest(e,t){const s=e.model,n=s.value.text;"top"===t||"topLine"===t?this.back(n).then((t=>{if(this.isDisposed||!t)return;if(s.value.text===t)return;this._setByHistory=!0,s.value.text=t;let n=0;n=t.indexOf("\n"),n<0&&(n=t.length),e.setCursorPosition({line:0,column:n})})):this.forward(n).then((t=>{if(this.isDisposed)return;const n=t||this.placeholder;if(s.value.text===n)return;this._setByHistory=!0,s.value.text=n;const o=e.getPositionAt(n.length);o&&e.setCursorPosition(o)}))}async _handleKernel(){var e;const t=null===(e=this.sessionContext.session)||void 0===e?void 0:e.kernel;if(t)return t.requestHistory(n.initialRequest).then((e=>{this.onHistory(e)}));this._history.length=0}setFilter(e=""){this._filtered.length=0;let t="",s="";for(let n=0;n<this._history.length;n++)s=this._history[n],s!==t&&e===s.slice(0,e.length)&&this._filtered.push(t=s);this._filtered.push(e)}}!function(e){e.initialRequest={output:!1,raw:!0,hist_access_type:"tail",n:500}}(n||(n={}));var r=s(71574),a=s(58291),h=s(53966),c=s(56615),d=s(88706),u=s(76943),p=s(36735),_=s(97196),C=s(50417),m=s(24318),g=s(71926);const y="jp-Console-cell",v="jp-CodeConsole-promptCell";class f extends p.Widget{constructor(e){super(),this._banner=null,this._executed=new o.Signal(this),this._mimetype="text/x-ipython",this._msgIds=new Map,this._msgIdCells=new Map,this._promptCellCreated=new o.Signal(this),this._dragData=null,this._drag=null,this._focusedCell=null,this.addClass("jp-CodeConsole"),this.node.dataset.jpKernelUser="true",this.node.dataset.jpCodeRunner="true",this.node.tabIndex=-1;const t=this.layout=new p.PanelLayout;this._cells=new C.ObservableList,this._content=new p.Panel,this._input=new p.Panel,this.contentFactory=e.contentFactory||f.defaultContentFactory,this.modelFactory=e.modelFactory||f.defaultModelFactory,this.rendermime=e.rendermime,this.sessionContext=e.sessionContext,this._mimeTypeService=e.mimeTypeService,this._content.addClass("jp-CodeConsole-content"),this._input.addClass("jp-CodeConsole-input"),t.addWidget(this._content),t.addWidget(this._input),this._history=new l({sessionContext:this.sessionContext}),this._onKernelChanged(),this.sessionContext.kernelChanged.connect(this._onKernelChanged,this),this.sessionContext.statusChanged.connect(this._onKernelStatusChanged,this)}get executed(){return this._executed}get promptCellCreated(){return this._promptCellCreated}get cells(){return this._cells}get promptCell(){return this._input.layout.widgets[0]||null}addCell(e,t){e.addClass(y),this._content.addWidget(e),this._cells.push(e),t&&(this._msgIds.set(t,e),this._msgIdCells.set(e,t)),e.disposed.connect(this._onCellDisposed,this),this.update()}addBanner(){if(this._banner){const e=this._banner;this._cells.push(this._banner),e.disposed.connect(this._onCellDisposed,this)}const e=this.modelFactory.createRawCell({});e.value.text="...";const t=(this._banner=new _.RawCell({model:e,contentFactory:this.contentFactory,placeholder:!1})).initializeState();t.addClass("jp-CodeConsole-banner"),t.readOnly=!0,this._content.addWidget(t)}clear(){const e=this._cells;for(;e.length>0;)e.get(0).dispose()}createCodeCell(){const e=this.contentFactory,t=this._createCodeCellOptions(),s=e.createCodeCell(t);return s.readOnly=!0,s.model.mimeType=this._mimetype,s}dispose(){this.isDisposed||(this._cells.clear(),this._msgIdCells=null,this._msgIds=null,this._history.dispose(),super.dispose())}async execute(e=!1,t=250){var s,n;if("dead"===(null===(n=null===(s=this.sessionContext.session)||void 0===s?void 0:s.kernel)||void 0===n?void 0:n.status))return;const o=this.promptCell;if(!o)throw new Error("Cannot execute without a prompt cell");if(o.model.trusted=!0,e)return this.newPromptCell(),void await this._execute(o);const i=await this._shouldExecute(t);this.isDisposed||(i?(this.newPromptCell(),this.promptCell.editor.focus(),await this._execute(o)):o.editor.newIndentedLine())}getCell(e){return this._msgIds.get(e)}inject(e,t={}){const s=this.createCodeCell();s.model.value.text=e;for(const e of Object.keys(t))s.model.metadata.set(e,t[e]);return this.addCell(s),this._execute(s)}insertLinebreak(){const e=this.promptCell;e&&e.editor.newIndentedLine()}replaceSelection(e){var t,s;const n=this.promptCell;n&&(null===(s=(t=n.editor).replaceSelection)||void 0===s||s.call(t,e))}serialize(){const e=[];return(0,m.each)(this._cells,(t=>{const s=t.model;(0,_.isCodeCellModel)(s)&&e.push(s.toJSON())})),this.promptCell&&e.push(this.promptCell.model.toJSON()),e}_evtMouseDown(e){const{button:t,shiftKey:s}=e;if(0!==t&&2!==t||s&&2===t)return;let n=e.target;const o=e=>e.classList.contains(y);let i=_.CellDragUtils.findCell(n,this._cells,o);if(-1===i&&(n=document.elementFromPoint(e.clientX,e.clientY),i=_.CellDragUtils.findCell(n,this._cells,o)),-1===i)return;const l=this._cells.get(i);"prompt"===_.CellDragUtils.detectTargetArea(l,e.target)&&(this._dragData={pressX:e.clientX,pressY:e.clientY,index:i},this._focusedCell=l,document.addEventListener("mouseup",this,!0),document.addEventListener("mousemove",this,!0),e.preventDefault())}_evtMouseMove(e){const t=this._dragData;t&&_.CellDragUtils.shouldStartDrag(t.pressX,t.pressY,e.clientX,e.clientY)&&this._startDrag(t.index,e.clientX,e.clientY)}_startDrag(e,t,s){const n=this._focusedCell.model,o=[n.toJSON()],i=_.CellDragUtils.createCellDragImage(this._focusedCell,o);this._drag=new g.Drag({mimeData:new u.MimeData,dragImage:i,proposedAction:"copy",supportedActions:"copy",source:this}),this._drag.mimeData.setData("application/vnd.jupyter.cells",o);const l=n.value.text;return this._drag.mimeData.setData("text/plain",l),this._focusedCell=null,document.removeEventListener("mousemove",this,!0),document.removeEventListener("mouseup",this,!0),this._drag.start(t,s).then((()=>{this.isDisposed||(this._drag=null,this._dragData=null)}))}handleEvent(e){switch(e.type){case"keydown":this._evtKeyDown(e);break;case"mousedown":this._evtMouseDown(e);break;case"mousemove":this._evtMouseMove(e);break;case"mouseup":this._evtMouseUp(e)}}onAfterAttach(e){const t=this.node;t.addEventListener("keydown",this,!0),t.addEventListener("click",this),t.addEventListener("mousedown",this),this.promptCell?(this.promptCell.editor.focus(),this.update()):this.newPromptCell()}onBeforeDetach(e){const t=this.node;t.removeEventListener("keydown",this,!0),t.removeEventListener("click",this)}onActivateRequest(e){const t=this.promptCell&&this.promptCell.editor;t&&t.focus(),this.update()}newPromptCell(){let e=this.promptCell;const t=this._input;e&&(e.readOnly=!0,e.removeClass(v),o.Signal.clearData(e.editor),t.widgets[0].parent=null,this.addCell(e));const s=this.contentFactory,n=this._createCodeCellOptions();e=s.createCodeCell(n),e.model.mimeType=this._mimetype,e.addClass(v),this._input.addWidget(e);const i=e.editor;i.addKeydownHandler(this._onEditorKeydown),this._history.editor=i,this._promptCellCreated.emit(e)}onUpdateRequest(e){x.scrollToBottom(this._content.node)}_evtKeyDown(e){const t=this.promptCell&&this.promptCell.editor;t&&(13!==e.keyCode||t.hasFocus()?27===e.keyCode&&t.hasFocus()&&(e.preventDefault(),e.stopPropagation(),this.node.focus()):(e.preventDefault(),t.focus()))}_evtMouseUp(e){this.promptCell&&this.promptCell.node.contains(e.target)&&this.promptCell.editor.focus()}_execute(e){const t=e.model.value.text;return this._history.push(t),"clear"===t||"%clear"===t?(this.clear(),Promise.resolve(void 0)):(e.model.contentChanged.connect(this.update,this),_.CodeCell.execute(e,this.sessionContext).then((t=>{if(!this.isDisposed){if(t&&"ok"===t.content.status){const s=t.content;if(s.payload&&s.payload.length){const t=s.payload.filter((e=>"set_next_input"===e.source))[0];if(t){const s=t.text;e.model.value.text=s}}}else t&&"error"===t.content.status&&(0,m.each)(this._cells,(e=>{null===e.model.executionCount&&e.setPrompt("")}));e.model.contentChanged.disconnect(this.update,this),this.update(),this._executed.emit(new Date)}}),(()=>{this.isDisposed||(e.model.contentChanged.disconnect(this.update,this),this.update())})))}_handleInfo(e){if("ok"!==e.status)return void(this._banner.model.value.text="Error in getting kernel banner");this._banner.model.value.text=e.banner;const t=e.language_info;this._mimetype=this._mimeTypeService.getMimeTypeByLanguage(t),this.promptCell&&(this.promptCell.model.mimeType=this._mimetype)}_createCodeCellOptions(){const e=this.contentFactory;return{model:this.modelFactory.createCodeCell({}),rendermime:this.rendermime,contentFactory:e,placeholder:!1}}_onCellDisposed(e,t){if(!this.isDisposed){this._cells.removeValue(e);const t=this._msgIdCells.get(e);t&&(this._msgIdCells.delete(e),this._msgIds.delete(t))}}_shouldExecute(e){const t=this.promptCell;if(!t)return Promise.resolve(!1);const s=t.model.value.text;return new Promise(((t,n)=>{var o;const i=setTimeout((()=>{t(!0)}),e),l=null===(o=this.sessionContext.session)||void 0===o?void 0:o.kernel;l?l.requestIsComplete({code:s}).then((e=>{clearTimeout(i),this.isDisposed&&t(!1),"incomplete"===e.content.status?t(!1):t(!0)})).catch((()=>{t(!0)})):t(!1)}))}_onEditorKeydown(e,t){return 13===t.keyCode}async _onKernelChanged(){var e;this.clear(),this._banner&&(this._banner.dispose(),this._banner=null),this.addBanner(),(null===(e=this.sessionContext.session)||void 0===e?void 0:e.kernel)&&this._handleInfo(await this.sessionContext.session.kernel.info)}async _onKernelStatusChanged(){var e;const t=null===(e=this.sessionContext.session)||void 0===e?void 0:e.kernel;"restarting"===(null==t?void 0:t.status)&&(this.addBanner(),this._handleInfo(await(null==t?void 0:t.info)))}}var x,w;!function(e){class t extends _.Cell.ContentFactory{createCodeCell(e){return e.contentFactory||(e.contentFactory=this),new _.CodeCell(e).initializeState()}createRawCell(e){return e.contentFactory||(e.contentFactory=this),new _.RawCell(e).initializeState()}}e.ContentFactory=t,e.defaultContentFactory=new t;class s{constructor(e={}){this.codeCellContentFactory=e.codeCellContentFactory||_.CodeCellModel.defaultContentFactory}createCodeCell(e){return e.contentFactory||(e.contentFactory=this.codeCellContentFactory),new _.CodeCellModel(e)}createRawCell(e){return new _.RawCellModel(e)}}e.ModelFactory=s,e.defaultModelFactory=new s({})}(f||(f={})),function(e){e.scrollToBottom=function(e){e.scrollTop=e.scrollHeight-e.clientHeight}}(x||(x={}));class D extends r.MainAreaWidget{constructor(e){super({content:new p.Panel}),this._executed=null,this._connected=null,this.addClass("jp-ConsolePanel");let{rendermime:t,mimeTypeService:s,path:n,basePath:o,name:i,manager:l,modelFactory:_,sessionContext:C,translator:m}=e;this.translator=m||c.nullTranslator;const g=this.translator.load("jupyterlab"),y=this.contentFactory=e.contentFactory||D.defaultContentFactory,v=w.count++;n||(n=a.URLExt.join(o||"",`console-${v}-${u.UUID.uuid4()}`)),C=this._sessionContext=C||new r.SessionContext({sessionManager:l.sessions,specsManager:l.kernelspecs,path:n,name:i||g.__("Console %1",v),type:"console",kernelPreference:e.kernelPreference,setBusy:e.setBusy});const f=new h.RenderMimeRegistry.UrlResolver({session:C,contents:l.contents});t=t.clone({resolver:f}),this.console=y.createConsole({rendermime:t,sessionContext:C,mimeTypeService:s,contentFactory:y,modelFactory:_}),this.content.addWidget(this.console),C.initialize().then((async e=>{e&&await r.sessionContextDialogs.selectKernel(C),this._connected=new Date,this._updateTitlePanel()})),this.console.executed.connect(this._onExecuted,this),this._updateTitlePanel(),C.kernelChanged.connect(this._updateTitlePanel,this),C.propertyChanged.connect(this._updateTitlePanel,this),this.title.icon=d.consoleIcon,this.title.closable=!0,this.id=`console-${v}`}get sessionContext(){return this._sessionContext}dispose(){this.sessionContext.dispose(),this.console.dispose(),super.dispose()}onActivateRequest(e){const t=this.console.promptCell;t&&t.editor.focus()}onCloseRequest(e){super.onCloseRequest(e),this.dispose()}_onExecuted(e,t){this._executed=t,this._updateTitlePanel()}_updateTitlePanel(){w.updateTitle(this,this._connected,this._executed,this.translator)}}!function(e){class t extends f.ContentFactory{createConsole(e){return new f(e)}}e.ContentFactory=t,e.defaultContentFactory=new t,e.IContentFactory=new u.Token("@jupyterlab/console:IContentFactory")}(D||(D={})),function(e){e.count=1,e.updateTitle=function(e,t,s,n){const o=(n=n||c.nullTranslator).load("jupyterlab"),i=e.console.sessionContext.session;if(i){let n=o.__("Name: %1\n",i.name)+o.__("Directory: %1\n",a.PathExt.dirname(i.path))+o.__("Kernel: %1",e.console.sessionContext.kernelDisplayName);t&&(n+=o.__("\nConnected: %1",a.Time.format(t.toISOString()))),s&&(n+=o.__("\nLast Execution: %1")),e.title.label=i.name,e.title.caption=n}else e.title.label=o.__("Console"),e.title.caption=""}}(w||(w={}));const F=new u.Token("@jupyterlab/console:IConsoleTracker")}}]);