(self.webpackChunk_retrolab_lab_extension=self.webpackChunk_retrolab_lab_extension||[]).push([[974],{950:(t,e,n)=>{"use strict";n.d(e,{as:()=>h});var i=n(56),r=n(461),o=n(778),a=n(337),s=n(3),c=n(797),u=n(562);const l=new c.Token("@jupyterlab/application:ILayoutRestorer");var p;!function(t){function e(n){return n&&n.type?"tab-area"===n.type?{type:"tab-area",currentIndex:n.currentIndex,widgets:n.widgets.map((e=>t.nameProperty.get(e))).filter((t=>!!t))}:{type:"split-area",orientation:n.orientation,sizes:n.sizes,children:n.children.map(e).filter((t=>!!t))}:null}function n(t,e){if(!t)return null;const i=t.type||"unknown";if("unknown"===i||"tab-area"!==i&&"split-area"!==i)return console.warn(`Attempted to deserialize unknown type: ${i}`),null;if("tab-area"===i){const{currentIndex:n,widgets:i}=t,r={type:"tab-area",currentIndex:n||0,widgets:i&&i.map((t=>e.get(t))).filter((t=>!!t))||[]};return r.currentIndex>r.widgets.length-1&&(r.currentIndex=0),r}const{orientation:r,sizes:o,children:a}=t;return{type:"split-area",orientation:r,sizes:o||[],children:a&&a.map((t=>n(t,e))).filter((t=>!!t))||[]}}t.nameProperty=new u.AttachedProperty({name:"name",create:t=>""}),t.serializeMain=function(n){const i={dock:n&&n.dock&&e(n.dock.main)||null};if(n&&n.currentWidget){const e=t.nameProperty.get(n.currentWidget);e&&(i.current=e)}return i},t.deserializeMain=function(t,e){if(!t)return null;const i=t.current||null,r=t.dock||null;return{currentWidget:i&&e.has(i)&&e.get(i)||null,dock:r?{main:n(r,e)}:null}}}(p||(p={}));const d=new c.Token("@jupyterlab/application:IMimeDocumentTracker");function h(t){const e=[],n=new i.WidgetTracker({namespace:"application-mimedocuments"});return t.forEach((t=>{let i=t.default;t.hasOwnProperty("__esModule")||(i=t),Array.isArray(i)||(i=[i]),i.forEach((t=>{e.push(function(t,e){return{id:e.id,requires:[o.IRenderMimeRegistry,a.ITranslator],autoStart:!0,activate:(n,i,o)=>{if(void 0!==e.rank?i.addFactory(e.rendererFactory,e.rank):i.addFactory(e.rendererFactory),!e.documentWidgetFactoryOptions)return;const a=n.docRegistry;let c=[];c=Array.isArray(e.documentWidgetFactoryOptions)?e.documentWidgetFactoryOptions:[e.documentWidgetFactoryOptions],e.fileTypes&&e.fileTypes.forEach((t=>{t.icon&&(t=Object.assign(Object.assign({},t),{icon:s.LabIcon.resolve({icon:t.icon})})),n.docRegistry.addFileType(t)})),c.forEach((n=>{const s=n.toolbarFactory?t=>n.toolbarFactory(t.content.renderer):void 0,c=new r.MimeDocumentFactory({renderTimeout:e.renderTimeout,dataType:e.dataType,rendermime:i,modelName:n.modelName,name:n.name,primaryFileType:a.getFileType(n.primaryFileType),fileTypes:n.fileTypes,defaultFor:n.defaultFor,defaultRendered:n.defaultRendered,toolbarFactory:s,translator:o,factory:e.rendererFactory});a.addWidgetFactory(c),c.widgetCreated.connect(((e,n)=>{y.factoryNameProperty.set(n,c.name),n.context.pathChanged.connect((()=>{t.save(n)})),t.add(n)}))}))}}}(n,t))}))})),e.push({id:"@jupyterlab/application:mimedocument",optional:[l],provides:d,autoStart:!0,activate:(t,e)=>(e&&e.restore(n,{command:"docmanager:open",args:t=>({path:t.context.path,factory:y.factoryNameProperty.get(t)}),name:t=>`${t.context.path}:${y.factoryNameProperty.get(t)}`}),n)}),e}var y;!function(t){t.factoryNameProperty=new u.AttachedProperty({name:"factoryName",create:()=>{}})}(y||(y={}))},448:(t,e,n)=>{"use strict";n.d(e,{J:()=>a});var i=n(797),r=n(129),o=n(168);new i.Token("@jupyterlab/application:ILabStatus");class a{constructor(t){this._busyCount=0,this._dirtyCount=0,this._busySignal=new o.Signal(t),this._dirtySignal=new o.Signal(t)}get busySignal(){return this._busySignal}get dirtySignal(){return this._dirtySignal}get isBusy(){return this._busyCount>0}get isDirty(){return this._dirtyCount>0}setDirty(){const t=this.isDirty;return this._dirtyCount++,this.isDirty!==t&&this._dirtySignal.emit(this.isDirty),new r.DisposableDelegate((()=>{const t=this.isDirty;this._dirtyCount=Math.max(0,this._dirtyCount-1),this.isDirty!==t&&this._dirtySignal.emit(this.isDirty)}))}setBusy(){const t=this.isBusy;return this._busyCount++,this.isBusy!==t&&this._busySignal.emit(this.isBusy),new r.DisposableDelegate((()=>{const t=this.isBusy;this._busyCount--,this.isBusy!==t&&this._busySignal.emit(this.isBusy)}))}}},361:(t,e,n)=>{"use strict";n.d(e,{eD:()=>f});var i=n(797),r=n(168),o=function(t,e){return(o=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])})(t,e)};function a(t,e){function n(){this.constructor=t}o(t,e),t.prototype=null===e?Object.create(e):(n.prototype=e.prototype,new n)}var s=function(){return(s=Object.assign||function(t){for(var e,n=1,i=arguments.length;n<i;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)};function c(t,e,n,i){return new(n||(n=Promise))((function(r,o){function a(t){try{c(i.next(t))}catch(t){o(t)}}function s(t){try{c(i.throw(t))}catch(t){o(t)}}function c(t){t.done?r(t.value):new n((function(e){e(t.value)})).then(a,s)}c((i=i.apply(t,e||[])).next())}))}function u(t,e){var n,i,r,o,a={label:0,sent:function(){if(1&r[0])throw r[1];return r[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,i&&(r=2&o[0]?i.return:o[0]?i.throw||((r=i.return)&&r.call(i),0):i.next)&&!(r=r.call(i,o[1])).done)return r;switch(i=0,r&&(o=[2&o[0],r.value]),o[0]){case 0:case 1:r=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,i=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!((r=(r=a.trys).length>0&&r[r.length-1])||6!==o[0]&&2!==o[0])){a=0;continue}if(3===o[0]&&(!r||o[1]>r[0]&&o[1]<r[3])){a.label=o[1];break}if(6===o[0]&&a.label<r[1]){a.label=r[1],r=o;break}if(r&&a.label<r[2]){a.label=r[2],a.ops.push(o);break}r[2]&&a.ops.pop(),a.trys.pop();continue}o=e.call(t,a)}catch(t){o=[6,t],i=0}finally{n=r=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}}var l,p="function"==typeof requestAnimationFrame?requestAnimationFrame:setImmediate,d="function"==typeof cancelAnimationFrame?cancelAnimationFrame:clearImmediate,h=function(){function t(t){var e=this;this._disposed=new r.Signal(this),this._tick=new i.PromiseDelegate,this._ticked=new r.Signal(this),this._timeout=-1,this._factory=t.factory,this._standby=t.standby||l.DEFAULT_STANDBY,this._state=s(s({},l.DEFAULT_STATE),{timestamp:(new Date).getTime()});var n=t.frequency||{},o=Math.max(n.interval||0,n.max||0,l.DEFAULT_FREQUENCY.max);this.frequency=s(s(s({},l.DEFAULT_FREQUENCY),n),{max:o}),this.name=t.name||l.DEFAULT_NAME,"auto"in t&&!t.auto||p((function(){e.start()}))}return Object.defineProperty(t.prototype,"disposed",{get:function(){return this._disposed},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"frequency",{get:function(){return this._frequency},set:function(e){if(!this.isDisposed&&!i.JSONExt.deepEqual(e,this.frequency||{})){var n=e.backoff,r=e.interval,o=e.max;if(r=Math.round(r),o=Math.round(o),"number"==typeof n&&n<1)throw new Error("Poll backoff growth factor must be at least 1");if((r<0||r>o)&&r!==t.NEVER)throw new Error("Poll interval must be between 0 and max");if(o>t.MAX_INTERVAL&&o!==t.NEVER)throw new Error("Max interval must be less than "+t.MAX_INTERVAL);this._frequency={backoff:n,interval:r,max:o}}},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"isDisposed",{get:function(){return"disposed"===this.state.phase},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"standby",{get:function(){return this._standby},set:function(t){this.isDisposed||this.standby===t||(this._standby=t)},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"state",{get:function(){return this._state},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"tick",{get:function(){return this._tick.promise},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"ticked",{get:function(){return this._ticked},enumerable:!0,configurable:!0}),t.prototype.dispose=function(){this.isDisposed||(this._state=s(s({},l.DISPOSED_STATE),{timestamp:(new Date).getTime()}),this._tick.promise.catch((function(t){})),this._tick.reject(new Error("Poll ("+this.name+") is disposed.")),this._disposed.emit(void 0),r.Signal.clearData(this))},t.prototype.refresh=function(){return this.schedule({cancel:function(t){return"refreshed"===t.phase},interval:t.IMMEDIATE,phase:"refreshed"})},t.prototype.schedule=function(e){return void 0===e&&(e={}),c(this,void 0,void 0,(function(){var n,r,o,a,c,l=this;return u(this,(function(u){switch(u.label){case 0:return this.isDisposed||e.cancel&&e.cancel(this.state)?[2]:(n=this.state,r=this._tick,o=new i.PromiseDelegate,a=s({interval:this.frequency.interval,payload:null,phase:"standby",timestamp:(new Date).getTime()},e),this._state=a,this._tick=o,n.interval===t.IMMEDIATE?d(this._timeout):clearTimeout(this._timeout),this._ticked.emit(this.state),r.resolve(this),[4,r.promise]);case 1:return u.sent(),c=function(){l.isDisposed||l.tick!==o.promise||l._execute()},this._timeout=a.interval===t.IMMEDIATE?p(c):a.interval===t.NEVER?-1:setTimeout(c,a.interval),[2]}}))}))},t.prototype.start=function(){return this.schedule({cancel:function(t){var e=t.phase;return"constructed"!==e&&"standby"!==e&&"stopped"!==e},interval:t.IMMEDIATE,phase:"started"})},t.prototype.stop=function(){return this.schedule({cancel:function(t){return"stopped"===t.phase},interval:t.NEVER,phase:"stopped"})},t.prototype._execute=function(){var t=this,e="function"==typeof this.standby?this.standby():this.standby;if(e="never"!==e&&("when-hidden"===e?!("undefined"==typeof document||!document||!document.hidden):e))this.schedule();else{var n=this.tick;this._factory(this.state).then((function(e){t.isDisposed||t.tick!==n||t.schedule({payload:e,phase:"rejected"===t.state.phase?"reconnected":"resolved"})})).catch((function(e){t.isDisposed||t.tick!==n||t.schedule({interval:l.sleep(t.frequency,t.state),payload:e,phase:"rejected"})}))}},t}();!function(t){t.IMMEDIATE=0,t.MAX_INTERVAL=2147483647,t.NEVER=1/0}(h||(h={})),function(t){t.DEFAULT_BACKOFF=3,t.DEFAULT_FREQUENCY={backoff:!0,interval:1e3,max:3e4},t.DEFAULT_NAME="unknown",t.DEFAULT_STANDBY="when-hidden",t.DEFAULT_STATE={interval:h.NEVER,payload:null,phase:"constructed",timestamp:new Date(0).getTime()},t.DISPOSED_STATE={interval:h.NEVER,payload:null,phase:"disposed",timestamp:new Date(0).getTime()},t.sleep=function(e,n){var i=e.backoff,r=e.interval,o=e.max;if(r===h.NEVER)return r;var a=!0===i?t.DEFAULT_BACKOFF:!1===i?1:i,s=function(t,e){return t=Math.ceil(t),e=Math.floor(e),Math.floor(Math.random()*(e-t+1))+t}(r,n.interval*a);return Math.min(o,s)}}(l||(l={}));var y=function(){function t(t,e){var n=this;void 0===e&&(e=500),this.payload=null,this.limit=e,this.poll=new h({auto:!1,factory:function(){return c(n,void 0,void 0,(function(){return u(this,(function(e){switch(e.label){case 0:return[4,t()];case 1:return[2,e.sent()]}}))}))},frequency:{backoff:!1,interval:h.NEVER,max:h.NEVER},standby:"never"}),this.payload=new i.PromiseDelegate,this.poll.ticked.connect((function(t,e){var r=n.payload;return"resolved"===e.phase?(n.payload=new i.PromiseDelegate,void r.resolve(e.payload)):"rejected"===e.phase||"stopped"===e.phase?(n.payload=new i.PromiseDelegate,r.promise.catch((function(t){})),void r.reject(e.payload)):void 0}),this)}return Object.defineProperty(t.prototype,"isDisposed",{get:function(){return null===this.payload},enumerable:!0,configurable:!0}),t.prototype.dispose=function(){this.isDisposed||(this.payload=null,this.poll.dispose())},t.prototype.stop=function(){return c(this,void 0,void 0,(function(){return u(this,(function(t){return[2,this.poll.stop()]}))}))},t}(),f=(function(t){function e(){return null!==t&&t.apply(this,arguments)||this}a(e,t),e.prototype.invoke=function(){return this.poll.schedule({interval:this.limit,phase:"invoked"}),this.payload.promise}}(y),function(t){function e(e,n){var i=t.call(this,e,"number"==typeof n?n:n&&n.limit)||this,r="leading";return"number"!=typeof n&&(r="edge"in(n=n||{})?n.edge:r),i._interval="trailing"===r?i.limit:h.IMMEDIATE,i}return a(e,t),e.prototype.invoke=function(){return"invoked"!==this.poll.state.phase&&this.poll.schedule({interval:this._interval,phase:"invoked"}),this.payload.promise},e}(y));f||(f={})}}]);