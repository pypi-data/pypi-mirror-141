(self["webpackChunkvegafusion_jupyter"] = self["webpackChunkvegafusion_jupyter"] || []).push([["javascript_vegafusion-embed_lib_index_js"],{

/***/ "../../javascript/vegafusion-embed/lib/embed.js":
/*!******************************************************!*\
  !*** ../../javascript/vegafusion-embed/lib/embed.js ***!
  \******************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.a(module, async (__webpack_handle_async_dependencies__) => {
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "foo": () => (/* binding */ foo),
/* harmony export */   "embedVegaFusion": () => (/* binding */ embedVegaFusion)
/* harmony export */ });
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./version */ "../../javascript/vegafusion-embed/lib/version.js");
/* harmony import */ var _css_vegafusion_embed_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/vegafusion-embed.css */ "../../javascript/vegafusion-embed/css/vegafusion-embed.css");
/* harmony import */ var _css_vegafusion_embed_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_css_vegafusion_embed_css__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _images_VegaFusionLogo_SmallGrey_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../images/VegaFusionLogo-SmallGrey.svg */ "../../javascript/vegafusion-embed/images/VegaFusionLogo-SmallGrey.svg");

const { render_vegafusion } = await Promise.all(/*! import() */[__webpack_require__.e("vendors-vegafusion-wasm_node_modules_grpc-web_index_js-vegafusion-wasm_node_modules_lodash_lo-68e19e"), __webpack_require__.e("vegafusion-wasm_pkg_vegafusion_wasm_js")]).then(__webpack_require__.bind(__webpack_require__, /*! vegafusion-wasm */ "../../vegafusion-wasm/pkg/vegafusion_wasm.js"));

// @ts-ignore

const CHART_WRAPPER_CLASS = 'chart-wrapper';
let DOWNLOAD_FILE_NAME = "visualization";
const I18N = {
    CLICK_TO_VIEW_ACTIONS: 'Click to view actions',
    PNG_ACTION: 'Save as PNG',
    SVG_ACTION: 'Save as SVG',
};
function foo() {
    console.log([_version__WEBPACK_IMPORTED_MODULE_0__.MODULE_NAME, _version__WEBPACK_IMPORTED_MODULE_0__.MODULE_VERSION]);
}
const defaultEmbedConfig = {
    verbose: false, debounce_wait: 30, debounce_max_wait: 60, download_source_link: undefined
};
function embedVegaFusion(element, spec_str, send_msg_fn, config) {
    // Clear existing children from element
    // Eventually we should detect when element is already setup and just make the necessary
    // changes
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    // Element that will be passed to render_vegafusion
    let chartElement = document.createElement("div");
    // Handle null config
    config = config || defaultEmbedConfig;
    // Render to chart element
    let receiver = render_vegafusion(chartElement, spec_str, config.verbose || defaultEmbedConfig.verbose, config.debounce_wait || defaultEmbedConfig.debounce_wait, config.debounce_max_wait || defaultEmbedConfig.debounce_max_wait, send_msg_fn);
    // Build container element that will hold the vegafusion chart
    let containerElement = document.createElement("div");
    containerElement.appendChild(chartElement);
    containerElement.classList.add(CHART_WRAPPER_CLASS);
    // Element that holds the dropdown menu
    let menuElement = document.createElement("div");
    menuElement.appendChild(buildMenu(receiver, undefined));
    // Add children to top-level element
    element.appendChild(containerElement);
    element.appendChild(menuElement);
    element.classList.add("vegafusion-embed");
    element.classList.add("has-actions");
    return receiver;
}
function buildMenu(receiver, download_source_link) {
    const details = document.createElement('details');
    details.title = I18N.CLICK_TO_VIEW_ACTIONS;
    const summary = document.createElement('summary');
    summary.innerHTML = _images_VegaFusionLogo_SmallGrey_svg__WEBPACK_IMPORTED_MODULE_2__["default"];
    details.append(summary);
    let documentClickHandler = (ev) => {
        if (!details.contains(ev.target)) {
            details.removeAttribute('open');
        }
    };
    document.addEventListener('click', documentClickHandler);
    // popup
    const ctrl = document.createElement('div');
    details.append(ctrl);
    ctrl.classList.add('vegafusion-actions');
    // image export
    for (const ext of ['svg', 'png']) {
        let scale_factor = 1.0;
        const i18nExportAction = I18N[`${ext.toUpperCase()}_ACTION`];
        const exportLink = document.createElement('a');
        exportLink.text = i18nExportAction;
        exportLink.href = '#';
        exportLink.target = '_blank';
        exportLink.download = `${DOWNLOAD_FILE_NAME}.${ext}`;
        // Disable browser tooltip
        exportLink.title = '';
        // add link on mousedown so that it's correct when the click happens
        exportLink.addEventListener('mousedown', async function (e) {
            e.preventDefault();
            if (receiver) {
                this.href = await receiver.to_image_url(ext, scale_factor);
            }
        });
        ctrl.append(exportLink);
    }
    // Add hr
    ctrl.append(document.createElement("hr"));
    // Add About
    const aboutLink = document.createElement('a');
    const about_href = 'https://vegafusion.io/';
    aboutLink.text = "About VegaFusion";
    aboutLink.href = about_href;
    aboutLink.target = '_blank';
    aboutLink.title = about_href;
    ctrl.append(aboutLink);
    // Add License
    const licenseLink = document.createElement('a');
    const licence_href = 'https://www.gnu.org/licenses/agpl-3.0.en.html';
    licenseLink.text = "AGPLv3 License";
    licenseLink.href = licence_href;
    licenseLink.target = '_blank';
    licenseLink.title = licence_href;
    ctrl.append(licenseLink);
    // Add source message
    if (download_source_link) {
        const sourceItem = document.createElement('a');
        sourceItem.text = 'Download Source';
        sourceItem.href = download_source_link;
        sourceItem.target = '_blank';
        sourceItem.title = download_source_link;
        ctrl.append(sourceItem);
    }
    else {
        const sourceItem = document.createElement('p');
        sourceItem.classList.add('source-msg');
        sourceItem.textContent =
            "VegaFusion's AGPLv3 license requires " +
                "the author to provide this application's " +
                'source code upon request';
        sourceItem.title = '';
        ctrl.append(sourceItem);
    }
    return details;
}
//# sourceMappingURL=embed.js.map
__webpack_handle_async_dependencies__();
}, 1);

/***/ }),

/***/ "../../javascript/vegafusion-embed/lib/grpc.js":
/*!*****************************************************!*\
  !*** ../../javascript/vegafusion-embed/lib/grpc.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "makeGrpcSendMessageFn": () => (/* binding */ makeGrpcSendMessageFn)
/* harmony export */ });
/* harmony import */ var grpc_web__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! grpc-web */ "../../javascript/vegafusion-embed/node_modules/grpc-web/index.js");
/* harmony import */ var grpc_web__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(grpc_web__WEBPACK_IMPORTED_MODULE_0__);

// Other utility functions
function makeGrpcSendMessageFn(client, hostname) {
    let sendMessageGrpc = (send_msg_bytes, receiver) => {
        let grpc_route = '/services.VegaFusionRuntime/TaskGraphQuery';
        // Make custom MethodDescriptor that does not perform serialization
        const methodDescriptor = new (grpc_web__WEBPACK_IMPORTED_MODULE_0___default().MethodDescriptor)(grpc_route, (grpc_web__WEBPACK_IMPORTED_MODULE_0___default().MethodType.UNARY), Uint8Array, Uint8Array, (v) => v, (v) => v);
        let promise = client.thenableCall(hostname + grpc_route, send_msg_bytes, {}, methodDescriptor);
        promise.then((response) => {
            receiver.receive(response);
        });
    };
    return sendMessageGrpc;
}
//# sourceMappingURL=grpc.js.map

/***/ }),

/***/ "../../javascript/vegafusion-embed/lib/index.js":
/*!******************************************************!*\
  !*** ../../javascript/vegafusion-embed/lib/index.js ***!
  \******************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.a(module, async (__webpack_handle_async_dependencies__) => {
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_NAME": () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_0__.MODULE_NAME),
/* harmony export */   "MODULE_VERSION": () => (/* reexport safe */ _version__WEBPACK_IMPORTED_MODULE_0__.MODULE_VERSION),
/* harmony export */   "embedVegaFusion": () => (/* reexport safe */ _embed__WEBPACK_IMPORTED_MODULE_1__.embedVegaFusion),
/* harmony export */   "foo": () => (/* reexport safe */ _embed__WEBPACK_IMPORTED_MODULE_1__.foo),
/* harmony export */   "makeGrpcSendMessageFn": () => (/* reexport safe */ _grpc__WEBPACK_IMPORTED_MODULE_2__.makeGrpcSendMessageFn)
/* harmony export */ });
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./version */ "../../javascript/vegafusion-embed/lib/version.js");
/* harmony import */ var _embed__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./embed */ "../../javascript/vegafusion-embed/lib/embed.js");
/* harmony import */ var _grpc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./grpc */ "../../javascript/vegafusion-embed/lib/grpc.js");
var __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([_embed__WEBPACK_IMPORTED_MODULE_1__]);
_embed__WEBPACK_IMPORTED_MODULE_1__ = (__webpack_async_dependencies__.then ? await __webpack_async_dependencies__ : __webpack_async_dependencies__)[0];
/*
 * VegaFusion
 * Copyright (C) 2022 Jon Mease
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.
 * If not, see http://www.gnu.org/licenses/.
 */



//# sourceMappingURL=index.js.map
});

/***/ }),

/***/ "../../javascript/vegafusion-embed/lib/version.js":
/*!********************************************************!*\
  !*** ../../javascript/vegafusion-embed/lib/version.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_VERSION": () => (/* binding */ MODULE_VERSION),
/* harmony export */   "MODULE_NAME": () => (/* binding */ MODULE_NAME)
/* harmony export */ });
/*
 * VegaFusion
 * Copyright (C) 2022 Jon Mease
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.
 * If not, see http://www.gnu.org/licenses/.
 */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "../../javascript/vegafusion-embed/package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!../../javascript/vegafusion-embed/css/vegafusion-embed.css":
/*!********************************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!../../javascript/vegafusion-embed/css/vegafusion-embed.css ***!
  \********************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../python/vegafusion-jupyter/node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../python/vegafusion-jupyter/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_python_vegafusion_jupyter_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".vegafusion-embed {\n  min-height: 40px;\n  position: relative;\n  display: inline-block;\n  box-sizing: border-box;\n  overflow: visible;\n}\n.vegafusion-embed.has-actions {\n  padding-right: 38px;\n}\n.vegafusion-embed details:not([open]) > :not(summary) {\n  display: none !important;\n}\n.vegafusion-embed summary {\n  list-style: none;\n  position: absolute;\n  top: 0;\n  right: 0;\n  padding: 6px;\n  z-index: 1000;\n  background: white;\n  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);\n  color: #1b1e23;\n  border: 1px solid #aaa;\n  border-radius: 999px;\n  opacity: 0.2;\n  transition: opacity 0.4s ease-in;\n  outline: none;\n  cursor: pointer;\n  line-height: 0px;\n}\n.vegafusion-embed summary::-webkit-details-marker {\n  display: none;\n}\n.vegafusion-embed summary:active {\n  box-shadow: #aaa 0px 0px 0px 1px inset;\n}\n.vegafusion-embed summary svg {\n  width: 16px;\n  height: 16px;\n}\n.vegafusion-embed details[open] summary {\n  opacity: 0.5;\n}\n.vegafusion-embed:hover summary, .vegafusion-embed:focus summary {\n  opacity: 0.7 !important;\n  transition: opacity 0.2s ease;\n}\n.vegafusion-embed .vegafusion-actions {\n  position: absolute;\n  z-index: 1001;\n  top: 35px;\n  right: -9px;\n  display: flex;\n  flex-direction: column;\n  padding-bottom: 8px;\n  padding-top: 8px;\n  border-radius: 4px;\n  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.2);\n  border: 1px solid #d9d9d9;\n  background: white;\n  animation-duration: 0.15s;\n  animation-name: scale-in;\n  animation-timing-function: cubic-bezier(0.2, 0, 0.13, 1.5);\n  text-align: left;\n}\n.vegafusion-embed .vegafusion-actions hr {\n  width: auto;\n  height: 1px;\n  border: none;\n  background-color: #434a56;\n  margin: 4px 10px 4px 10px;\n  opacity: 50%;\n}\n.vegafusion-embed .vegafusion-actions .source-msg {\n  padding: 4px 16px;\n  font-family: sans-serif;\n  font-size: 10px;\n  font-weight: 400;\n  max-width: 180px;\n  color: #CD5C5C;\n}\n.vegafusion-embed .vegafusion-actions a {\n  padding: 4px 16px;\n  font-family: sans-serif;\n  font-size: 12px;\n  font-weight: 600;\n  white-space: nowrap;\n  color: #434a56;\n  text-decoration: none;\n}\n.vegafusion-embed .vegafusion-actions a:hover {\n  background-color: #f7f7f9;\n  color: black;\n}\n.vegafusion-embed .vegafusion-actions::before, .vegafusion-embed .vegafusion-actions::after {\n  content: \"\";\n  display: inline-block;\n  position: absolute;\n  pointer-events: none;\n}\n.vegafusion-embed .vegafusion-actions::before {\n  left: auto;\n  right: 14px;\n  top: -16px;\n  border: 8px solid #0000;\n  border-bottom-color: #d9d9d9;\n}\n.vegafusion-embed .vegafusion-actions::after {\n  left: auto;\n  right: 15px;\n  top: -14px;\n  border: 7px solid #0000;\n  border-bottom-color: #fff;\n}\n.vegafusion-embed .chart-wrapper.fit-x {\n  width: 100%;\n}\n.vegafusion-embed .chart-wrapper.fit-y {\n  height: 100%;\n}\n\n.vegafusion-embed-wrapper {\n  max-width: 100%;\n  overflow: auto;\n  padding-right: 14px;\n}\n\n@keyframes scale-in {\n  from {\n    opacity: 0;\n    transform: scale(0.6);\n  }\n  to {\n    opacity: 1;\n    transform: scale(1);\n  }\n}\n\n/*# sourceMappingURL=vegafusion-embed.css.map */\n", "",{"version":3,"sources":["webpack://./../../javascript/vegafusion-embed/scss/vegafusion-embed.scss","webpack://./../../javascript/vegafusion-embed/css/vegafusion-embed.css"],"names":[],"mappings":"AAEA;EACE,gBAAA;EACA,kBAAA;EACA,qBAAA;EACA,sBAAA;EACA,iBAAA;ACDF;ADGE;EACE,mBAAA;ACDJ;ADIE;EACE,wBAAA;ACFJ;ADKE;EACE,gBAAA;EACA,kBAAA;EACA,MAAA;EACA,QAAA;EACA,YAAA;EACA,aAAA;EACA,iBAAA;EACA,0CAAA;EACA,cAAA;EACA,sBAAA;EACA,oBAAA;EACA,YAAA;EACA,gCAAA;EACA,aAAA;EACA,eAAA;EACA,gBAAA;ACHJ;ADKI;EACE,aAAA;ACHN;ADMI;EACE,sCAAA;ACJN;ADOI;EACE,WAAA;EACA,YAAA;ACLN;ADSE;EACE,YAAA;ACPJ;ADUE;EAEE,uBAAA;EACA,6BAAA;ACTJ;ADYE;EACE,kBAAA;EACA,aAAA;EACA,SAAA;EACA,WAAA;EACA,aAAA;EACA,sBAAA;EACA,mBAAA;EACA,gBAAA;EACA,kBAAA;EACA,0CAAA;EACA,yBAAA;EACA,iBAAA;EACA,yBAAA;EACA,wBAAA;EACA,0DAAA;EACA,gBAAA;ACVJ;ADYI;EACE,WAAA;EACA,WAAA;EACA,YAAA;EACA,yBAAA;EACA,yBAAA;EACA,YAAA;ACVN;ADaI;EACE,iBAAA;EACA,uBAAA;EACA,eAAA;EACA,gBAAA;EACA,gBAAA;EACA,cAAA;ACXN;ADcI;EACE,iBAAA;EACA,uBAAA;EACA,eAAA;EACA,gBAAA;EACA,mBAAA;EACA,cAAA;EACA,qBAAA;ACZN;ADcM;EACE,yBAAA;EACA,YAAA;ACZR;ADgBI;EAEE,WAAA;EACA,qBAAA;EACA,kBAAA;EACA,oBAAA;ACfN;ADkBI;EACE,UAAA;EACA,WAAA;EACA,UAAA;EACA,uBAAA;EACA,4BAAA;AChBN;ADmBI;EACE,UAAA;EACA,WAAA;EACA,UAAA;EACA,uBAAA;EACA,yBAAA;ACjBN;ADsBI;EACE,WAAA;ACpBN;ADsBI;EACE,YAAA;ACpBN;;ADyBA;EACE,eAAA;EACA,cAAA;EACA,mBAAA;ACtBF;;ADyBA;EACE;IACE,UAAA;IACA,qBAAA;ECtBF;EDyBA;IACE,UAAA;IACA,mBAAA;ECvBF;AACF;;AAEA,+CAA+C","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../javascript/vegafusion-embed/images/VegaFusionLogo-SmallGrey.svg":
/*!*****************************************************************************!*\
  !*** ../../javascript/vegafusion-embed/images/VegaFusionLogo-SmallGrey.svg ***!
  \*****************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg version=\"1.1\" viewBox=\"0.0 0.0 946.4776902887139 673.4829396325459\" fill=\"none\" stroke=\"none\" stroke-linecap=\"square\" stroke-miterlimit=\"10\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns=\"http://www.w3.org/2000/svg\"><clipPath id=\"p.0\"><path d=\"m0 0l946.47766 0l0 673.4829l-946.47766 0l0 -673.4829z\" clip-rule=\"nonzero\"/></clipPath><g clip-path=\"url(#p.0)\"><path fill=\"#000000\" fill-opacity=\"0.0\" d=\"m0 0l946.47766 0l0 673.4829l-946.47766 0z\" fill-rule=\"evenodd\"/><path fill=\"#434a56\" d=\"m241.20998 355.4672l228.50392 0l0 318.04727l-228.50392 0z\" fill-rule=\"evenodd\"/><path fill=\"#434a56\" d=\"m601.9989 0l-65.49762 177.0l343.29565 0.9973755l65.87903 -177.99738z\" fill-rule=\"evenodd\"/><path fill=\"#434a56\" d=\"m505.0006 317.5013l-42.4993 177.0l302.89688 0.15222168l64.59503 -177.88187z\" fill-rule=\"evenodd\"/><path fill=\"#434a56\" d=\"m0.46194226 -0.04330709l240.56693 673.5696l127.509186 -285.16272l-140.021 -388.40683z\" fill-rule=\"evenodd\"/><path fill=\"#434a56\" d=\"m712.8845 -0.01968504l-242.1799 673.54333l-229.69412 0l242.1799 -673.54333z\" fill-rule=\"evenodd\"/></g></svg>");

/***/ }),

/***/ "../../javascript/vegafusion-embed/css/vegafusion-embed.css":
/*!******************************************************************!*\
  !*** ../../javascript/vegafusion-embed/css/vegafusion-embed.css ***!
  \******************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../../../python/vegafusion-jupyter/node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../../../python/vegafusion-jupyter/node_modules/css-loader/dist/cjs.js!./vegafusion-embed.css */ "./node_modules/css-loader/dist/cjs.js!../../javascript/vegafusion-embed/css/vegafusion-embed.css");

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

/***/ "../../javascript/vegafusion-embed/package.json":
/*!******************************************************!*\
  !*** ../../javascript/vegafusion-embed/package.json ***!
  \******************************************************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"vegafusion-embed","version":"0.0.5","description":"Library to embed vegafusion visualizations","keywords":["vega","vega-lite","vegafusion","visualization"],"files":["lib/**/*.js","lib/**/*.d.ts","dist/*.js","dist/*.d.ts","dist/*.wasm","css/*.css","images/*.svg"],"homepage":"https://github.com/vegafusion/vegafusion","bugs":{"url":"https://github.com/vegafusion/vegafusion/issues"},"license":"AGPL-3.0-or-later","author":{"name":"Jon Mease","email":"jonmmease@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/jonmmease/vegafusion"},"scripts":{"build":"npm run build:lib","build:prod":"npm run clean && npm run build:lib","build:lib":"tsc && sass scss:css","clean":"npm run clean:lib && rimraf dist","clean:lib":"rimraf lib","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"npm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w"},"dependencies":{"vega-lite":"^4.17.0","vegafusion-wasm":"../../vegafusion-wasm/pkg","grpc-web":"^1.3.1"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@types/jest":"^26.0.0","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"6.5.1","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","sass":"^1.45.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","svg-inline-loader":"^0.8.2","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3"}}');

/***/ })

}]);
//# sourceMappingURL=javascript_vegafusion-embed_lib_index_js.3296face9376db262fb0.js.map