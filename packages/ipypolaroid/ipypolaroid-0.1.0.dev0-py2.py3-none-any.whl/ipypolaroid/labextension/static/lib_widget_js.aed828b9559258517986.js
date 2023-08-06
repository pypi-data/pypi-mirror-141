(self["webpackChunkjupyter_polaroid"] = self["webpackChunkjupyter_polaroid"] || []).push([["lib_widget_js"],{

/***/ "./lib/playback-control.js":
/*!*********************************!*\
  !*** ./lib/playback-control.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

/**
 * Implementation of a navigation slider.
 * @copyright CEA-LIST/DIASI/SIALV/LVA (2019)
 * @author CEA-LIST/DIASI/SIALV/LVA <pixano@cea.fr>
 * @license CECILL-C
 */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PlaybackControl = void 0;
//@ts-ignore
const lit_element_1 = __webpack_require__(/*! lit-element */ "webpack/sharing/consume/default/lit-element/lit-element");
__webpack_require__(/*! @material/mwc-slider/ */ "./node_modules/@material/mwc-slider/slider.js");
const style_1 = __webpack_require__(/*! ./style */ "./lib/style.js");
//@customElement('playback-control' as any)
class PlaybackControl extends lit_element_1.LitElement {
    constructor() {
        super();
        this.max = 0;
        this.current = 0;
        // utils boolean to force maximal slider fps
        // using keydown of: keySpeed fps
        this.enableNavigation = true;
        // slider time limit using keydown (ms), i.e fps: 1000/keyTime
        this.keyTime = 50;
        this.onNavigationKey = this.onNavigationKey.bind(this);
    }
    static get styles() {
        return [
            lit_element_1.css `
					:host {
						display: flex;
						overflow: hidden;
						width: 100%;
						height: 50px;
						z-index: 1;
						background: #f9f9f9;
						--mdc-theme-secondary: #9C27B0;
						-webkit-touch-callout: none; /* iOS Safari */
						-webkit-user-select: none; /* Safari */
						 -khtml-user-select: none; /* Konqueror HTML */
							 -moz-user-select: none; /* Old versions of Firefox */
								-ms-user-select: none; /* Internet Explorer/Edge */
										user-select: none; /* Non-prefixed version, currently
																					supported by Chrome, Opera and Firefox */
					}

					mwc-slider {
						align-items: center;
						width: -webkit-fill-available;
						width: 100%;
						margin-right: 15px;
					}
					.button {
						cursor: pointer;
						margin-right: 10px;
						margin-left: 10px;
						font-size: 23px;
						align-items: center;
						display: flex;
					}
					.button > svg {
						height: 18px;
					}
					.frameidx {
						color: #777777;
						font-size: 14px;
						-webkit-transform: scale(1.1, 1);
						width: 55px;
						align-items: center;
						display: flex;
						margin: auto;
					}
				`
        ];
    }
    onNavigationKey(evt) {
        if ((evt.key === 'ArrowRight' || evt.key === 'ArrowLeft') &&
            this.shadowRoot.activeElement === this.slider) {
            // stop bubbling
            evt.stopPropagation();
        }
        if (!this.enableNavigation) {
            return;
        }
        this.enableNavigation = false;
        // force navigation speed through arrow keys to under 10fps.
        setTimeout(() => {
            this.enableNavigation = true;
        }, this.keyTime);
        if (evt.key === 'ArrowRight') {
            this.setNext();
        }
        if (evt.key === 'ArrowLeft') {
            this.setBefore();
        }
    }
    connectedCallback() {
        super.connectedCallback();
        // set global window event listeners on connection
        // using useCapture so as to it is triggered first
        window.addEventListener('keydown', this.onNavigationKey);
    }
    disconnectedCallback() {
        // A classic global event listener is not be automatically destroyed by lit-element,
        // Removing it to prevent memory leaks and weird bugs.
        window.removeEventListener('keydown', this.onNavigationKey);
        super.disconnectedCallback();
    }
    onSliderInput() {
        //@ts-ignore
        this.set(this.slider.value);
    }
    setNext() {
        //@ts-ignore
        this.set(Math.min(this.slider.value + 1, this.max));
    }
    setBefore() {
        //@ts-ignore
        this.set(Math.max(this.slider.value - 1, 0));
    }
    /**
     * Set from inside, notify change
     * @param value
     */
    set(value) {
        this.current = value;
        this.dispatchEvent(new CustomEvent('update', { detail: this.current }));
    }
    get slider() {
        return this.shadowRoot.querySelector('mwc-slider');
    }
    updated(changedProps) {
        var _a;
        if (changedProps.has('current')) {
            try {
                //@ts-ignore
                (_a = this.slider) === null || _a === void 0 ? void 0 : _a.layout();
            }
            catch (_b) {
                console.warn("slider update failed");
            }
        }
    }
    /**
     * Render the element template.
     */
    render() {
        /**
         * `render` must return a lit-html `TemplateResult`.
         *
         * To create a `TemplateResult`, tag a JavaScript template literal
         * with the `html` helper function:
         */
        return lit_element_1.html `
					<p class="button" style="fill: ${this.current > 0 ? "black" : "#d0d0d0"}" @click=${this.setBefore}>${style_1.triLeft}</p>
					<p class="button" style="fill: ${this.current < this.max ? "black" : "#d0d0d0"}" @click=${this.setNext}>${style_1.triRight}</p>
					<p class="frameidx">${this.current}/${this.max}</p>
					<mwc-slider @input=${this.onSliderInput}
											discrete
											value=${this.current}
											max="${this.max}"
											step="1"></mwc-slider>
				`;
    }
}
exports.PlaybackControl = PlaybackControl;
PlaybackControl.properties = {
    max: { type: Number },
    current: { type: Number },
};
customElements.define('playback-control', PlaybackControl);
//# sourceMappingURL=playback-control.js.map

/***/ }),

/***/ "./lib/style.js":
/*!**********************!*\
  !*** ./lib/style.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.genericStyles = exports.demoStyles = exports.track = exports.paintBrush = exports.subtractCircle = exports.replaceCircle = exports.uniteCircle = exports.parallelogram = exports.square = exports.polygonLasso = exports.polygon = exports.freeDrawing = exports.eraser = exports.dot = exports.borderOuter = exports.triLeft = exports.triRight = exports.pointer = exports.polyline = exports.circle = exports.mergeTracks = exports.cutTrack = exports.switchTrack = exports.decrease = exports.increase = exports.upload = exports.swap = exports.opacity = exports.zoomOut = exports.zoomIn = exports.filter = exports.balloon2 = exports.balloon = exports.rectify = exports.lock = exports.brush = exports.union = exports.subtract = exports.magicSelect = exports.createPencil = exports.fullscreen = void 0;
const lit_element_1 = __webpack_require__(/*! lit-element */ "webpack/sharing/consume/default/lit-element/lit-element");
exports.fullscreen = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M21.414 18.586l2.586-2.586v8h-8l2.586-2.586-5.172-5.172 2.828-2.828 5.172 5.172zm-13.656-8l2.828-2.828-5.172-5.172 2.586-2.586h-8v8l2.586-2.586 5.172 5.172zm10.828-8l-2.586-2.586h8v8l-2.586-2.586-5.172 5.172-2.828-2.828 5.172-5.172zm-8 13.656l-2.828-2.828-5.172 5.172-2.586-2.586v8h8l-2.586-2.586 5.172-5.172z"/></svg>`;
exports.createPencil = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-3.994 12.964l3.106 3.105-4.112.931 1.006-4.036zm9.994-3.764l-5.84 5.921-3.202-3.202 5.841-5.919 3.201 3.2z"/></svg>`;
exports.magicSelect = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M7.828 5.016l-2.828 2.828 16.172 16.156 2.828-2.828-16.172-16.156zm2.121 6.363l-3.535-3.535 1.414-1.414 3.535 3.536-1.414 1.413zm-3.191-9.004l-.911-1.796c.982-.368 2.042-.579 3.153-.579l.422.021-.318 1.984-.104-.005c-.785 0-1.537.136-2.242.375zm6.434 1.033c-.631-.475-1.34-.851-2.11-1.091l.316-1.983c1.193.33 2.287.894 3.226 1.647l-1.432 1.427zm1.412 1.416l1.432-1.427c.751.941 1.312 2.037 1.638 3.23l-1.984.312c-.239-.772-.613-1.482-1.086-2.115zm1.392 4.092l1.984-.311.02.395c0 1.005-.18 1.965-.485 2.866l-1.633-1.632c.073-.401.118-.812.118-1.234l-.004-.084zm-12.601 4.258l-1.432 1.427c-.75-.941-1.311-2.036-1.637-3.23l1.984-.311c.239.772.612 1.482 1.085 2.114zm1.411 1.417c.632.475 1.341.852 2.111 1.092l-.317 1.984c-1.193-.33-2.287-.894-3.227-1.648l1.433-1.428zm7.048 2.928c-.898.302-1.854.481-2.854.481l-.426-.021.318-1.984.108.005c.417 0 .823-.043 1.219-.115l1.635 1.634zm-8.559-12.56l-1.801-.921c.674-1.017 1.549-1.888 2.568-2.559l.914 1.802c-.651.46-1.219 1.028-1.681 1.678zm-1.291 4.126l-1.984.311-.02-.396c0-1.122.215-2.19.589-3.181l1.794.918c-.244.711-.383 1.471-.383 2.263l.004.085z"/></svg>`;
exports.subtract = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 16V8h11v5h5v11H0zm17-1v-2h3v3h-3zm4 0v-2h3v3h-3zm0-5V8h3v3h-3zM8 5V4h2v3H8zm13 0V4h3v3h-3zM8 1V0h2v3H8zm4 0V0h3v3h-3zm5 0V0h2v3h-2zm4 0V0h3v3h-3zm0 0"/></svg>`;
exports.union = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 16V8h8V0h16v16h-8v8H0zm0 0"/></svg>`;
exports.brush = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M17.831 7.672c1.096-1.096 2.875-1.865 3.688-3.106.892-1.362.508-3.192-.851-4.085-1.362-.892-3.187-.508-4.081.854-.842 1.286-.801 3.322-1.433 4.779-.817 1.882-3.553 2.116-6.698.474-1.727 3.352-4.075 6.949-6.456 9.874l2.263 1.484c1.018-.174 2.279-1.059 2.792-2.03-.04 1.167-.478 2.2-1.337 2.983l4.275 2.797c.546-.544 1.054-.976 1.616-1.345-.319.643-.532 1.324-.63 1.99l2.532 1.659c1.5-2.884 4.416-7.343 6.455-9.874-2.82-2.272-3.657-4.936-2.135-6.454zm1.762-5.545c.454.296.58.908.281 1.36-.294.457-.905.582-1.356.286-.456-.297-.582-.906-.284-1.36.295-.455.905-.583 1.359-.286zm-3.959 15.037l-8.225-5.386 1.616-2.469 8.221 5.387-1.612 2.468z"/></svg>`;
exports.lock = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 9v-3c0-2.206 1.794-4 4-4s4 1.794 4 4v3h2v-3c0-3.313-2.687-6-6-6s-6 2.687-6 6v3h2zm.746 2h2.831l-8.577 8.787v-2.9l5.746-5.887zm12.254 1.562v-1.562h-1.37l-12.69 13h2.894l11.166-11.438zm-6.844-1.562l-11.156 11.431v1.569h1.361l12.689-13h-2.894zm6.844 7.13v-2.927l-8.586 8.797h2.858l5.728-5.87zm-3.149 5.87h3.149v-3.226l-3.149 3.226zm-11.685-13h-3.166v3.244l3.166-3.244z"/></svg>`;
exports.rectify = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g id="surface1">
											<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 2.875 20.433594 L 11.667969 11.644531 L 20.457031 2.855469 C 21.03125 2.964844 21.046875 3.027344 21.117188 3.511719 L 3.535156 21.09375 C 2.894531 21.070312 2.871094 21.097656 2.875 20.433594 Z M 2.875 20.433594 "/>
											<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 7.144531 8.375 C 6.257812 8.375 5.542969 9.089844 5.542969 9.972656 C 5.542969 10.859375 6.257812 11.574219 7.144531 11.574219 C 8.027344 11.574219 8.742188 10.859375 8.742188 9.972656 C 8.742188 9.089844 8.027344 8.375 7.144531 8.375 Z M 7.128906 9.277344 C 7.515625 9.277344 7.828125 9.589844 7.828125 9.972656 C 7.828125 10.359375 7.515625 10.671875 7.128906 10.671875 C 6.746094 10.671875 6.433594 10.359375 6.433594 9.972656 C 6.433594 9.589844 6.746094 9.277344 7.128906 9.277344 Z M 7.128906 9.277344 "/>
											<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 13.851562 2.628906 C 12.96875 2.628906 12.25 3.347656 12.25 4.230469 C 12.25 5.113281 12.96875 5.828125 13.851562 5.828125 C 14.734375 5.828125 15.449219 5.113281 15.449219 4.230469 C 15.449219 3.347656 14.734375 2.628906 13.851562 2.628906 Z M 13.839844 3.53125 C 14.222656 3.53125 14.535156 3.84375 14.535156 4.230469 C 14.535156 4.617188 14.222656 4.929688 13.839844 4.929688 C 13.453125 4.929688 13.140625 4.617188 13.140625 4.230469 C 13.140625 3.84375 13.453125 3.53125 13.839844 3.53125 Z M 13.839844 3.53125 "/>
											<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 17.164062 10.613281 C 16.28125 10.613281 15.5625 11.328125 15.5625 12.214844 C 15.5625 13.097656 16.28125 13.8125 17.164062 13.8125 C 18.046875 13.8125 18.765625 13.097656 18.765625 12.214844 C 18.765625 11.328125 18.046875 10.613281 17.164062 10.613281 Z M 17.152344 11.515625 C 17.535156 11.515625 17.847656 11.828125 17.847656 12.214844 C 17.847656 12.597656 17.535156 12.910156 17.152344 12.910156 C 16.765625 12.910156 16.453125 12.597656 16.453125 12.214844 C 16.453125 11.828125 16.765625 11.515625 17.152344 11.515625 Z M 17.152344 11.515625 "/>
											<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 14.476562 17.039062 C 13.59375 17.039062 12.878906 17.753906 12.878906 18.636719 C 12.878906 19.519531 13.59375 20.238281 14.476562 20.238281 C 15.363281 20.238281 16.078125 19.519531 16.078125 18.636719 C 16.078125 17.753906 15.363281 17.039062 14.476562 17.039062 Z M 14.464844 17.9375 C 14.851562 17.9375 15.164062 18.253906 15.164062 18.636719 C 15.164062 19.023438 14.851562 19.335938 14.464844 19.335938 C 14.082031 19.335938 13.765625 19.023438 13.765625 18.636719 C 13.765625 18.253906 14.082031 17.9375 14.464844 17.9375 Z M 14.464844 17.9375 "/>
											</g></svg>`;
exports.balloon = lit_element_1.html `<svg width="24" height="24"><path d="M8.96 23.8c-.17-.13-.53-1.83-1.45-6.87a6.72 6.72 0 00-.34-1.4c-.06-.03-.28-.02-.5.03-.63.15-1.07.12-1.07-.07 0-.1.24-.56.53-1.03.3-.48.53-.9.53-.93 0-.04-.22-.13-.49-.2-1.63-.41-3.71-2-4.8-3.65a6.1 6.1 0 01-1.04-3.3A5.75 5.75 0 014.43.31c.88-.3 2.5-.27 3.43.05.96.32 1.89.96 2.53 1.73a6.34 6.34 0 011.52 4.27c-.01 1.32-.22 2.1-.9 3.5a8.72 8.72 0 01-2.23 2.9c-.26.2-.47.41-.47.46 0 .05.36.37.8.7.95.75 1.02.99.31 1.12-.9.16-.95.18-.95.4 0 .5 1.08 6 1.2 6.13.11.1.25-.04.76-.8.34-.51 1.06-1.54 1.6-2.29.97-1.31.99-1.36.8-1.55-.1-.1-.35-.28-.53-.39-.36-.21-.44-.53-.15-.61l.83-.19c1.03-.2 1.02-.2.68-.91a7.4 7.4 0 01-.7-3.07c-.1-2.03.37-3.53 1.52-4.8a5.3 5.3 0 014.05-1.92 5.13 5.13 0 015.05 6.42 6.03 6.03 0 01-3.26 4.03 7.5 7.5 0 01-3.96.88l-1.2-.03v.37c0 .2.05.63.1.95.12.86-.02.95-.73.46-.48-.33-.58-.37-.7-.24-.08.09-.7.97-1.4 1.96-1.38 2-2.55 3.61-2.84 3.9-.22.22-.38.23-.63.05zm6.62-14.51c.11-.06.3-.3.41-.52a3.53 3.53 0 011.68-1.43c.27-.1.76-.17 1.09-.17.64 0 .85-.12.85-.5 0-.47-.35-.67-1.17-.67-1.37 0-2.6.7-3.4 1.94-.47.73-.51.94-.2 1.25.23.23.44.26.74.1zM2.8 7.95c.32-.12.39-.53.2-1.18-.37-1.28.02-2.82.89-3.51.39-.31.45-.68.17-.99-.65-.71-2.14.67-2.52 2.35a4.04 4.04 0 000 2.22c.22 1.02.61 1.36 1.26 1.11z"/></svg>`;
exports.balloon2 = lit_element_1.html `<svg width="24" height="24"><path d="M6.13.11c-.63 0-1.26.06-1.7.2a5.75 5.75 0 00-4.1 6.06 6.1 6.1 0 001.04 3.3c1.09 1.67 3.17 3.25 4.8 3.66.27.07.5.16.5.2 0 .03-.25.45-.54.93-.29.47-.53.94-.53 1.03 0 .19.44.22 1.08.07.21-.05.43-.06.49-.02.05.03.2.66.34 1.39.92 5.04 1.28 6.74 1.45 6.87.25.18.41.17.63-.05.29-.29 1.46-1.9 2.85-3.9.69-1 1.31-1.87 1.39-1.96.12-.13.22-.1.7.24.7.5.85.4.72-.46-.04-.32-.09-.75-.1-.95v-.37l1.2.03a7.5 7.5 0 003.97-.88 6.03 6.03 0 003.26-4.03 5.14 5.14 0 00-5.05-6.42 5.3 5.3 0 00-4.05 1.91c-1.15 1.28-1.63 2.78-1.52 4.81a7.4 7.4 0 00.7 3.07c.34.71.35.7-.68.91l-.83.19c-.29.08-.21.4.15.61.18.1.42.28.53.4.19.18.16.23-.8 1.54-.54.75-1.26 1.78-1.6 2.29-.5.76-.65.9-.76.8a66.9 66.9 0 01-1.2-6.13c0-.22.04-.24.95-.4.71-.13.64-.37-.32-1.11-.43-.34-.8-.66-.8-.7 0-.06.22-.26.48-.46a8.72 8.72 0 002.24-2.9c.67-1.4.88-2.2.89-3.5a6.34 6.34 0 00-1.52-4.28A5.83 5.83 0 007.86.37 5.98 5.98 0 006.12.1zm-.65.96c2.38-.12 4.6 1.86 5.12 4.57.57 2.91-1.01 5.62-3.53 6.04-2.51.42-5.01-1.6-5.58-4.52a7 7 0 01.04-2.54c.04-.2.1-.39.18-.58l.04-.1a4.32 4.32 0 013.73-2.87zM18.44 6c.82 0 1.17.2 1.17.67 0 .38-.2.5-.85.5-.33 0-.82.08-1.1.17-.6.2-1.39.88-1.67 1.43-.11.23-.3.46-.4.52-.31.16-.52.13-.76-.1-.3-.3-.26-.52.2-1.25A4.02 4.02 0 0118.45 6z"/></svg>`;
exports.filter = lit_element_1.html `<svg width="24" height="24"><path d="M11.94 1.9c-4.76 0-9.27 3.7-10.27 8.42a10.2 10.2 0 002.91 9.64 10.54 10.54 0 004.9 2.9c3.14.75 6.74-.14 9.36-2.32 1.12-.93 2.5-2.74 2.32-3.04-.06-.1-1.9-1.22-4.09-2.51a49.02 49.02 0 01-3.98-2.48c0-.07 1.8-1.2 3.99-2.48a67.75 67.75 0 004.09-2.51c.16-.26-1.14-2.03-2.14-2.9a12.12 12.12 0 00-7.1-2.72zm-.06 3.5h2.58V8h-2.58V5.4z"/><path d="M20 10.44h3.71v3.71H20z"/></svg>`;
exports.zoomIn = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M13 10h-3v3h-2v-3h-3v-2h3v-3h2v3h3v2zm8.172 14l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>`;
exports.zoomOut = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M13 10h-8v-2h8v2zm8.172 14l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>`;
exports.opacity = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="20"><g fill="none" fill-rule="evenodd"><path d="M20-2H-4v24h24V-2zm0 0H-4v24h24V-2zM-4 22h24V-2H-4v24z"/><path fill="#1D1D1D" d="M13.7 6L8 .3 2.3 6a8 8 0 0011.4 11.3 8 8 0 000-11.3zM2 12c0-2 .6-3.3 1.8-4.4L8 3.3l4.2 4.4A5.6 5.6 0 0114 12H2z"/></g></svg>`;
exports.swap = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M486 102H205V51a26 26 0 00-44-18L8 187a26 26 0 0018 43h460c15 0 26-11 26-25v-77c0-14-11-26-26-26zm0 103H26L179 51v77h307v77zM510 297c-4-9-13-15-24-15H26c-15 0-26 11-26 25v77c0 14 11 26 26 26h281v51a26 26 0 0044 18l154-154c7-7 9-18 5-28zM333 461v-77H26v-77h460L333 461z"/></svg>`;
exports.upload = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path d="M17 12v5H3v-5H1v5a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5z"/><path d="M15 7l-5-6-5 6h4v8h2V7h4z"/></svg>`;
exports.increase = lit_element_1.html `<svg enable-background="new 0 0 24 24" version="1.1" viewBox="0 0 24 24" xml:space="preserve" xmlns="http://www.w3.org/2000/svg"><path d="m16 7h-8c-0.6 0-1 0.4-1 1v8c0 0.6 0.4 1 1 1h8c0.6 0 1-0.4 1-1v-8c0-0.6-0.4-1-1-1zm0 9h-8v-8h8v8z"/><polygon points="5.2 6.7 6.8 5.2 3.9 2.3 6 0 0 0 0 6 2.3 3.9"/><polygon points="17.7 0 19.9 2.3 17 5.2 18.5 6.7 21.6 3.8 24 6 24 0"/><polygon points="18.8 17 17.2 18.5 20.1 21.6 18 24 24 24 24 17.7 21.7 19.9"/><polygon points="5.5 17 2.4 19.9 0 17.8 0 24 6.3 24 4.1 21.6 7 18.6"/></svg>`;
exports.decrease = lit_element_1.html `<svg enable-background="new 0 0 24 24" version="1.1" viewBox="0 0 24 24" xml:space="preserve" xmlns="http://www.w3.org/2000/svg"><path d="M17,8c0-0.6-0.4-1-1-1H8C7.4,7,7,7.4,7,8v8c0,0.6,0.4,1,1,1h8c0.6,0,1-0.4,1-1V8z M16,16H8V8h8V16z"/><polygon points="0.8 7 7 7 7 0.7 4.6 2.8 1.6 0 0 1.5 2.9 4.6"/><polygon points="21.2 4.6 24 1.6 22.5 0 19.4 2.9 17 0.8 17 7 23.3 7"/><polygon points="23.2 17 17 17 17 23.3 19.4 21.2 22.4 24 24 22.5 21.1 19.4"/><polygon points="2.8 19.4 0 22.4 1.5 24 4.6 21.1 7 23.3 7 17 0.7 17"/></svg>`;
exports.switchTrack = lit_element_1.html `<svg width="24pt" height="24pt" version="1.1" viewBox="0 0 24 24"><path d="m17.043 2.9453v1.1211l-0.83203 0.24609c-1.9492 0.58594-3.7656 2.3047-7.0312 6.6602-3.7773 5.0312-4.3828 5.5-7.0781 5.5h-1.8164v3.2656h1.9023c3.8672 0 5.1367-0.89062 9.5234-6.6719 2.4258-3.1953 3.4219-4.3359 4.4648-5.0898 0.84766-0.61328 0.86719-0.59766 0.86719 0.62891 0 0.80859 0.042969 1.0625 0.17578 1.0117 0.46484-0.18359 6.5625-3.7734 6.5938-3.8828 0.039062-0.12109-6.168-3.7734-6.5664-3.8633-0.16406-0.035156-0.20312 0.17578-0.20312 1.0742m-16.758 2.8047v1.6328h1.7812c2.3867 0 2.9375 0.30078 4.9102 2.6406 1.2148 1.4414 0.99219 1.4531 2.1445-0.10938l0.95312-1.293-0.45703-0.57812c-2.3672-3.0078-4.0938-3.9258-7.3711-3.9258h-1.9609v1.6328m11.719 8.1172c-1.1641 1.543-1.2031 1.3281 0.60156 3.1484 1.5938 1.6094 2.7266 2.3438 3.8945 2.5312l0.54297 0.085937v1.1992c0 0.96875 0.039062 1.1914 0.20312 1.1562 0.39844-0.09375 6.6055-3.7422 6.5664-3.8633-0.03125-0.11328-6.1289-3.6992-6.5938-3.8828-0.13281-0.054688-0.17578 0.20312-0.17578 1.0078 0 0.59375-0.054688 1.082-0.12109 1.082-0.38672 0-2.875-2.3594-3.5078-3.3281-0.34375-0.52344-0.38672-0.49609-1.4102 0.86328" fill-rule="evenodd"/></svg>`;
exports.cutTrack = lit_element_1.html `<svg viewBox="0 0 24 24"><path d="M 10.201 12.087 L 10.181 21.325 L 13.541 21.325 L 13.577 13.396 L 16.332 13.407 L 19.092 13.423 L 19.116 15.181 L 19.145 16.938 L 21.57 14.477 L 24 12.011 L 21.57 9.582 L 19.145 7.147 L 19.129 8.814 L 19.116 10.476 L 13.577 10.476 L 13.541 3 L 10.181 3 L 10.201 12.086 M 2.441 9.593 L 0 12.035 L 2.441 14.481 L 4.884 16.922 L 4.911 15.172 L 4.935 13.423 L 7.126 13.384 L 7.126 10.432 L 4.911 10.476 L 4.899 8.813 L 4.884 7.147 L 2.441 9.593" fill-rule="evenodd"/></svg>`;
exports.mergeTracks = lit_element_1.html `<svg width="24pt" height="24pt" version="1.1" viewBox="0 0 24 24"><path d="m0 12.074v10.441h3.3164v-8.957h3.5117v3.2891l2.4141-2.4102 2.4102-2.4141-2.3984-2.3984-2.3984-2.4023-0.027344 1.7227-0.023437 1.7188-1.7461 0.011719-1.7422 0.015625v-9.0586h-3.3164v10.441m20.684-6.0625v4.3789h-3.5117v-3.2891l-2.4141 2.4102-2.4102 2.4141 2.3984 2.3984 2.3984 2.4023 0.027344-1.7188 0.023437-1.7227 3.4883-0.023437v9.2539h3.3164v-20.883h-3.3164v4.3789" fill-rule="evenodd"/></svg>`;
exports.circle = lit_element_1.html `<svg version="1.1" viewBox="0 0 24 24"><g><path d="m11.754 0.19922c-2.2109 0.039062-4.4062 0.72266-6.25 1.9492-2.4219 1.6016-4.1602 4.0078-4.9023 6.793-0.27344 1.0195-0.39453 1.9531-0.39453 3.0586 0 0.74609 0.039063 1.2539 0.15234 1.9375 0.61719 3.75 3.0273 6.9883 6.457 8.6641 1.2539 0.61328 2.5352 0.98438 3.9258 1.1328 0.77734 0.085937 1.7891 0.082031 2.5977-0.007813 3.0078-0.33594 5.7969-1.8477 7.75-4.1992 1.4648-1.7695 2.3867-3.9258 2.6367-6.1875 0.09375-0.84375 0.09375-1.8359 0-2.6719-0.47266-4.2109-3.1914-7.8594-7.1055-9.5312-1.5273-0.65234-3.168-0.96484-4.8672-0.9375zm0.77734 0.375c-0.042969 0.003906-0.12109 0.003906-0.16797 0-0.050781-0.003907-0.015625-0.003907 0.078125-0.003907s0.13281 0 0.089844 0.003907zm0.32812 0.019531c-0.027344 0.003906-0.078125 0.003906-0.11328 0s-0.011719-0.007812 0.050781-0.007812 0.089844 0.003906 0.0625 0.007812zm0.16016 0.019531c-0.015625 0.003907-0.035156 0.003907-0.046875 0-0.015625-0.003906-0.003906-0.007812 0.019532-0.007812 0.027343 0 0.039062 0.003906 0.027343 0.007812zm-5.8086 0.99219c0.003906 0.007812-0.13672 0.085937-0.3125 0.17188-0.22266 0.10547-0.3125 0.14453-0.30859 0.12109 0.003906-0.027344 0.56641-0.32422 0.59766-0.31641 0.011719 0.003907 0.023438 0.011719 0.023438 0.023438zm5.7266 0.26172c2.1211 0.19922 4.0781 1.0273 5.6914 2.4102 0.28906 0.24609 0.84766 0.80469 1.0938 1.0938 1.2422 1.4531 2.0469 3.1992 2.3359 5.0742 0.085937 0.5625 0.11328 0.91797 0.11328 1.5547s-0.027344 0.98828-0.11328 1.5547c-0.28516 1.8594-1.1016 3.6328-2.3359 5.0742-0.24609 0.28906-0.80469 0.84766-1.0938 1.0938-1.4414 1.2344-3.2148 2.0508-5.0742 2.3359-0.56641 0.085937-0.91797 0.11328-1.5547 0.11328s-0.99219-0.027344-1.5547-0.11328c-1.875-0.28906-3.6211-1.0938-5.0742-2.3359-0.28906-0.24609-0.84766-0.80469-1.0938-1.0938-1.3867-1.6172-2.2031-3.5469-2.4141-5.7109-0.042969-0.44922-0.042969-1.3867 0-1.8359 0.21094-2.1406 0.98828-4 2.3633-5.6523 0.24219-0.29297 0.91016-0.96094 1.2031-1.2031 1.7656-1.4688 3.832-2.2812 6.1016-2.3984 0.27734-0.011719 1.1016 0.007813 1.4062 0.039063zm-6.3906 0.070312c0.015625-0.007812 0.015625-0.003906 0.007813 0.007812-0.019532 0.035157-0.046876 0.027344-0.046876-0.011718 0-0.015625 0.007813-0.019532 0.011719-0.007813 0.003907 0.011719 0.019531 0.019531 0.027344 0.011719zm11.453 0.32422c0 0.003906-0.015625 0-0.039062-0.011719-0.019532-0.011719-0.035157-0.023438-0.035157-0.03125 0-0.003906 0.015625 0 0.035157 0.011719 0.023437 0.011719 0.039062 0.023437 0.039062 0.03125zm0.14844 0.09375c0 0.003906-0.015626 0-0.035157-0.011719s-0.039062-0.023438-0.039062-0.03125c0-0.003906 0.019531 0 0.039062 0.011719s0.035157 0.023437 0.035157 0.03125zm0.41406 0.28125c0 0.003906-0.023438-0.007813-0.054688-0.03125-0.03125-0.023438-0.058593-0.042969-0.058593-0.046875 0-0.007813 0.027343 0.007812 0.058593 0.027344 0.03125 0.023437 0.054688 0.046874 0.054688 0.050781zm-15.918 2.8086c0 0.003907-0.015625 0.019532-0.03125 0.03125-0.03125 0.023438-0.035156 0.023438-0.007812-0.007812 0.023437-0.03125 0.039062-0.039062 0.039062-0.023438zm-0.30078 0.44141c-0.011719 0.019531-0.023438 0.039062-0.03125 0.039062-0.003906 0 0-0.019531 0.011719-0.039062s0.023437-0.035157 0.03125-0.035157c0.003906 0 0 0.015626-0.011719 0.035157zm19.715 0.64844c0.003906 0.015625 0.003906 0.023438-0.007813 0.019532-0.011719-0.007813-0.019531-0.019532-0.019531-0.03125 0-0.027344 0.011719-0.019532 0.027344 0.011718zm0.17969 0.34766c0.050781 0.10547 0.09375 0.19531 0.089844 0.19531-0.003906 0.003906-0.050781-0.082031-0.10547-0.1875-0.050781-0.10938-0.09375-0.19531-0.089844-0.19531 0.007813 0 0.054688 0.082032 0.10547 0.1875zm-21.625 4.1367c-0.003906 0.019531-0.007812 0.003907-0.007812-0.03125 0-0.035156 0.003906-0.050781 0.007812-0.035156 0.003907 0.019531 0.003907 0.050781 0 0.066406zm-0.019531 0.23438c-0.003906 0.035156-0.007812 0.011719-0.007812-0.050781s0.003906-0.089844 0.007812-0.0625 0.003906 0.078125 0 0.11328zm-0.019531 0.39453c-0.003907 0.042968-0.003907 0.003906-0.003907-0.089844s0-0.125 0.003907-0.078125c0.003906 0.050781 0.003906 0.125 0 0.16797zm22.859 0.89844c-0.003906 0.054687-0.007813 0.015625-0.007813-0.085937 0-0.10547 0.003907-0.14844 0.007813-0.10156 0.003906 0.050781 0.003906 0.13281 0 0.1875zm0.015625 0.23438c-0.003907 0.03125-0.007813 0.011719-0.007813-0.039062 0-0.054688 0.003906-0.078126 0.007813-0.054688 0.003906 0.023438 0.003906 0.066406 0 0.09375zm-0.023438 0.089844c0.007813 0.12891 0.003907 0.16406-0.007812 0.11328-0.015625-0.074219-0.027344-0.32422-0.011719-0.30859 0.003906 0.003907 0.011719 0.09375 0.019531 0.19531zm0 0.20312c0.011719 0.007812 0.011719 0.011719-0.011719 0.011719-0.023437 0-0.03125-0.011719-0.03125-0.070313 0.003907-0.0625 0.003907-0.0625 0.011719-0.011719 0.003907 0.027344 0.019531 0.0625 0.03125 0.070313zm-21.645 4.0391c0.050781 0.10547 0.089844 0.19141 0.085938 0.19141-0.011719 0-0.19922-0.36719-0.19922-0.38281 0-0.027344 0.015625 0 0.11328 0.19141zm0.18359 0.37109c-0.003906 0.003906-0.015625-0.003906-0.023438-0.023437-0.011718-0.023438-0.007812-0.027344 0.011719-0.011719 0.011719 0.015625 0.015625 0.03125 0.011719 0.035156zm19.484 0.97266c0 0.003907-0.015625 0.019531-0.03125 0.03125-0.03125 0.027344-0.03125 0.023438-0.007813-0.007812 0.023438-0.027344 0.039063-0.039063 0.039063-0.023438zm-15.973 2.9297c0.023438 0.03125 0.023438 0.035156-0.003906 0.007812-0.035156-0.023437-0.042968-0.039062-0.027344-0.039062 0.003907 0 0.019532 0.015625 0.03125 0.03125zm0.44922 0.30078c0 0.003906-0.019531 0-0.039062-0.011719s-0.035157-0.023437-0.035157-0.03125c0-0.003906 0.015626 0 0.035157 0.011719s0.039062 0.023438 0.039062 0.03125zm0.14844 0.09375c0 0.003906-0.015625 0-0.035157-0.011719-0.023437-0.011719-0.039062-0.023437-0.039062-0.03125 0-0.003906 0.015625 0 0.039062 0.011719 0.019532 0.011719 0.035157 0.023438 0.035157 0.03125zm11.195 0.37109c0 0.011718-0.33203 0.17969-0.35156 0.17578-0.011719 0 0.32812-0.17969 0.34766-0.18359 0 0 0.003906 0.003907 0.003906 0.007813zm-6.2383 1.2422c-0.015625 0.003907-0.035156 0.003907-0.046875 0-0.015625-0.003906-0.003906-0.007812 0.023437-0.007812 0.023438 0 0.035157 0.003906 0.023438 0.007812zm0.23438 0.019531c-0.027344 0.003907-0.078125 0.003907-0.11328 0-0.035156-0.003906-0.011719-0.007812 0.050781-0.007812s0.089844 0.003906 0.0625 0.007812zm0.38281 0.019532c-0.042969 0.003906-0.11719 0.003906-0.16797 0-0.046875-0.003906-0.011719-0.007813 0.078125-0.007813 0.09375 0 0.13281 0.003907 0.089844 0.007813z"/><path d="m6.7305 1.8203c-0.074219 0.039063-0.13281 0.070313-0.125 0.074219 0.019531 0 0.27734-0.12891 0.27734-0.14062 0-0.015625 0.003907-0.015625-0.15234 0.066406z"/></g></svg>`;
exports.polyline = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" version="1" viewBox="0 0 24 24" enable-background="new 0 0 24 24"><path d="M 20 2 C 18.970152 2 18.141273 2.7807107 18.03125 3.78125 L 14.5625 4.78125 C 14.19654 4.3112749 13.641793 4 13 4 C 11.895431 4 11 4.8954305 11 6 C 11 7.1045695 11.895431 8 13 8 C 13.052792 8 13.104488 8.0040159 13.15625 8 L 16.53125 14.6875 C 16.440877 14.788724 16.349735 14.881869 16.28125 15 L 11.9375 14.46875 C 11.705723 13.620636 10.921625 13 10 13 C 8.8954305 13 8 13.895431 8 15 C 8 15.217462 8.0295736 15.428987 8.09375 15.625 L 4.96875 18.25 C 4.6825722 18.092012 4.3500149 18 4 18 C 2.8954305 18 2 18.895431 2 20 C 2 21.104569 2.8954305 22 4 22 C 5.1045695 22 6 21.104569 6 20 C 6 19.782538 5.9704264 19.571013 5.90625 19.375 L 9.03125 16.75 C 9.3174278 16.907988 9.6499851 17 10 17 C 10.754554 17 11.409413 16.585686 11.75 15.96875 L 16.0625 16.53125 C 16.294277 17.379364 17.078375 18 18 18 C 19.104569 18 20 17.104569 20 16 C 20 14.895431 19.104569 14 18 14 C 17.947208 14 17.895512 13.995984 17.84375 14 L 14.5 7.3125 C 14.761761 7.0130168 14.922918 6.6355416 14.96875 6.21875 L 18.4375 5.21875 C 18.80346 5.6887251 19.358207 6 20 6 C 21.104569 6 22 5.1045695 22 4 C 22 2.8954305 21.104569 2 20 2 z"/></svg>`;
exports.pointer = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 30 37.5" xml:space="preserve"><g transform="translate(-30 -320)"><polygon xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" points="55.287,336.168 38,321 38,344 44.299,339.402 48.763,349.428 52.221,347.889 47.757,337.863	"/></g></svg>`;
exports.triRight = lit_element_1.html `<svg width="24pt" height="24pt" viewBox="0 0 24 24"><polygon points="0 0, 24 12, 0 24"/></svg>`;
exports.triLeft = lit_element_1.html `<svg width="24pt" height="24pt" viewBox="0 0 24 24"><polygon points="0 12, 24 0, 24 24"/></svg>`;
exports.borderOuter = lit_element_1.html `<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M13 7h-2v2h2V7zm0 4h-2v2h2v-2zm4 0h-2v2h2v-2zM3 3v18h18V3H3zm16 16H5V5h14v14zm-6-4h-2v2h2v-2zm-4-4H7v2h2v-2z"/></svg>`;
exports.dot = lit_element_1.html `<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="20"/></svg>`;
exports.eraser = lit_element_1.html `<svg version="1.1" x="0px" y="0px" viewBox="0 0 328.498 328.498" style="enable-background:new 0 0 328.498 328.498;"><g><g><g><path	d="M167.2,173.663L167.2,173.663l-57.276-57.276L13.01,213.301c-4.013,4.013-4.013,10.52,0,14.533l68.923,68.923c1.927,1.927,4.541,3.01,7.267,3.01h68.979c6.528,0,12.789-2.593,17.405-7.21l55.255-55.255l0,0L167.2,173.663z"/><path	d="M158.179,309.768H89.2c-5.416,0-10.508-2.109-14.338-5.938L5.939,234.906C2.109,231.076,0,225.984,0,220.568c0-5.417,2.11-10.509,5.94-14.339l103.984-103.984l135.057,135.058l-62.325,62.327C176.118,306.167,167.426,309.768,158.179,309.768z M109.925,130.529l-89.843,89.844c-0.031,0.031-0.082,0.081-0.082,0.195s0.052,0.165,0.082,0.195l68.923,68.923c0.052,0.053,0.121,0.081,0.195,0.081h68.979c3.904,0,7.575-1.52,10.335-4.28l48.185-48.185L109.925,130.529z"/></g><g><path	d="M230.84,251.445L95.782,116.388l91.719-91.719c3.829-3.829,8.921-5.938,14.338-5.938c5.416,0,10.508,2.108,14.338,5.938l106.382,106.382c3.83,3.83,5.939,8.922,5.939,14.338c0,5.417-2.11,10.509-5.94,14.339L230.84,251.445z M124.067,116.388L230.84,223.161l77.576-77.577c0.031-0.03,0.081-0.081,0.082-0.195c0-0.114-0.052-0.165-0.082-0.195L202.034,38.812c-0.03-0.03-0.081-0.081-0.195-0.081h-0.001c-0.113,0-0.163,0.05-0.193,0.08L124.067,116.388z"/></g></g><g><rect x="88.934" y="289.758" width="148.906" height="20"/></g><g><rect x="256.249" y="289.758" width="32" height="20"/></g></g></svg>`;
exports.freeDrawing = lit_element_1.html `<svg version="1.1" x="0px" y="0px" viewBox="0 0 283.093 283.093" style="enable-background:new 0 0 283.093 283.093;" xml:space="preserve"><g><path d="M271.315,54.522L218.989,2.196c-2.93-2.928-7.678-2.928-10.607,0L78.274,132.303c-1.049,1.05-1.764,2.388-2.053,3.843l-12.964,65.29c-0.487,2.456,0.282,4.994,2.053,6.765c1.421,1.42,3.334,2.196,5.304,2.196c0.485,0,0.975-0.047,1.461-0.144l65.29-12.964c1.456-0.289,2.793-1.004,3.843-2.053L271.315,65.129C274.244,62.2,274.244,57.452,271.315,54.522z M83.182,178.114l6.776-34.127l39.566,39.566l-34.127,6.776L83.182,178.114z"/><path d="M205.912,227.066c-71.729-30.029-118.425,19.633-132.371,27.175c-17.827,9.641-42.941,20.97-48.779,1.358c-3.522-11.832,15.521-24.479,28.131-28.42c9.2-2.876,5.271-17.358-3.988-14.465c-19.582,6.121-42.948,22.616-38.851,45.839c3.044,17.256,24.67,32.995,66.368,11.114c30.308-15.902,50.897-48.84,114.733-31.783c20.969,5.602,37.92,19.27,45.178,40.057c3.168,9.07,17.662,5.169,14.465-3.988C243.062,251.799,227.411,236.067,205.912,227.066z"/></g></svg>`;
exports.polygon = lit_element_1.html `<svg version="1.1" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve"><g><path d="M213.3,0c-23.6,0-42.7,19.1-42.7,42.7V44l-108,68c-6-3.2-12.8-5.3-20-5.3C19.1,106.7,0,125.8,0,149.3c0,15.8,8.6,29.3,21.3,36.7v246.7C8.6,440.1,0,453.6,0,469.3C0,492.9,19.1,512,42.7,512c15.8,0,29.2-8.6,36.7-21.3h268c7.4,12.8,20.9,21.3,36.7,21.3c23.6,0,42.7-19.1,42.7-42.7c0-8.5-2.3-16.7-6.7-23.3l52-104.7c22.3-1.4,40-20,40-42.7c0-20.8-14.9-38.3-34.7-42l-40.7-122c6.8-7.6,11.3-17.1,11.3-28c0-23.6-19.1-42.7-42.7-42.7c-10.9,0-20.4,4.6-28,11.3L255.3,34C251.3,14.6,233.9,0,213.3,0z M241.3,74.7l122,40c3.3,17.2,16.8,30.8,34,34L438,270c-6.9,7.6-11.3,17.6-11.3,28.7c0,8.8,2.8,17.2,7.3,24l-52.7,104c-14.7,0.9-27,9.3-34,21.3h-268c-3.8-6.4-8.9-11.6-15.3-15.3V186c12.8-7.4,21.3-20.9,21.3-36.7V148l108-68c6,3.2,12.8,5.3,20,5.3C224.1,85.3,233.8,81.3,241.3,74.7z"/></g></svg>`;
exports.polygonLasso = lit_element_1.html `<svg version="1.1" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve"><g><path d="M172.2,394.7v7.4c11.2,0,22.3,2.8,28.9,7.4c3.7,2.8,6.5,4.7,7.4,7.4c1.9,2.8,2.8,5.6,2.8,8.4s-0.9,5.6-2.8,8.4c-2.8,3.7-7.4,8.4-14,11.2c-6.5,2.8-14,4.7-23.3,4.7c-11.2,0-22.3-2.8-28.9-7.4c-3.7-2.8-6.5-4.7-7.4-7.4c-1.9-2.8-2.8-5.6-2.8-8.4s0.9-5.6,2.8-8.4c2.8-3.7,7.4-8.4,14-11.2c6.5-2.8,14-4.7,23.3-4.7V394.7v-8.4c-14,0-27.9,3.7-37.2,10.2c-4.7,3.7-9.3,7.4-12.1,12.1c-2.8,4.7-4.7,10.2-4.7,16.8c0,5.6,1.9,11.2,4.7,16.8c4.7,7.4,12.1,13,20.5,16.8c8.4,3.7,18.6,5.6,29.8,6.5c14,0,27.9-3.7,37.2-10.2c4.7-3.7,9.3-7.4,12.1-12.1s4.7-10.2,4.7-16.8c0-5.6-1.9-11.2-4.7-16.8c-4.7-7.4-12.1-13-20.5-16.8s-18.6-5.6-29.8-6.5V394.7z"/><path d="M200.1,456.1l0.9-2.8L200.1,456.1L200.1,456.1l0.9-2.8L200.1,456.1c0,0,2.8,1.9,5.6,5.6s5.6,9.3,5.6,18.6c0,4.7-0.9,8.4-1.9,10.2c-1.9,2.8-2.8,3.7-4.7,4.7l-1.9,0.9l0,0v2.8v-2.8l0,0v2.8v-2.8V512c0.9,0,6.5,0,12.1-4.7c2.8-1.9,5.6-5.6,7.4-10.2c1.9-4.7,2.8-10.2,2.8-16.8c0-14-4.7-23.3-9.3-29.8c-4.7-6.5-10.2-8.4-10.2-9.3L200.1,456.1L200.1,456.1z"/><polygon points="187.1,391 60.5,114.5 324,159.2 462.7,35.4 462.7,325.8 209.5,402.2 214.1,417 478.5,337 478.5,0 319.3,142.4 33.5,94 173.1,397.5"/></g></svg>`;
exports.square = lit_element_1.html `<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="m482 90h15c8.285156 0 15-6.714844 15-15v-60c0-8.285156-6.714844-15-15-15h-60c-8.285156 0-15 6.714844-15 15v15h-332v-15c0-8.285156-6.714844-15-15-15h-60c-8.285156 0-15 6.714844-15 15v60c0 8.285156 6.714844 15 15 15h15v331c0 .339844.027344.667969.050781 1h-15.050781c-8.285156 0-15 6.714844-15 15v60c0 8.285156 6.714844 15 15 15h60c8.285156 0 15-6.714844 15-15v-15h331c.335938 0 .667969-.027344 1-.050781v15.050781c0 8.285156 6.714844 15 15 15h60c8.285156 0 15-6.714844 15-15v-60c0-8.285156-6.714844-15-15-15h-15.050781c.023437-.332031.050781-.660156.050781-1zm-30-60h30v30h-30zm-422 0h30v30h-30zm30 452h-30v-30h30zm422 0h-30v-30h30zm-45-60c-8.285156 0-15 6.714844-15 15v15.050781c-.332031-.023437-.660156-.050781-1-.050781h-331v-15c0-8.285156-6.714844-15-15-15h-15.050781c.023437-.332031.050781-.660156.050781-1v-331h15c8.285156 0 15-6.714844 15-15v-15h332v15c0 8.285156 6.714844 15 15 15h15v331c0 .339844.027344.667969.050781 1zm0 0"/></svg>`;
exports.parallelogram = lit_element_1.html `<svg xml:space="preserve" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 1000 1000" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd"><path class="fil0" d="M932 201l-263 598 -601 0c87,-199 175,-399 263,-598l601 0zm-72 47l-499 0 -221 504 499 0 221 -504z"/></g></svg>`;
exports.uniteCircle = lit_element_1.html `<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAACgAgMAAAD2oY++AAAAAXNSR0IB2cksfwAAAAxQTFRFAAAAAAAAAAAAAAAANek3lgAAAAR0Uk5T/gAicCKdMBIAAALkSURBVHic7dm7kdswEAZgiBwFDOiLVIJKYHCOVIIDS/ZYDpj7giuBTbAEZw6uBDShEhg4uxJMgC8A++9ihzMeJ97sZr45ErtLvGSuXHx7N+bp5/qn4dzdmjHKIQdv3o2yz8BXM0ctw7tZYxDh2wY/SPBmgugF+BLCZwHaEJY8vJsoBha2MaxY2MWw4OAXk0TPwO8pbBj4msKagTaFJYa31PmXBPArhWcIWworCMlY/GgAJGPxo6EQjMWNhkJSFxcnAMGg3bApBIN2w6YQDNoNm8IOwQJAkB2XHwqRM4ZCmB1jHgR+xvBEIEzjmEgCyXcwRUPgJwyPBLYYVgTCwoyl2Q8vGB4I7DAs9sEf71iNUYbwF8ti+CK4MVZ3l90G35SQaQYKrRIybUhh7g0XyHwpFLZaaJUwl+wVKp5spN4KYmoKOMkimC3f0rjMB0WhzUP/cSlecfpc8w0xw1YB/ZTSKaCfpKwCumlP0WLTRKoZi5+amakzDjfZK+oyLR+dwvkFSfMP3RKnKaBfNJkVKA63DCuacVrYVdlxWwVVdtzm46JwfjvTKaDfIFkFdFsuVRrdJk7VZP0INfl2u2Gj+rIc1BSmcVBTmN7BNu+mDbsCTkcARamnQ8Ul6+ZjSh7OB58uC3slXA5nNgcHJVwPkBm4HUkzbjvkyhEcm+W4/of/DFrJlX8VdhIs9sCLBA97oDil1AFsJVjtgeJEegygODU3ARQn+3MAxeXjFEBxQXoEUFzi+gBKi2bQPPIyXETwwsNDBIVi1xEUSnOMoFCaJoJCxk8RFBLZR1CYA64x7DhXJJDNT51ANj/HBLIdeU4g22iPBHL9E/bOBDsMCwJbDCsCuesTApki9gRyl0YUMvdVFMKWbABkbukoRJmMs7jAlsIKQnBsHiDE96cIkmenT14gabUHA+H1MoRJY5xZiO7KMYzK2AgQXPwzkP6UwMDtqukZuOiicr68+ohcfKPprsOefkN3/QNz7BGg/vj3xQAAAABJRU5ErkJggg==" alt="" class="autoscale gsicon">`;
exports.replaceCircle = lit_element_1.html `<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAACgAgMAAAD2oY++AAAAAXNSR0IB2cksfwAAAAxQTFRFAAAAAAAAAAAAAAAANek3lgAAAAR0Uk5T/wDROaqwHD0AAAOiSURBVHic3dixbtswEABQQp4cI5+RJYHRyZ9iy4Oh6BM8Gh1S/YT3jEGKIpPHovoJ7RqD7gaKAGkrkkeK5N3xBKNZyikRnsTjSSaPVGuu3f98uv169v8q1j2qoV2dJVi+KtPuOgF+VtC+5eF942BxzsJfyrdPOVg2Iyy6DDyooC0zsNdPenn/86afvOBhpd13/deDlicW6p5f7J9vrm8SDj1fdTCsR+ibgnrMLs8682bcFKx8TuCuEwP3LiUu4GsG9jBQ//wFDYfOFvF9OhACVlHPpu8TCQ9Rz+5GAtbBmCGUOQnbOEQd5IyCwwOW8ZWD7gLDTRKiCfJIwJ1SXXylVGpFwKGj9JIOBsN9OhY9mmsC9ubVonsxbNVNemk75AfDJh20HnaBYalzkbQhYx2Cm+QFmpsbdUSwwtkx4SC4w9nRmVghuNWfStpqdYPgAadRJ3KJ4D79duBuBGucbxMPAVcY7gjY0nBGwCOGmwR+eX66bSbA33ZC/kHBIoAPMHHbKTRqZQjtUhUvVyR8Haf3uxyswoXglIF9CNMPKIDRA/Ejh0vUA9EjSw/DNS1Y13DXB5W0JQP7FC5oWKUuGY6HqOekbw9Rz0nf7qNIx4zG7T4zIsQ4SAeJEOMg3U+BCDEOEn5cVIhxkPBzJUOMgoQJgAwxChKmFDLEKEiYpMgQVThP2mmvpF24LtmJlBlLMBqYmrcc9NMaTPZ7DvoZFZaPnoN+2LAgNRz0w7ZLHDvocdh20dzw8Oizo5fhHQ9XkB27sLPZ8fmBUoHNjs8PFB81D+duLKacaXk4cy/QFEgNDwsXoi656N8BwM6GaIq4TL4h41AWZvJtM+4KTfZr1O20HkvXzIsxr8YXw5kXY16NL6+Z36pty6Bgz7xBHdy4BcjDYFNR5+CVdrBNyUII1MBWcm4rJUK3OZOg3+41AvQbSAGOW9I8DDa5WVh4J8H1R8J8uwT++xj/K9jm4OxDYZ2D80ugMPdcAIVpb4TSROqhNDV7KE72DorLh4PyguRgw7uw4JuwaDrY8nAWwZqH8wjKpQJAufgAKJczACcUSBZOKLksnFDEAew5uEigXGgClEtXgHIxDHBCeW3hhIIdYE/DBYLypgKgvE0BKG98AMpbKQfFzZmD4nbPQXED6aC4JfVQ2uR6KG2bPZQ24iMUtvYjFA4LRigcPwRQONAIzkj7/ANHmD10CWH2GCeCuYOhCOaOmmIIh1cFcXiVQHMc9vxOuvVfbbWqTsr5YWMAAAAASUVORK5CYII=" alt="" class="autoscale gsicon">`;
exports.subtractCircle = lit_element_1.html `<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAACgAgMAAAD2oY++AAAAAXNSR0IB2cksfwAAAAxQTFRFAAAAAAAAAAAAAAAANek3lgAAAAR0Uk5TAf/hiBGx/K0AAAP7SURBVHicxZgxdtswDIZl63nQ4HTyEXQEDVnyfIQMpu2XeNCcZsgRfAkeIUOm5gB5r7qEjtChW+cOdSWRFAHih6z2vb5isqlPIgCCAMEsU+XX29NX/WmUb6aTx+vcdzPI52vcjfHyPs3lNoD7ZhK8NaM8T4I2gvspbm2IvEyAJQWPOpcbJo0KFhys5808NbfloGr3jUlEW50qBU/zVNSVtCmoKLlMOWPOECwkWM+zRbNmI8HdPFsUa3LJ4bhYIHA7z2hsNjAamy0WsBe0iC0CD/O8g/2DOGMkB92IHAlip5ezANcYlFkA+ht5fDZYYVAuzWwQriBaww0GZYzPAvOfb08WgywqPilQCk5xFMxfJzgaZ7dTHAGVqJGg4mgBXvlgDPFq+PdwuVwBXZH8yJS9FacuAteBd1NgX+5dGbUGOsqD/dbzhbkDY7EWYD9z7X623c4E2+EwOjEo0YPAIg/aWOgHUGp5GL3deHDT73WZLnYhHsY9sRmyq1jQXVBxzATl8FPki6NXMR5aqgEUHjp5FeNurJyf0rlP3ov1CBbjGJPw9pmAx+AIAbZ0R6y9gYmSL26hScJYet8mSp7dLFHF7rV9BpRs3FBUsU/2DVDSOYQVB+tfY0runTYssbR+lVoKHtwIy5Kluc/cRESOTqmagpX3AbPm5LSmtnRAjD3m70VSlsJ/FpPb4Qu8IuYGmN2/ukprrPU6E7O9d5KMv/EDZBF3bvyeg2EBVtzoboaag2FJiX9qp9KWgyFIyLnmTI2k1jz6F6gtS1ndSzcUHeljXhwsqlEpastaHlVuxmjx8u5AWQ+te7ahKoZdlyr5mEWPO2AFanbvwecYkbXXXIJDAv4xgo0H7wU4TLr/WNGZu7Fagqjx2cAOiMRicDMGQXPWwvMraPcwCBrIVmkEREtqFVA0uSrYtc0ssKzezeX/GJxoJHN2WJ4N/kdjdIcnO3k2qAVFFotYALcauPg7EG+FQXgSmQ3C7eqEZxuYAJzwbINSCnyEkhScDKU9L1x9lEi9cIeA1BykZSBI9kF4vIDy4SWpQKAgKZ8QJS7IIlFKFM0gRWKmKMNBVonjRGHXHoijQtSJT5UePkaxifLpcSZInt5OpAckfVy5pSlE49/iiKyEkSU2uxVuq7DZVkxUQGuWUnUwhF/P4Z1KCdzbIiUtMLEESi7RNAVQEo3Bt9EsvPFx0hV25NxSXKqs8e3SrRgu8UXvMr0p7o8UQEXWQIYpcNiXyQOr3WKSJhf8pTrRA4479DQQJI2401C9g4+tfZbdGXVmelngOP1e3R0qHy6X13hOhpI0bWcVnH1Xzj858cE/uPiPF0MPzSQ4XjV1B+sr4sjrnLsO+6LM+xuKVUGMXWFsHAAAAABJRU5ErkJggg==" alt="" class="autoscale gsicon">`;
exports.paintBrush = lit_element_1.html `<svg width="24pt" height="24pt" viewBox="0 0 24 24" version="1.1"><path style="stroke:none;fill-rule:nonzero;fill-opacity:1;" d="M 23.410156 2.175781 C 23.03125 1.800781 22.535156 1.589844 22.003906 1.582031 C 21.996094 1.582031 21.988281 1.582031 21.980469 1.582031 C 21.457031 1.582031 20.960938 1.78125 20.585938 2.144531 L 9.324219 12.914062 C 10.527344 13.21875 11.558594 13.992188 12.230469 15.125 C 12.4375 15.46875 12.597656 15.835938 12.71875 16.210938 L 23.441406 5 C 23.800781 4.621094 24 4.125 24 3.605469 C 24 3.066406 23.789062 2.558594 23.410156 2.175781 Z M 23.410156 2.175781 "/><path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 8.277344 14.171875 C 8.222656 14.167969 8.164062 14.167969 8.109375 14.167969 C 7.15625 14.167969 6.214844 14.5 5.445312 15.050781 C 4.519531 15.71875 4.148438 16.675781 3.46875 17.550781 C 2.617188 18.644531 1.304688 19.179688 0 19.542969 C 0.757812 21.546875 3.578125 22.371094 5.425781 22.414062 C 5.492188 22.414062 5.558594 22.417969 5.625 22.417969 C 7.71875 22.417969 10.183594 21.636719 11.191406 19.578125 C 12.300781 17.320312 10.933594 14.28125 8.277344 14.171875 Z M 8.277344 14.171875 "/></svg>`;
exports.track = lit_element_1.html `<svg width="24pt" height="24pt" viewBox="0 0 24 24" version="1.1"><g><path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 11.054688 0.09375 C 10.960938 0.144531 10.832031 0.261719 10.773438 0.359375 C 10.671875 0.523438 10.664062 0.59375 10.648438 1.335938 L 10.632812 2.136719 L 10.179688 2.210938 C 6.21875 2.898438 2.898438 6.21875 2.210938 10.179688 L 2.136719 10.632812 L 1.335938 10.648438 C 0.59375 10.664062 0.523438 10.671875 0.359375 10.777344 C 0.046875 10.96875 0 11.132812 0 12 C 0 12.867188 0.046875 13.03125 0.359375 13.222656 C 0.523438 13.328125 0.59375 13.335938 1.335938 13.351562 L 2.136719 13.367188 L 2.210938 13.820312 C 2.898438 17.78125 6.21875 21.101562 10.179688 21.789062 L 10.632812 21.863281 L 10.648438 22.664062 C 10.664062 23.40625 10.671875 23.476562 10.777344 23.640625 C 10.96875 23.953125 11.132812 24 12 24 C 12.867188 24 13.03125 23.953125 13.222656 23.640625 C 13.328125 23.476562 13.335938 23.40625 13.351562 22.664062 L 13.367188 21.863281 L 13.820312 21.789062 C 17.78125 21.101562 21.101562 17.78125 21.789062 13.820312 L 21.863281 13.367188 L 22.664062 13.351562 C 23.40625 13.335938 23.476562 13.328125 23.640625 13.222656 C 23.953125 13.03125 24 12.867188 24 12 C 24 11.132812 23.953125 10.96875 23.640625 10.777344 C 23.476562 10.671875 23.40625 10.664062 22.664062 10.648438 L 21.863281 10.632812 L 21.789062 10.179688 C 21.101562 6.21875 17.78125 2.898438 13.820312 2.210938 L 13.367188 2.136719 L 13.351562 1.335938 C 13.335938 0.59375 13.328125 0.523438 13.222656 0.359375 C 13.03125 0.046875 12.867188 0 11.992188 0 C 11.328125 0.00390625 11.203125 0.015625 11.054688 0.09375 Z M 10.640625 5.492188 C 10.640625 6.167969 10.695312 6.382812 10.925781 6.59375 C 11.113281 6.769531 11.277344 6.796875 12 6.796875 C 12.722656 6.796875 12.886719 6.769531 13.074219 6.59375 C 13.304688 6.382812 13.359375 6.167969 13.359375 5.492188 C 13.359375 5.15625 13.375 4.875 13.386719 4.875 C 13.476562 4.875 14.210938 5.085938 14.527344 5.203125 C 16.472656 5.921875 18.078125 7.527344 18.796875 9.472656 C 18.914062 9.789062 19.125 10.523438 19.125 10.613281 C 19.125 10.625 18.84375 10.640625 18.507812 10.640625 C 17.832031 10.640625 17.617188 10.695312 17.40625 10.925781 C 17.230469 11.113281 17.203125 11.277344 17.203125 12 C 17.203125 12.722656 17.230469 12.886719 17.40625 13.074219 C 17.617188 13.304688 17.832031 13.359375 18.507812 13.359375 C 18.84375 13.359375 19.125 13.375 19.125 13.386719 C 19.125 13.402344 19.082031 13.578125 19.03125 13.78125 C 18.375 16.355469 16.355469 18.375 13.785156 19.03125 C 13.578125 19.082031 13.402344 19.125 13.386719 19.125 C 13.375 19.125 13.359375 18.84375 13.359375 18.5 C 13.359375 17.832031 13.304688 17.617188 13.074219 17.40625 C 12.886719 17.230469 12.722656 17.203125 12 17.203125 C 11.277344 17.203125 11.113281 17.230469 10.925781 17.40625 C 10.695312 17.617188 10.640625 17.832031 10.640625 18.5 C 10.640625 18.84375 10.625 19.125 10.613281 19.125 C 10.597656 19.125 10.421875 19.082031 10.214844 19.03125 C 9.449219 18.835938 8.738281 18.523438 8.085938 18.101562 C 6.773438 17.257812 5.699219 15.917969 5.183594 14.492188 C 5.082031 14.203125 4.875 13.46875 4.875 13.386719 C 4.875 13.375 5.15625 13.359375 5.5 13.359375 C 6.167969 13.359375 6.382812 13.304688 6.59375 13.074219 C 6.769531 12.886719 6.796875 12.722656 6.796875 12 C 6.796875 11.277344 6.769531 11.113281 6.59375 10.925781 C 6.382812 10.695312 6.167969 10.640625 5.5 10.640625 C 5.15625 10.640625 4.875 10.625 4.875 10.613281 C 4.875 10.53125 5.082031 9.796875 5.183594 9.507812 C 5.875 7.59375 7.496094 5.949219 9.40625 5.222656 C 9.722656 5.105469 10.46875 4.882812 10.585938 4.878906 C 10.625 4.875 10.640625 5.03125 10.640625 5.492188 Z M 10.640625 5.492188 "/><path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 11.382812 10.46875 C 9.867188 11.105469 10.121094 13.332031 11.738281 13.585938 C 12.617188 13.726562 13.421875 13.167969 13.597656 12.296875 C 13.75 11.574219 13.367188 10.820312 12.703125 10.503906 C 12.328125 10.332031 11.75 10.3125 11.382812 10.46875 Z M 11.382812 10.46875 "/></g></svg>`;
exports.demoStyles = lit_element_1.css `
	main {
		display: flex;
		height: 100%;
		width: 100%;
		--mdc-theme-secondary: #79005D;
	}
	.right-panel {
		position: absolute;
		display: flex;
		flex-direction: column;
		right: 0px;
		top: 0px;
		bottom: 0px;
		display: flex;
		margin: auto;
		width: auto;
	}
	.icon {
			-webkit-touch-callout: none;
			-webkit-user-select: none;
			-khtml-user-select: none;
			-moz-user-select: none;
			-ms-user-select: none;
			user-select: none;
			right: 0px;
			margin-bottom: 10px;
			margin-left: 10px;
			margin-right: 10px;
			display: flex;
			margin-top: 10px;
			height: 24px;
			width: 24px;
			z-index: 1;
			color: black;
			background: white;
			fill: var(--mdc-theme-secondary);
			padding: 10px;
			border-radius: 50%;
			cursor: pointer;
			font-size: 18px;
			-webkit-transition: all 0.5s ease;
				-moz-transition: all 0.5s ease;
					-o-transition: all 0.5s ease;
					-ms-transition: all 0.5s ease;
							transition: all 0.5s ease;
	}
	.icon:hover {
		background: var(--mdc-theme-secondary);
		fill: white;
	}
	svg {
		overflow: visible;
		width: inherit;
	}
	.icons {
		height: calc(100% - 44px);
		padding-top: 60px;
		flex-wrap: wrap;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}`;
exports.genericStyles = lit_element_1.css `
	#container {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
	}
	[name="slider"] > div {
		height: 50px;
		flex: 0 0 50px;
		display: flex;
	}
	playback-control {
		background: #f9f9f9;
		color: var(--font-color);
	}
`;
//# sourceMappingURL=style.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) nicolas allezard
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.CarouselView = exports.CarouselModel = exports.PolaroidView = exports.PolaroidModel = void 0;
// Copyright (c) nicolas allezard
// Distributed under the terms of the Modified BSD License.
//@ts-ignore
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
__webpack_require__(/*! @material/mwc-dialog */ "webpack/sharing/consume/default/@material/mwc-dialog/@material/mwc-dialog");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
//@ts-ignore
const lit_element_1 = __webpack_require__(/*! lit-element */ "webpack/sharing/consume/default/lit-element/lit-element");
__webpack_require__(/*! ./playback-control */ "./lib/playback-control.js");
//@ts-ignore
const lock = lit_element_1.html `<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 9v-3c0-2.206 1.794-4 4-4s4 1.794 4 4v3h2v-3c0-3.313-2.687-6-6-6s-6 2.687-6 6v3h2zm.746 2h2.831l-8.577 8.787v-2.9l5.746-5.887zm12.254 1.562v-1.562h-1.37l-12.69 13h2.894l11.166-11.438zm-6.844-1.562l-11.156 11.431v1.569h1.361l12.689-13h-2.894zm6.844 7.13v-2.927l-8.586 8.797h2.858l5.728-5.87zm-3.149 5.87h3.149v-3.226l-3.149 3.226zm-11.685-13h-3.166v3.244l3.166-3.244z"/></svg>`;
//@ts-ignore
const fastforward = lit_element_1.html `<svg   version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M292.418,134.248c-8.331-8.331-21.839-8.331-30.17,0c-8.331,8.331-8.331,21.839,0,30.17L353.83,256l-91.582,91.582
		c-8.331,8.331-8.331,21.839,0,30.17c8.331,8.331,21.839,8.331,30.17,0l106.667-106.667c8.331-8.331,8.331-21.839,0-30.17
		L292.418,134.248z"/>
	  <path d="M271.085,240.915L164.418,134.248c-8.331-8.331-21.839-8.331-30.17,0s-8.331,21.839,0,30.17L225.83,256l-91.582,91.582
		c-8.331,8.331-8.331,21.839,0,30.17c8.331,8.331,21.839,8.331,30.17,0l106.667-106.667
		C279.416,262.754,279.416,249.246,271.085,240.915z"/>
</svg>`;
//@ts-ignore
const left_arrow = lit_element_1.html `<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"

   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M309.416,152.144l-149.333,85.333c-14.332,8.19-14.332,28.855,0,37.045l149.333,85.333
		c14.222,8.127,31.918-2.142,31.918-18.523V170.667C341.333,154.286,323.638,144.017,309.416,152.144z M298.667,304.572
		L213.665,256l85.001-48.572V304.572z"/>
	  </svg>`;
//@ts-ignore
const right_arrow = lit_element_1.html `<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">

	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M351.918,237.477l-149.333-85.333c-14.222-8.127-31.918,2.142-31.918,18.523v170.667
		c0,16.38,17.696,26.649,31.918,18.523l149.333-85.333C366.25,266.333,366.25,245.667,351.918,237.477z M213.333,304.572v-97.144
		L298.335,256L213.333,304.572z"/>
 </svg>`;
//@ts-ignore
const rewind = lit_element_1.html `<svg  version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	  viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">

	  <path d="M256,0C114.618,0,0,114.618,0,256s114.618,256,256,256s256-114.618,256-256S397.382,0,256,0z M256,469.333
		c-117.818,0-213.333-95.515-213.333-213.333S138.182,42.667,256,42.667S469.333,138.182,469.333,256S373.818,469.333,256,469.333
		z"/>
	  <path d="M158.17,256l91.582-91.582c8.331-8.331,8.331-21.839,0-30.17c-8.331-8.331-21.839-8.331-30.17,0L112.915,240.915
		c-8.331,8.331-8.331,21.839,0,30.17l106.667,106.667c8.331,8.331,21.839,8.331,30.17,0c8.331-8.331,8.331-21.839,0-30.17
		L158.17,256z"/>
	  <path d="M377.752,134.248c-8.331-8.331-21.839-8.331-30.17,0L240.915,240.915c-8.331,8.331-8.331,21.839,0,30.17l106.667,106.667
		c8.331,8.331,21.839,8.331,30.17,0c8.331-8.331,8.331-21.839,0-30.17L286.17,256l91.582-91.582
		C386.083,156.087,386.083,142.58,377.752,134.248z"/>
 </svg>`;
//@ts-ignore
const freeDrawing = lit_element_1.html `<svg class="freeDrawing" version="1.1" x="0px" y="0px" viewBox="0 0 283.093 283.093" style="enable-background:new 0 0 283.093 283.093;" xml:space="preserve"><g><path d="M271.315,54.522L218.989,2.196c-2.93-2.928-7.678-2.928-10.607,0L78.274,132.303c-1.049,1.05-1.764,2.388-2.053,3.843l-12.964,65.29c-0.487,2.456,0.282,4.994,2.053,6.765c1.421,1.42,3.334,2.196,5.304,2.196c0.485,0,0.975-0.047,1.461-0.144l65.29-12.964c1.456-0.289,2.793-1.004,3.843-2.053L271.315,65.129C274.244,62.2,274.244,57.452,271.315,54.522z M83.182,178.114l6.776-34.127l39.566,39.566l-34.127,6.776L83.182,178.114z"/><path d="M205.912,227.066c-71.729-30.029-118.425,19.633-132.371,27.175c-17.827,9.641-42.941,20.97-48.779,1.358c-3.522-11.832,15.521-24.479,28.131-28.42c9.2-2.876,5.271-17.358-3.988-14.465c-19.582,6.121-42.948,22.616-38.851,45.839c3.044,17.256,24.67,32.995,66.368,11.114c30.308-15.902,50.897-48.84,114.733-31.783c20.969,5.602,37.92,19.27,45.178,40.057c3.168,9.07,17.662,5.169,14.465-3.988C243.062,251.799,227.411,236.067,205.912,227.066z"/></g></svg>`;
//box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
//@customElement('my-element' as any)
class litPolaroid extends lit_element_1.LitElement {
    constructor() {
        super();
        this.image_data = '';
        this.caption = '';
        this.width = 200;
        this.height = 220;
        this.jupyter_widget = null;
        this.carousel = null;
        this.target = "unselected";
    }
    get caption_element() {
        return this.shadowRoot.querySelector("#image_caption");
    }
    _handleClick(e) {
        //this.carousel.openZoom(this.image_data)
        var modal = document.getElementById("myModal");
        // // Get the button that opens the modal
        // var btn = document.getElementById("myBtn");
        // // Get the <span> element that closes the modal
        // var span = document.getElementsByClassName("close")[0];
        // When the user clicks the button, open the modal 
        modal.style.display = "block";
        if (this.jupyter_widget) {
            if (this.carousel.selected_id === this.id) {
                this.target = "unselected";
                this.carousel.selected_id = -1;
                this.jupyter_widget.selected_id = [-1];
                this.jupyter_widget.model.set("selected_id", JSON.parse(JSON.stringify([-1])));
                this.jupyter_widget.touch();
            }
            else {
                this.carousel.selected_id = this.id;
                this.jupyter_widget.selected_id = [this.id];
                this.jupyter_widget.model.set("selected_id", JSON.parse(JSON.stringify([this.id])));
                this.jupyter_widget.touch();
                this.carousel.deselect();
                this.target = "selected";
                this.jupyter_widget.send({ event: { selected: this.id } });
                this.jupyter_widget.touch();
            }
        }
    }
    render() {
        const image_height = this.height;
        //height:${this.height}px
        //${image_height}px
        return lit_element_1.html `
	<div class="polaroid tooltip" style="width:${this.width}px;"  @click="${(e) => this._handleClick(e)}"  target="${this.target}" >
	  <img class=myid src=${this.image_data} style=" width:100%;  height:${image_height}px; object-fit: contain; ">

	  <p class="caption_class" id="image_caption">
	  ${this.caption}
	  </p>
	</div>
	`;
    }
}
litPolaroid.properties = {
    caption: { type: String },
    image_data: { type: String },
    width: { type: Number },
    target: { type: String }
};
litPolaroid.styles = [lit_element_1.css `
	
	 div.polaroid {

	  display: flex;
	  flex-direction: column;

	  width: 200px;
	  
	  background-color: #FCFAEF; 
	  box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
	  
	  padding: 5px 2px 0px 2px;

	  align-items:center;
	  justify-content: space-around;
	  overflow: hidden;

	  margin-bottom:2px;
	  margin-top:5px;

	  margin-right:5px;

	  

	  border-radius: 8px;
	}
	div.polaroid[target=selected] {
	  transition: 0.2s;
	  background-color: #F2CCA7;
	  box-shadow: 4px 8px 8px 2px rgba(0, 0, 0, 0.2);
	   margin-top: 2px;
	   // margin-left: -2px;
	}
	 div.polaroid:hover{
	   transition: 0.2s;
	   box-shadow: 4px 8px 8px 2px rgba(0, 0, 0, 0.2);
	   // margin-top: -2px;
	   // margin-left: -2px;

	 }
	p.caption_class {
	  text-align: center;
	  width: 100%;
	  padding:0px;
	  margin:0px;
	  overflow-wrap: break-word;
	}
  `];
customElements.define('lit-polaroid', litPolaroid);
//${this.image_list.map( (url:any) => html`<lit-polaroid  image_data=${url}></lit-polaroid>`) }
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class PolaroidModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: PolaroidModel.model_name, _model_module: PolaroidModel.model_module, _model_module_version: PolaroidModel.model_module_version, _view_name: PolaroidModel.view_name, _view_module: PolaroidModel.view_module, _view_module_version: PolaroidModel.view_module_version, _id: 'polaroid', image: '', im_format: 'png', width: 200, height: 220, selected: false });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        console.log("initialize");
        this.on('msg:custom', this.onMessage.bind(this));
        this.send({ event: 'client_ready' }, {}); //{ event: 'client_ready' }, {});
    }
    onMessage(message, buffers) {
        return __awaiter(this, void 0, void 0, function* () {
            // Retrieve the commands buffer as an object (list of commands)
            console.log("command", message, buffers);
        });
    }
}
exports.PolaroidModel = PolaroidModel;
PolaroidModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
PolaroidModel.model_name = 'PolaroidModel';
PolaroidModel.model_module = version_1.MODULE_NAME;
PolaroidModel.model_module_version = version_1.MODULE_VERSION;
PolaroidModel.view_name = 'PolaroidView'; // Set to null if no view
PolaroidModel.view_module = version_1.MODULE_NAME; // Set to null if no view
PolaroidModel.view_module_version = version_1.MODULE_VERSION;
class PolaroidView extends base_1.DOMWidgetView {
    // initialize(){
    //  this.el.style.setProperty("minWidth","400px")
    //   console.log(this.el.style)
    // }
    render() {
        this.el.classList.add("polaroid-widget");
        console.log("PolaroidView 6");
        // const layout=this.model.get('layout')
        // layout.attributes["min_width"]="600px"
        // console.log("layout",layout);
        // this.setLayout(layout);
        console.log("size", this.model.get("width"), this.model.get("height"));
        this.polaroid = document.createElement("lit-polaroid");
        this.polaroid.width = this.model.get("width");
        this.polaroid.height = this.model.get("height");
        this.el.appendChild(this.polaroid);
        var url = '';
        const format = this.model.get('im_format');
        const value = this.model.get('image');
        console.log("format", format);
        if (format !== 'url') {
            const blob = new Blob([value], {
                type: `image/${this.model.get('format')}`,
            });
            url = URL.createObjectURL(blob);
        }
        else {
            url = value;
        }
        console.log(url);
        this.polaroid.image_data = url;
        this.polaroid.caption = this.model.get('caption');
        this.model.on('change:image', this.image_changed, this);
        this.model.on('change:caption', this.caption_changed, this);
        this.model.on('change:selected', this.select_change, this);
        this.polaroid.addEventListener('mousedown', { handleEvent: this.onMouseDown.bind(this) });
        //this.polaroid.setAttribute('tabindex', '0');
    }
    select_change() {
        const selected = this.model.get("selected");
        if (selected) {
            this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target", "selected");
        }
        else {
            this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target", "unselected");
        }
    }
    onMouseDown(event) {
        // Bring focus to the canvas element, so keyboard events can be triggered
        this.polaroid.focus();
        console.log("onMouseDown", event.type);
        const msg = { _id: '', type: '', buttons: -1 };
        msg.type = event.type;
        msg.buttons = event.buttons;
        msg._id = this.model.get('_id');
        //this.polaroid.shadowRoot.querySelector(".polaroid").setAttribute("target","selected")
        this.send(Object.assign({ event: event.type }, msg));
        //this.send({ event_type :'toto event' });
    }
    caption_changed() {
        const caption_element = this.polaroid.caption_element;
        // console.log("cap .caption_class ",this.polaroid.shadowRoot.querySelector(".caption_class"))
        // console.log("cap #image_caption",this.polaroid.shadowRoot.querySelector("#image_caption"))
        caption_element.textContent = this.model.get('caption');
        this.polaroid.caption = this.model.get('caption');
        console.log("set caption", this.polaroid.caption);
    }
    image_changed() {
        var url = '';
        console.log("image_changed");
        const format = this.model.get('im_format');
        const value = this.model.get('image');
        console.log("format", format);
        if (format !== 'url') {
            const blob = new Blob([value], {
                type: `image/${this.model.get('format')}`,
            });
            url = URL.createObjectURL(blob);
        }
        else {
            url = value;
        }
        console.log(url);
        this.polaroid.image_data = url;
        this.polaroid.caption = this.model.get('caption');
        this.polaroid.update();
    }
}
exports.PolaroidView = PolaroidView;
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class litCarousel extends lit_element_1.LitElement {
    constructor() {
        super();
        //this.image_list=new Array()
        this.polaroid_items = new Array();
        this.width = 800;
        this.height = 400;
        this.item_width = 200;
        this.item_height = 200;
        this.nb_per_page = 0;
        this.page_number = 0;
        this.nb_samples = 0;
        this.nb_pages = 0;
        this.selected_id = 'none';
        this.wrap_mode = "wrap";
        this.wait = false;
        this.count = 0;
    }
    deselect() {
        for (var i = 0; i < this.polaroid_items.length; ++i) {
            if (this.polaroid_items[i])
                this.polaroid_items[i].target = "unselected";
        }
    }
    createItems(image_list) {
        // if (image_list){
        //   this.image_list=image_list
        // }
        console.log("createItems !!");
        this.nb_per_page = Math.floor(this.width / (this.item_width + 9)) * Math.floor(this.height / (this.item_height + 10 + 20));
        this.polaroid_items = new Array(this.nb_per_page);
        for (var i = 0; i < this.polaroid_items.length; ++i) {
            this.polaroid_items[i] = new litPolaroid();
            if (this.images_data.has(i)) {
                this.polaroid_items[i].image_data = this.images_data.get(i).url;
                this.polaroid_items[i].caption = this.images_data.get(i).caption;
            }
            //console.log(i,this.images_data.get(i).caption)
            this.polaroid_items[i].jupyter_widget = this.jupyter_widget;
            this.polaroid_items[i].id = i;
            this.polaroid_items[i].width = this.item_width;
            this.polaroid_items[i].height = this.item_height;
            this.polaroid_items[i].carousel = this;
            this.polaroid_items[i].style.order = i;
        }
    }
    computeNbPages() {
        this.nb_per_page = Math.floor(this.width / (this.item_width + 9)) * Math.floor(this.height / (this.item_height + 10 + 20));
        this.nb_pages = Math.floor(this.jupyter_widget.images_index.length / this.nb_per_page) + 1;
    }
    updatePageContent(begin, end) {
        console.log("update index_page", this.page_number, "begin", begin, "end", end);
        var i_item = 0;
        for (var i = begin; i < end; ++i, ++i_item) {
            if (this.images_data.has(i)) {
                if (!this.polaroid_items[i_item])
                    this.polaroid_items[i_item] = new litPolaroid();
                console.log(i, this.images_data.get(i).caption);
                this.polaroid_items[i_item].image_data = this.images_data.get(i).url;
                this.polaroid_items[i_item].id = i;
                this.polaroid_items[i_item].width = this.item_width;
                this.polaroid_items[i_item].height = this.item_height;
                this.polaroid_items[i_item].caption = this.images_data.get(i).caption;
                this.polaroid_items[i_item].carousel = this;
                this.polaroid_items[i_item].jupyter_widget = this.jupyter_widget;
                this.polaroid_items[i_item].style.order = i_item;
            }
            //     //nbdone+=1
        }
        console.log("nb correct", i_item);
        for (var i = i_item; i < this.polaroid_items.length; i++)
            delete this.polaroid_items[i];
        this.deselect();
        const match = this.polaroid_items.filter((item) => item.id === this.selected_id);
        if (match.length > 0) {
            console.log(match);
            match[0].target = "selected";
        }
    }
    gotoPage(page_index) {
        if (this.wait)
            return;
        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!   update", page_index);
        this.nb_per_page = Math.floor(this.width / (this.item_width + 9)) * Math.floor(this.height / (this.item_height + 10 + 20));
        this.nb_per_page = this.nb_per_page < this.polaroid_items.length ? this.nb_per_page : this.polaroid_items.length;
        console.log("width", this.width, "height", this.height);
        console.log("nb row ", Math.floor(this.width / (this.item_width + 9)));
        console.log("nb col", Math.floor(this.height / (this.item_height + 10 + 20)));
        console.log("this.nb_per_page", this.nb_per_page);
        var begin = page_index * this.nb_per_page;
        begin = begin > 0 ? begin : 0;
        var end = begin + this.nb_per_page;
        if (begin >= this.jupyter_widget.images_index.length)
            return;
        end = end < this.jupyter_widget.images_index.length ? end : this.jupyter_widget.images_index.length;
        begin = begin < this.jupyter_widget.images_index.length ? begin : this.jupyter_widget.images_index.length;
        //if (begin>=end) return
        console.log("begin", begin);
        console.log("end", end);
        //|| !((end-1) in this.jupyter_widget.data_indices)
        const missing = [];
        for (var i = begin; i < end; i++) {
            if (!(this.jupyter_widget.images_data.has(i))) {
                missing.push(i);
            }
        }
        console.log("missing", missing);
        if (!(this.jupyter_widget.images_data.has(begin)) || !(this.jupyter_widget.images_data.has(end - 1))) {
            this.count += 1;
            this.wait = true;
            this.jupyter_widget.send({ send_data: [begin, end, this.count] });
            console.log("!!!!!!!!!!!!!! SEND ME DATA ", begin, end, this.count);
            //console.log("image_data",this.jupyter_widget.images_data.size)
            this.jupyter_widget.data_received = false;
            const waitFor = (condFunc) => __awaiter(this, void 0, void 0, function* () {
                return new Promise((resolve) => {
                    if (condFunc()) {
                        resolve();
                    }
                    else {
                        console.log(".");
                        setTimeout(() => __awaiter(this, void 0, void 0, function* () {
                            yield waitFor(condFunc);
                            resolve();
                        }), 400);
                    }
                });
            });
            const myFunc = () => __awaiter(this, void 0, void 0, function* () {
                yield waitFor(() => (this.jupyter_widget.data_received === true));
                console.log('!!!!!!! FINI D ATTENDRE');
                this.wait = false;
                // this.page_number-=1
                this.updatePageContent(begin, end);
                this.update(this.jupyter_widget.image_list);
            });
            myFunc();
            return;
        }
        this.updatePageContent(begin, end);
        this.wait = false;
    }
    updateItem(i) {
        const match = this.polaroid_items.filter((item) => item.id === i);
        if (match.length > 0) {
            match[0].jupyter_widget = this.jupyter_widget;
            //if (match[0].image_data)  URL.revokeObjectURL(match[0].image_data);
            match[0].image_data = this.images_data.get(i).url;
            match[0].id = i;
            match[0].width = this.item_width;
            match[0].caption = this.images_data.get(i).caption;
            match[0].carousel = this;
            match[0].style.order = i;
        }
        else {
            console.log("NO MATCH WITH ", i);
        }
    }
    wheel_func(event) {
        event.preventDefault();
        const delta = Math.sign(event.deltaY);
        this.move_by(delta);
    }
    isNumeric(a) {
        if (typeof a != "string")
            return false; // we only process strings!  
        return !isNaN(a) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
            !isNaN(parseFloat(a)); // ...and ensure strings of whitespace fail
    }
    //style="z-index=9999; height=100%
    get imageZoom() {
        return lit_element_1.html `
        <p> toto</p>
        <mwc-dialog hideActions style="--mdc-dialog-z-index:99999999;--mdc-shape-medium: 0px; --mdc-dialog-max-width:800px; --mdc-dialog-padding-top: 400px;">
            
            <img class="image_zoom" style="height:400px; object-fit:contain; ">
           
            
           
        </mwc-dialog>
        `;
    }
    openZoom(image) {
        const d = this.shadowRoot.querySelector('mwc-dialog');
        d.open = true;
        console.log(d.style.marginTop);
        const i = d.querySelector('.image_zoom');
        i.src = image;
    }
    render() {
        //if (this.polaroid_items.length===0)  this.createItems();
        // var width
        // if (this.isNumeric(this.width)) width=this.width+"px"
        console.log("render carousel");
        return lit_element_1.html `
	   ${this.imageZoom}

<div id="myModal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="close">&times;</span>
    <p>Some text in the Modal..</p>
  </div>


	<div class="lit-carousel" 
		 style="width:${this.width}px;; height:fit-content; flex-wrap:${this.wrap_mode}" 
		 @wheel=${(event) => this.wheel_func(event)}
	>
	  ${this.polaroid_items.map((item) => lit_element_1.html `${item}
		`)}
	  
	</div>
	<div class="navigation"  style="width:${this.width}px; " >
	<p>Page : ${this.page_number}/${this.nb_pages - 1}</p>
	<p class="icon" title="Rewind"         @click=${() => this.move_by(-10)} >${rewind}</p>
	  <p class="icon" title="Back"           @click=${() => this.move_by(-1)} >${left_arrow}</p>
	  <p class="icon" title="Next"           @click=${() => this.move_by(1)} >${right_arrow}</p>
	  <p class="icon" title="Fast Forward"   @click=${() => this.move_by(10)} >${fastforward}</p>
	  </div>
`;
    }
    move_by(step) {
        if (this.wait)
            return;
        var page_number = this.page_number + step;
        this.computeNbPages();
        page_number = page_number > 0 ? page_number : 0;
        page_number = page_number < this.nb_pages ? page_number : this.nb_pages - 1;
        this.gotoPage(page_number);
        this.page_number = page_number;
    }
}
litCarousel.properties = {
    page_number: { type: Number }
};
litCarousel.styles = [lit_element_1.css `
	  .lit-carousel{
		display: flex;
		flex-direction: row;
		overflow: hidden;
		flex-wrap: wrap;
	  }
	.icon {
		 width:  30px;
		 height:  30px;

		  margin-bottom: 10px;
		  margin-left: 10px;
		  margin-right: 10px;
		  margin-top: 10px;
		  z-index: 1;
		  color: black;
		  background: white;
		  fill: #79005D;
		  padding: 10px;
		  border-radius: 50%;
		  cursor: pointer;
		   box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
		}

		.icon:hover {
		background:  #79005D;
		fill: white;
		 box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);
	  }
	  .navigation{
		display: flex;
		width: 100%;
		align-items: center;
		align-content: center;
		justify-content: center;

	  }

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 400px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
	  `];
customElements.define('lit-carousel', litCarousel);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class CarouselModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: CarouselModel.model_name, _model_module: CarouselModel.model_module, _model_module_version: CarouselModel.model_module_version, _view_name: CarouselModel.view_name, _view_module: CarouselModel.view_module, _view_module_version: CarouselModel.view_module_version, _id: 'Carousel', image_list: [], image_index: [], im_format: 'png', image_captions: [], width: 800, item_with: 200, item_height: 200, selected_id: [] });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        console.log("initialize");
        //this.on('msg:custom', this.onMessage.bind(this));
    }
}
exports.CarouselModel = CarouselModel;
CarouselModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
CarouselModel.model_name = 'CarouselModel';
CarouselModel.model_module = version_1.MODULE_NAME;
CarouselModel.model_module_version = version_1.MODULE_VERSION;
CarouselModel.view_name = 'CarouselView'; // Set to null if no view
CarouselModel.view_module = version_1.MODULE_NAME; // Set to null if no view
CarouselModel.view_module_version = version_1.MODULE_VERSION;
class CarouselView extends base_1.DOMWidgetView {
    onMessage(message, buffers) {
        return __awaiter(this, void 0, void 0, function* () {
            // Retrieve the commands buffer as an object (list of commands)
            console.log("command", message, buffers);
            if ("set_image" in message) {
                console.log("set new image", message.set_image.index, message.set_image.caption);
                const index = message.set_image.index, caption = message.set_image.caption, format = message.set_image.format;
                var url = '';
                if (this.images_data.has(index)) {
                    console.log("found", index);
                    if (format !== 'url') {
                        const blob = new Blob(buffers, { type: `image/${format}`, });
                        url = URL.createObjectURL(blob);
                    }
                    else {
                        url = (new TextDecoder('utf-8')).decode(buffers[0]);
                    }
                    //console.log(cap_list[i])    
                    this.images_data.set(index, { caption: caption, url: url });
                    console.log(this.images_data.get(index));
                    this.carousel.updateItem(index);
                }
            }
            console.log(this.images_data);
        });
    }
    render() {
        this.el.classList.add("Carousel-widget");
        console.log("CarouselView 7");
        // const layout=this.model.get('layout')
        // layout.attributes["min_width"]="600px"
        // console.log("layout",layout);
        // this.setLayout(layout);
        this.images_index = this.model.get("images_index");
        console.log("this.images_index", this.images_index.length);
        const width = this.model.get("width");
        const height = this.model.get("height");
        const item_width = this.model.get("item_width");
        const item_height = this.model.get("item_height");
        this.model.on('change:image_list', this.dataFromPython, this);
        this.model.on('change:selected_id', this.onSelectedId, this);
        this.model.on('msg:custom', this.onMessage.bind(this));
        this.carousel = document.createElement('lit-carousel');
        this.carousel.item_width = item_width;
        this.carousel.item_height = item_height;
        this.carousel.width = width;
        this.carousel.height = height;
        this.carousel.jupyter_widget = this;
        this.images_data = new Map();
        this.updateImagesData();
        this.carousel.images_data = this.images_data;
        this.carousel.computeNbPages();
        this.carousel.createItems();
        this.carousel.gotoPage(0);
        // POUR EFFACER IMAGE LIST 
        // this.model.set("image_list",JSON.parse(JSON.stringify(['-'])));
        // this.touch()
        this.data_received = false;
        //console.log("step",step,(width/(item_width+14)))
        this.el.appendChild(this.carousel);
        const playbackcontrol = document.createElement("playback-control");
        playbackcontrol.max = 100;
        playbackcontrol.current = 0;
        this.el.appendChild(playbackcontrol);
    }
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    onSelectedId() {
        console.log("selected_id", this.selected_id);
    }
    dataFromPython() {
        this.data_received = false;
        console.log("dataFromPython");
        if (this.updateImagesData()) {
            this.carousel.images_data = this.images_data;
            this.data_received = true;
        }
        this.data_received = true;
    }
    updateImagesData() {
        const im_list = this.model.get('image_list');
        if (im_list[0] === '-') {
            console.log("liste vide");
            return false;
        }
        console.log(im_list[0][0]);
        console.log("updateImagesData", im_list.length);
        // for (var i = 0; i < im_list.length; i++) {
        //   this.data_indices.push(im_list[i][1])
        //   console.log("new ind",im_list[i][1])
        // } 
        var url = '';
        const nb_to_come = im_list.length;
        if (nb_to_come + this.images_data.size > 100) {
            console.log("CLEANING");
            const nb_to_remove = nb_to_come + this.images_data.size - 100;
            var i = 0;
            var nb_remove = 0;
            while (nb_remove < nb_to_remove) {
                if (this.images_data.has(i)) {
                    //console.log("remove",i)
                    URL.revokeObjectURL(this.images_data.get(i).url);
                    this.images_data.delete(i);
                    nb_remove++;
                }
                i++;
                if (i > this.images_data.size)
                    break;
            }
            console.log(".................... REMOVED ", nb_remove);
        }
        const cap_list = this.model.get('image_captions');
        const cap_list_tmp = new Array(im_list.length);
        for (var i = 0; i < im_list.length; i++) {
            const image_index = im_list[i][1];
            if (!this.images_data.has(image_index)) {
                console.log("add new image_index", image_index);
                if (this.model.get('format') !== 'url') {
                    const blob = new Blob([im_list[i][0]], { type: `image/${this.model.get('format')}`, });
                    url = URL.createObjectURL(blob);
                }
                else {
                    url = im_list[i][0];
                }
                //console.log(cap_list[i])    
                if (cap_list[image_index]) {
                    cap_list_tmp[i] = cap_list[image_index];
                }
                else {
                    cap_list_tmp[i] = image_index;
                }
                this.images_data.set(image_index, { caption: cap_list_tmp[i], url: url });
            }
        }
        console.log("NEW IMAGES DATA size", this.images_data.size);
        this.model.set("image_list", JSON.parse(JSON.stringify(['-'])));
        this.touch();
        return true;
    }
}
exports.CarouselView = CarouselView;
// var interval:number; //set scope here so both functions can access it
//     fastforward_.firstElementChild!.addEventListener("mousedown", function() {
//       avance_func(step*10);
//       interval = setInterval(()=>avance_func(step*10), 300); //500 ms - customize for your needs
//     });
//     fastforward_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
//     })
//     right_.firstElementChild!.addEventListener("mousedown", function() {
//       avance_func(step);
//       interval = setInterval(()=>avance_func(step), 300); //500 ms - customize for your needs
//     });
//     right_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
//     })
//     left_.firstElementChild!.addEventListener("mousedown", function() {
//       recule_func(step);
//       interval = setInterval(()=>recule_func(step), 300); //500 ms - customize for your needs
//     });
//     left_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) { clearInterval(interval ); }
//     });
//     rewind_.firstElementChild!.addEventListener("mousedown", function() {
//       recule_func(step*10);
//       interval = setInterval(()=>recule_func(step*10), 300); //500 ms - customize for your needs
//     });
//     rewind_.firstElementChild!.addEventListener("mouseup", function() {
//       if (interval ) clearInterval(interval );
//     })
//     function avance_func(step:number) {
//       that.pos+=1
//       that.carousel.gotoPage(that.pos)
//       console.log(that.pos)
//       // if (that.pos>that.image_and_captions.length-2)  that.pos=that.image_and_captions.length-2
//       // const w=item_width+14//that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect()["width"]
//       // console.log(that.pos,w*that.pos)
//       // that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 
//     }
//     function recule_func(step:number) {
//       that.pos-=1
//       if (that.pos<0) that.pos=0
//         that.carousel.gotoPage(that.pos)
//       console.log(that.pos)
//       //   const w=item_width+14
//       //   console.log(that.pos,w*that.pos)
//       // console.log(that.carousel.shadowRoot.querySelector("#carousel_item_1").getBoundingClientRect())
//       //that.carousel.shadowRoot.querySelector(".lit-carousel").scrollTo({left:w*that.pos-2,behavior:'smooth'}) 
//     } 
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".freeDrawing{\n     width:  30px;\n    }\n.icon {\n     width:  50px;\n      margin-bottom: 10px;\n      margin-left: 10px;\n      margin-right: 10px;\n      margin-top: 10px;\n      z-index: 1;\n      color: black;\n      background: white;\n      fill: #79005D;\n      padding: 10px;\n      border-radius: 50%;\n      cursor: pointer;\n       box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);\n    }\n\n    .icon:hover {\n    background:  #79005D;\n    fill: white;\n     box-shadow: 0px 6px 20px 0 rgba(0, 0, 0, 0.2);\n  }\n  .navigation{\n    display: flex;\n    width: 100%;\n    align-items: center;\n    align-content: center;\n    justify-content: center;\n\n  }", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"jupyter_polaroid","version":"0.1.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//ipypolaroid","bugs":{"url":"https://github.com//ipypolaroid/issues"},"license":"BSD-3-Clause","author":{"name":"nicolas allezard","email":"nicolas.allezard@cea.fr"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//ipypolaroid"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipypolaroid/labextension","clean:nbextension":"rimraf ipypolaroid/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@material/mwc-dialog":"^0.25.3","@material/mwc-slider":"^0.25.3","lit-element":"2.4.0","requirejs":"^2.3.6"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/node":"^17.0.21","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipypolaroid/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.aed828b9559258517986.js.map