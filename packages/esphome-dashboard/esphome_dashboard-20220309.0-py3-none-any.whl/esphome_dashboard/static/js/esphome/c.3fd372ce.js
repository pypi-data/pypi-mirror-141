import{_ as o,c as t,f as e,n as s,s as i,$ as r,Q as c}from"./index-92d154f2.js";import"./c.1cb51b24.js";import{o as n}from"./c.9706c602.js";import"./c.722f5049.js";import"./c.cb8aec9e.js";import"./c.ee1971f8.js";let a=class extends i{render(){return r`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){c(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){n(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],a.prototype,"configuration",void 0),o([t()],a.prototype,"target",void 0),o([e()],a.prototype,"_result",void 0),a=o([s("esphome-logs-dialog")],a);
