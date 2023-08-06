"use strict";
(self["webpackChunkvegafusion_jupyter"] = self["webpackChunkvegafusion_jupyter"] || []).push([["vegafusion-wasm_pkg_vegafusion_wasm_js"],{

/***/ "../../vegafusion-wasm/pkg/snippets/vegafusion-wasm-7be8a8f8730f9217/js/vega_utils.js":
/*!********************************************************************************************!*\
  !*** ../../vegafusion-wasm/pkg/snippets/vegafusion-wasm-7be8a8f8730f9217/js/vega_utils.js ***!
  \********************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vega_version": () => (/* binding */ vega_version),
/* harmony export */   "localTimezone": () => (/* binding */ localTimezone),
/* harmony export */   "getSignalValue": () => (/* binding */ getSignalValue),
/* harmony export */   "setSignalValue": () => (/* binding */ setSignalValue),
/* harmony export */   "getDataValue": () => (/* binding */ getDataValue),
/* harmony export */   "setDataValue": () => (/* binding */ setDataValue),
/* harmony export */   "addSignalListener": () => (/* binding */ addSignalListener),
/* harmony export */   "addDataListener": () => (/* binding */ addDataListener),
/* harmony export */   "setupTooltip": () => (/* binding */ setupTooltip),
/* harmony export */   "make_grpc_send_message_fn": () => (/* binding */ make_grpc_send_message_fn)
/* harmony export */ });
/* harmony import */ var vega__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vega */ "../../vegafusion-wasm/node_modules/vega/build/vega.module.js");
/* harmony import */ var vega_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! vega-util */ "../../vegafusion-wasm/node_modules/vega-util/build/vega-util.module.js");
/* harmony import */ var vega_tooltip__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! vega-tooltip */ "../../vegafusion-wasm/node_modules/vega-tooltip/build/vega-tooltip.module.js");
/* harmony import */ var grpc_web__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! grpc-web */ "../../vegafusion-wasm/node_modules/grpc-web/index.js");
/* harmony import */ var grpc_web__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(grpc_web__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! lodash */ "../../vegafusion-wasm/node_modules/lodash/lodash.js");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_4__);
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







function vega_version() {
    return vega__WEBPACK_IMPORTED_MODULE_0__.version
}

function localTimezone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
}

// JSON Serialize Dates to milliseconds
Object.defineProperty(Date.prototype, "toJSON", {value: function() {return this.getTime()}})

function getNestedRuntime(view, scope) {
    // name is an array that may have leading integer group indices
    var runtime = view._runtime;
    for (const index of scope) {
        runtime = runtime.subcontext[index];
    }
    return runtime
}

function lookupSignalOp(view, name, scope) {
    // name is an array that may have leading integer group indices
    let parent_runtime = getNestedRuntime(view, scope);
    return parent_runtime.signals[name];
}

function dataref(view, name, scope) {
    // name is an array that may have leading integer group indices
    let parent_runtime = getNestedRuntime(view, scope);
    return parent_runtime.data[name];
}

function getSignalValue(view, name, scope) {
    let signal_op = lookupSignalOp(view, name, scope);
    return lodash__WEBPACK_IMPORTED_MODULE_4___default().cloneDeep(signal_op.value)
}

function setSignalValue(view, name, scope, value) {
    let signal_op = lookupSignalOp(view, name, scope);
    view.update(signal_op, value);
}

function getDataValue(view, name, scope) {
    let data_op = dataref(view, name, scope);
    return lodash__WEBPACK_IMPORTED_MODULE_4___default().cloneDeep(data_op.values.value)
}

function setDataValue(view, name, scope, value) {
    let dataset = dataref(view, name, scope);
    let changeset = view.changeset().remove(vega_util__WEBPACK_IMPORTED_MODULE_1__.truthy).insert(value)
    dataset.modified = true;
    view.pulse(dataset.input, changeset);
}

function addSignalListener(view, name, scope, handler, wait, maxWait) {
    let signal_op = lookupSignalOp(view, name, scope);
    let options = {};
    if (maxWait) {
        options["maxWait"] = maxWait;
    }

    return addOperatorListener(
        view,
        name,
        signal_op,
        lodash__WEBPACK_IMPORTED_MODULE_4___default().debounce(handler, wait, options),
    );
}

function addDataListener(view, name, scope, handler, wait, maxWait) {
    let dataset = dataref(view, name, scope).values;
    let options = {};
    if (maxWait) {
        options["maxWait"] = maxWait;
    }
    return addOperatorListener(
        view,
        name,
        dataset,
        lodash__WEBPACK_IMPORTED_MODULE_4___default().debounce(handler, wait, options),
    );
}

function setupTooltip(view) {
    let tooltip_opts = {};
    let handler = new vega_tooltip__WEBPACK_IMPORTED_MODULE_2__.Handler(tooltip_opts).call;
    view.tooltip(handler)
}

// Private helpers from Vega
function findOperatorHandler(op, handler) {
    const h = (op._targets || [])
        .filter(op => op._update && op._update.handler === handler);
    return h.length ? h[0] : null;
}

function addOperatorListener(view, name, op, handler) {
    let h = findOperatorHandler(op, handler);
    if (!h) {
        h = trap(view, () => handler(name, op.value));
        h.handler = handler;
        view.on(op, null, h);
    }
    return view;
}

function trap(view, fn) {
    return !fn ? null : function() {
        try {
            fn.apply(this, arguments);
        } catch (error) {
            view.error(error);
        }
    };
}

// Other utility functions
function make_grpc_send_message_fn(client, hostname) {
    let send_message_grpc = (send_msg_bytes, receiver) => {
        let grpc_route = '/services.VegaFusionRuntime/TaskGraphQuery'

        // Make custom MethodDescriptor that does not perform serialization
        const methodDescriptor = new grpc_web__WEBPACK_IMPORTED_MODULE_3__.MethodDescriptor(
            grpc_route,
            grpc_web__WEBPACK_IMPORTED_MODULE_3__.MethodType.UNARY,
            Uint8Array,
            Uint8Array,
            (v) => v,
            (v) => v,
        );

        let promise = client.unaryCall(
            hostname + grpc_route,
            send_msg_bytes,
            {},
            methodDescriptor,
        );
        promise.then((response) => {
            receiver.receive(response)
        })
    }
    return send_message_grpc
}


/***/ }),

/***/ "../../vegafusion-wasm/pkg/vegafusion_wasm.js":
/*!****************************************************!*\
  !*** ../../vegafusion-wasm/pkg/vegafusion_wasm.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MsgReceiver": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.MsgReceiver),
/* harmony export */   "__wbg_addDataListener_456995b220390fcc": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_addDataListener_456995b220390fcc),
/* harmony export */   "__wbg_addSignalListener_a5e9038b891854bf": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_addSignalListener_a5e9038b891854bf),
/* harmony export */   "__wbg_buffer_397eaa4d72ee94dd": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_buffer_397eaa4d72ee94dd),
/* harmony export */   "__wbg_call_888d259a5fefc347": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_call_888d259a5fefc347),
/* harmony export */   "__wbg_call_8a893cac80deeb51": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_call_8a893cac80deeb51),
/* harmony export */   "__wbg_document_1c64944725c0d81d": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_document_1c64944725c0d81d),
/* harmony export */   "__wbg_error_09919627ac0992f5": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_error_09919627ac0992f5),
/* harmony export */   "__wbg_getTimezoneOffset_d3e5a22a1b7fb1d8": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_getTimezoneOffset_d3e5a22a1b7fb1d8),
/* harmony export */   "__wbg_globalThis_3f735a5746d41fbd": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_globalThis_3f735a5746d41fbd),
/* harmony export */   "__wbg_global_1bc0b39582740e95": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_global_1bc0b39582740e95),
/* harmony export */   "__wbg_hover_a39bfd113c0ce79a": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_hover_a39bfd113c0ce79a),
/* harmony export */   "__wbg_initialize_a8353b0d8d0972b6": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_initialize_a8353b0d8d0972b6),
/* harmony export */   "__wbg_instanceof_Window_c4b70662a0d2c5ec": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_instanceof_Window_c4b70662a0d2c5ec),
/* harmony export */   "__wbg_localTimezone_5cf6ae3c216ea328": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_localTimezone_5cf6ae3c216ea328),
/* harmony export */   "__wbg_log_9539b89e3b2388e4": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_log_9539b89e3b2388e4),
/* harmony export */   "__wbg_makegrpcsendmessagefn_8c78e0b86571e064": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_makegrpcsendmessagefn_8c78e0b86571e064),
/* harmony export */   "__wbg_msgreceiver_new": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_msgreceiver_new),
/* harmony export */   "__wbg_new0_fd3a3a290b25cdac": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_new0_fd3a3a290b25cdac),
/* harmony export */   "__wbg_new_028cf17de51aff60": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_new_028cf17de51aff60),
/* harmony export */   "__wbg_new_693216e109162396": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_new_693216e109162396),
/* harmony export */   "__wbg_new_a7ce447f15ff496f": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_new_a7ce447f15ff496f),
/* harmony export */   "__wbg_newnoargs_be86524d73f67598": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_newnoargs_be86524d73f67598),
/* harmony export */   "__wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff),
/* harmony export */   "__wbg_parse_6b72b788b27befad": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_parse_6b72b788b27befad),
/* harmony export */   "__wbg_run_225748bf1790e173": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_run_225748bf1790e173),
/* harmony export */   "__wbg_self_c6fbdfc2918d5e58": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_self_c6fbdfc2918d5e58),
/* harmony export */   "__wbg_setDataValue_efb68a2714885f8f": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_setDataValue_efb68a2714885f8f),
/* harmony export */   "__wbg_setSignalValue_da3d818ea510b40c": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_setSignalValue_da3d818ea510b40c),
/* harmony export */   "__wbg_setupTooltip_d7bb97330f0eaeb1": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_setupTooltip_d7bb97330f0eaeb1),
/* harmony export */   "__wbg_stack_0ddaca5d1abfb52f": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_stack_0ddaca5d1abfb52f),
/* harmony export */   "__wbg_toImageURL_5509edbc6b2e977a": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_toImageURL_5509edbc6b2e977a),
/* harmony export */   "__wbg_vegaversion_d841aed44b4b676c": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_vegaversion_d841aed44b4b676c),
/* harmony export */   "__wbg_window_baec038b5ab35c54": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbg_window_baec038b5ab35c54),
/* harmony export */   "__wbindgen_closure_wrapper1193": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_closure_wrapper1193),
/* harmony export */   "__wbindgen_debug_string": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_debug_string),
/* harmony export */   "__wbindgen_is_undefined": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_is_undefined),
/* harmony export */   "__wbindgen_json_parse": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_json_parse),
/* harmony export */   "__wbindgen_json_serialize": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_json_serialize),
/* harmony export */   "__wbindgen_memory": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_memory),
/* harmony export */   "__wbindgen_object_clone_ref": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_object_clone_ref),
/* harmony export */   "__wbindgen_object_drop_ref": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_object_drop_ref),
/* harmony export */   "__wbindgen_throw": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.__wbindgen_throw),
/* harmony export */   "make_grpc_send_message_fn": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.make_grpc_send_message_fn),
/* harmony export */   "render_vegafusion": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.render_vegafusion),
/* harmony export */   "vega_version": () => (/* reexport safe */ _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__.vega_version)
/* harmony export */ });
/* harmony import */ var _vegafusion_wasm_bg_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./vegafusion_wasm_bg.js */ "../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js");



/***/ }),

/***/ "../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js":
/*!*******************************************************!*\
  !*** ../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js ***!
  \*******************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render_vegafusion": () => (/* binding */ render_vegafusion),
/* harmony export */   "vega_version": () => (/* binding */ vega_version),
/* harmony export */   "make_grpc_send_message_fn": () => (/* binding */ make_grpc_send_message_fn),
/* harmony export */   "MsgReceiver": () => (/* binding */ MsgReceiver),
/* harmony export */   "__wbindgen_object_drop_ref": () => (/* binding */ __wbindgen_object_drop_ref),
/* harmony export */   "__wbg_msgreceiver_new": () => (/* binding */ __wbg_msgreceiver_new),
/* harmony export */   "__wbg_log_9539b89e3b2388e4": () => (/* binding */ __wbg_log_9539b89e3b2388e4),
/* harmony export */   "__wbg_setSignalValue_da3d818ea510b40c": () => (/* binding */ __wbg_setSignalValue_da3d818ea510b40c),
/* harmony export */   "__wbg_setDataValue_efb68a2714885f8f": () => (/* binding */ __wbg_setDataValue_efb68a2714885f8f),
/* harmony export */   "__wbg_run_225748bf1790e173": () => (/* binding */ __wbg_run_225748bf1790e173),
/* harmony export */   "__wbindgen_json_serialize": () => (/* binding */ __wbindgen_json_serialize),
/* harmony export */   "__wbg_toImageURL_5509edbc6b2e977a": () => (/* binding */ __wbg_toImageURL_5509edbc6b2e977a),
/* harmony export */   "__wbg_localTimezone_5cf6ae3c216ea328": () => (/* binding */ __wbg_localTimezone_5cf6ae3c216ea328),
/* harmony export */   "__wbindgen_json_parse": () => (/* binding */ __wbindgen_json_parse),
/* harmony export */   "__wbg_parse_6b72b788b27befad": () => (/* binding */ __wbg_parse_6b72b788b27befad),
/* harmony export */   "__wbg_new_028cf17de51aff60": () => (/* binding */ __wbg_new_028cf17de51aff60),
/* harmony export */   "__wbg_initialize_a8353b0d8d0972b6": () => (/* binding */ __wbg_initialize_a8353b0d8d0972b6),
/* harmony export */   "__wbg_hover_a39bfd113c0ce79a": () => (/* binding */ __wbg_hover_a39bfd113c0ce79a),
/* harmony export */   "__wbg_setupTooltip_d7bb97330f0eaeb1": () => (/* binding */ __wbg_setupTooltip_d7bb97330f0eaeb1),
/* harmony export */   "__wbindgen_object_clone_ref": () => (/* binding */ __wbindgen_object_clone_ref),
/* harmony export */   "__wbg_addSignalListener_a5e9038b891854bf": () => (/* binding */ __wbg_addSignalListener_a5e9038b891854bf),
/* harmony export */   "__wbg_addDataListener_456995b220390fcc": () => (/* binding */ __wbg_addDataListener_456995b220390fcc),
/* harmony export */   "__wbg_vegaversion_d841aed44b4b676c": () => (/* binding */ __wbg_vegaversion_d841aed44b4b676c),
/* harmony export */   "__wbg_makegrpcsendmessagefn_8c78e0b86571e064": () => (/* binding */ __wbg_makegrpcsendmessagefn_8c78e0b86571e064),
/* harmony export */   "__wbg_new_693216e109162396": () => (/* binding */ __wbg_new_693216e109162396),
/* harmony export */   "__wbg_stack_0ddaca5d1abfb52f": () => (/* binding */ __wbg_stack_0ddaca5d1abfb52f),
/* harmony export */   "__wbg_error_09919627ac0992f5": () => (/* binding */ __wbg_error_09919627ac0992f5),
/* harmony export */   "__wbg_instanceof_Window_c4b70662a0d2c5ec": () => (/* binding */ __wbg_instanceof_Window_c4b70662a0d2c5ec),
/* harmony export */   "__wbg_document_1c64944725c0d81d": () => (/* binding */ __wbg_document_1c64944725c0d81d),
/* harmony export */   "__wbg_newnoargs_be86524d73f67598": () => (/* binding */ __wbg_newnoargs_be86524d73f67598),
/* harmony export */   "__wbg_call_888d259a5fefc347": () => (/* binding */ __wbg_call_888d259a5fefc347),
/* harmony export */   "__wbg_call_8a893cac80deeb51": () => (/* binding */ __wbg_call_8a893cac80deeb51),
/* harmony export */   "__wbg_getTimezoneOffset_d3e5a22a1b7fb1d8": () => (/* binding */ __wbg_getTimezoneOffset_d3e5a22a1b7fb1d8),
/* harmony export */   "__wbg_new0_fd3a3a290b25cdac": () => (/* binding */ __wbg_new0_fd3a3a290b25cdac),
/* harmony export */   "__wbg_self_c6fbdfc2918d5e58": () => (/* binding */ __wbg_self_c6fbdfc2918d5e58),
/* harmony export */   "__wbg_window_baec038b5ab35c54": () => (/* binding */ __wbg_window_baec038b5ab35c54),
/* harmony export */   "__wbg_globalThis_3f735a5746d41fbd": () => (/* binding */ __wbg_globalThis_3f735a5746d41fbd),
/* harmony export */   "__wbg_global_1bc0b39582740e95": () => (/* binding */ __wbg_global_1bc0b39582740e95),
/* harmony export */   "__wbindgen_is_undefined": () => (/* binding */ __wbindgen_is_undefined),
/* harmony export */   "__wbg_buffer_397eaa4d72ee94dd": () => (/* binding */ __wbg_buffer_397eaa4d72ee94dd),
/* harmony export */   "__wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff": () => (/* binding */ __wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff),
/* harmony export */   "__wbg_new_a7ce447f15ff496f": () => (/* binding */ __wbg_new_a7ce447f15ff496f),
/* harmony export */   "__wbindgen_debug_string": () => (/* binding */ __wbindgen_debug_string),
/* harmony export */   "__wbindgen_throw": () => (/* binding */ __wbindgen_throw),
/* harmony export */   "__wbindgen_memory": () => (/* binding */ __wbindgen_memory),
/* harmony export */   "__wbindgen_closure_wrapper1193": () => (/* binding */ __wbindgen_closure_wrapper1193)
/* harmony export */ });
/* harmony import */ var _snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./snippets/vegafusion-wasm-7be8a8f8730f9217/js/vega_utils.js */ "../../vegafusion-wasm/pkg/snippets/vegafusion-wasm-7be8a8f8730f9217/js/vega_utils.js");
/* harmony import */ var vega__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vega */ "../../vegafusion-wasm/node_modules/vega/build/vega.module.js");
/* harmony import */ var _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./vegafusion_wasm_bg.wasm */ "../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm");
/* module decorator */ module = __webpack_require__.hmd(module);




const heap = new Array(32).fill(undefined);

heap.push(undefined, null, true, false);

function getObject(idx) { return heap[idx]; }

let heap_next = heap.length;

function dropObject(idx) {
    if (idx < 36) return;
    heap[idx] = heap_next;
    heap_next = idx;
}

function takeObject(idx) {
    const ret = getObject(idx);
    dropObject(idx);
    return ret;
}

let WASM_VECTOR_LEN = 0;

let cachegetUint8Memory0 = null;
function getUint8Memory0() {
    if (cachegetUint8Memory0 === null || cachegetUint8Memory0.buffer !== _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer) {
        cachegetUint8Memory0 = new Uint8Array(_vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer);
    }
    return cachegetUint8Memory0;
}

const lTextEncoder = typeof TextEncoder === 'undefined' ? (0, module.require)('util').TextEncoder : TextEncoder;

let cachedTextEncoder = new lTextEncoder('utf-8');

const encodeString = (typeof cachedTextEncoder.encodeInto === 'function'
    ? function (arg, view) {
    return cachedTextEncoder.encodeInto(arg, view);
}
    : function (arg, view) {
    const buf = cachedTextEncoder.encode(arg);
    view.set(buf);
    return {
        read: arg.length,
        written: buf.length
    };
});

function passStringToWasm0(arg, malloc, realloc) {

    if (realloc === undefined) {
        const buf = cachedTextEncoder.encode(arg);
        const ptr = malloc(buf.length);
        getUint8Memory0().subarray(ptr, ptr + buf.length).set(buf);
        WASM_VECTOR_LEN = buf.length;
        return ptr;
    }

    let len = arg.length;
    let ptr = malloc(len);

    const mem = getUint8Memory0();

    let offset = 0;

    for (; offset < len; offset++) {
        const code = arg.charCodeAt(offset);
        if (code > 0x7F) break;
        mem[ptr + offset] = code;
    }

    if (offset !== len) {
        if (offset !== 0) {
            arg = arg.slice(offset);
        }
        ptr = realloc(ptr, len, len = offset + arg.length * 3);
        const view = getUint8Memory0().subarray(ptr + offset, ptr + len);
        const ret = encodeString(arg, view);

        offset += ret.written;
    }

    WASM_VECTOR_LEN = offset;
    return ptr;
}

let cachegetInt32Memory0 = null;
function getInt32Memory0() {
    if (cachegetInt32Memory0 === null || cachegetInt32Memory0.buffer !== _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer) {
        cachegetInt32Memory0 = new Int32Array(_vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer);
    }
    return cachegetInt32Memory0;
}

const lTextDecoder = typeof TextDecoder === 'undefined' ? (0, module.require)('util').TextDecoder : TextDecoder;

let cachedTextDecoder = new lTextDecoder('utf-8', { ignoreBOM: true, fatal: true });

cachedTextDecoder.decode();

function getStringFromWasm0(ptr, len) {
    return cachedTextDecoder.decode(getUint8Memory0().subarray(ptr, ptr + len));
}

function addHeapObject(obj) {
    if (heap_next === heap.length) heap.push(heap.length + 1);
    const idx = heap_next;
    heap_next = heap[idx];

    heap[idx] = obj;
    return idx;
}

function debugString(val) {
    // primitive types
    const type = typeof val;
    if (type == 'number' || type == 'boolean' || val == null) {
        return  `${val}`;
    }
    if (type == 'string') {
        return `"${val}"`;
    }
    if (type == 'symbol') {
        const description = val.description;
        if (description == null) {
            return 'Symbol';
        } else {
            return `Symbol(${description})`;
        }
    }
    if (type == 'function') {
        const name = val.name;
        if (typeof name == 'string' && name.length > 0) {
            return `Function(${name})`;
        } else {
            return 'Function';
        }
    }
    // objects
    if (Array.isArray(val)) {
        const length = val.length;
        let debug = '[';
        if (length > 0) {
            debug += debugString(val[0]);
        }
        for(let i = 1; i < length; i++) {
            debug += ', ' + debugString(val[i]);
        }
        debug += ']';
        return debug;
    }
    // Test for built-in
    const builtInMatches = /\[object ([^\]]+)\]/.exec(toString.call(val));
    let className;
    if (builtInMatches.length > 1) {
        className = builtInMatches[1];
    } else {
        // Failed to match the standard '[object ClassName]'
        return toString.call(val);
    }
    if (className == 'Object') {
        // we're a user defined class or Object
        // JSON.stringify avoids problems with cycles, and is generally much
        // easier than looping through ownProperties of `val`.
        try {
            return 'Object(' + JSON.stringify(val) + ')';
        } catch (_) {
            return 'Object';
        }
    }
    // errors
    if (val instanceof Error) {
        return `${val.name}: ${val.message}\n${val.stack}`;
    }
    // TODO we could test for more things here, like `Set`s and `Map`s.
    return className;
}

function makeMutClosure(arg0, arg1, dtor, f) {
    const state = { a: arg0, b: arg1, cnt: 1, dtor };
    const real = (...args) => {
        // First up with a closure we increment the internal reference
        // count. This ensures that the Rust closure environment won't
        // be deallocated while we're invoking it.
        state.cnt++;
        const a = state.a;
        state.a = 0;
        try {
            return f(a, state.b, ...args);
        } finally {
            if (--state.cnt === 0) {
                _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_export_2.get(state.dtor)(a, state.b);

            } else {
                state.a = a;
            }
        }
    };
    real.original = state;

    return real;
}
function __wbg_adapter_18(arg0, arg1, arg2, arg3) {
    var ptr0 = passStringToWasm0(arg2, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__._dyn_core__ops__function__FnMut__A_B___Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__h44b6a391e4ade6a7(arg0, arg1, ptr0, len0, addHeapObject(arg3));
}

function passArray8ToWasm0(arg, malloc) {
    const ptr = malloc(arg.length * 1);
    getUint8Memory0().set(arg, ptr / 1);
    WASM_VECTOR_LEN = arg.length;
    return ptr;
}

function isLikeNone(x) {
    return x === undefined || x === null;
}
/**
* @param {Element} element
* @param {string} spec_str
* @param {boolean} verbose
* @param {number} debounce_wait
* @param {number | undefined} debounce_max_wait
* @param {Function} send_msg_fn
* @returns {MsgReceiver}
*/
function render_vegafusion(element, spec_str, verbose, debounce_wait, debounce_max_wait, send_msg_fn) {
    var ptr0 = passStringToWasm0(spec_str, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    var ret = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.render_vegafusion(addHeapObject(element), ptr0, len0, verbose, debounce_wait, !isLikeNone(debounce_max_wait), isLikeNone(debounce_max_wait) ? 0 : debounce_max_wait, addHeapObject(send_msg_fn));
    return MsgReceiver.__wrap(ret);
}

/**
* @returns {string}
*/
function vega_version() {
    try {
        const retptr = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(-16);
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.vega_version(retptr);
        var r0 = getInt32Memory0()[retptr / 4 + 0];
        var r1 = getInt32Memory0()[retptr / 4 + 1];
        return getStringFromWasm0(r0, r1);
    } finally {
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(16);
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(r0, r1);
    }
}

/**
* @param {any} client
* @param {string} hostname
* @returns {Function}
*/
function make_grpc_send_message_fn(client, hostname) {
    var ptr0 = passStringToWasm0(hostname, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    var ret = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.make_grpc_send_message_fn(addHeapObject(client), ptr0, len0);
    return takeObject(ret);
}

let cachegetUint32Memory0 = null;
function getUint32Memory0() {
    if (cachegetUint32Memory0 === null || cachegetUint32Memory0.buffer !== _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer) {
        cachegetUint32Memory0 = new Uint32Array(_vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory.buffer);
    }
    return cachegetUint32Memory0;
}

function getArrayU32FromWasm0(ptr, len) {
    return getUint32Memory0().subarray(ptr / 4, ptr / 4 + len);
}

function handleError(f, args) {
    try {
        return f.apply(this, args);
    } catch (e) {
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_exn_store(addHeapObject(e));
    }
}
/**
*/
class MsgReceiver {

    static __wrap(ptr) {
        const obj = Object.create(MsgReceiver.prototype);
        obj.ptr = ptr;

        return obj;
    }

    __destroy_into_raw() {
        const ptr = this.ptr;
        this.ptr = 0;

        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbg_msgreceiver_free(ptr);
    }
    /**
    * @param {Uint8Array} bytes
    */
    receive(bytes) {
        var ptr0 = passArray8ToWasm0(bytes, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc);
        var len0 = WASM_VECTOR_LEN;
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.msgreceiver_receive(this.ptr, ptr0, len0);
    }
    /**
    * @returns {string}
    */
    client_spec_json() {
        try {
            const retptr = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(-16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.msgreceiver_client_spec_json(retptr, this.ptr);
            var r0 = getInt32Memory0()[retptr / 4 + 0];
            var r1 = getInt32Memory0()[retptr / 4 + 1];
            return getStringFromWasm0(r0, r1);
        } finally {
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(r0, r1);
        }
    }
    /**
    * @returns {string}
    */
    server_spec_json() {
        try {
            const retptr = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(-16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.msgreceiver_server_spec_json(retptr, this.ptr);
            var r0 = getInt32Memory0()[retptr / 4 + 0];
            var r1 = getInt32Memory0()[retptr / 4 + 1];
            return getStringFromWasm0(r0, r1);
        } finally {
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(r0, r1);
        }
    }
    /**
    * @returns {string}
    */
    comm_plan_json() {
        try {
            const retptr = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(-16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.msgreceiver_comm_plan_json(retptr, this.ptr);
            var r0 = getInt32Memory0()[retptr / 4 + 0];
            var r1 = getInt32Memory0()[retptr / 4 + 1];
            return getStringFromWasm0(r0, r1);
        } finally {
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_add_to_stack_pointer(16);
            _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(r0, r1);
        }
    }
    /**
    * @param {string} img_type
    * @param {number | undefined} scale_factor
    * @returns {Promise<any>}
    */
    to_image_url(img_type, scale_factor) {
        var ptr0 = passStringToWasm0(img_type, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
        var len0 = WASM_VECTOR_LEN;
        var ret = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.msgreceiver_to_image_url(this.ptr, ptr0, len0, !isLikeNone(scale_factor), isLikeNone(scale_factor) ? 0 : scale_factor);
        return takeObject(ret);
    }
}

function __wbindgen_object_drop_ref(arg0) {
    takeObject(arg0);
};

function __wbg_msgreceiver_new(arg0) {
    var ret = MsgReceiver.__wrap(arg0);
    return addHeapObject(ret);
};

function __wbg_log_9539b89e3b2388e4(arg0, arg1) {
    console.log(getStringFromWasm0(arg0, arg1));
};

function __wbg_setSignalValue_da3d818ea510b40c(arg0, arg1, arg2, arg3, arg4, arg5) {
    (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.setSignalValue)(getObject(arg0), getStringFromWasm0(arg1, arg2), getArrayU32FromWasm0(arg3, arg4), takeObject(arg5));
};

function __wbg_setDataValue_efb68a2714885f8f(arg0, arg1, arg2, arg3, arg4, arg5) {
    (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.setDataValue)(getObject(arg0), getStringFromWasm0(arg1, arg2), getArrayU32FromWasm0(arg3, arg4), takeObject(arg5));
};

function __wbg_run_225748bf1790e173(arg0) {
    getObject(arg0).run();
};

function __wbindgen_json_serialize(arg0, arg1) {
    const obj = getObject(arg1);
    var ret = JSON.stringify(obj === undefined ? null : obj);
    var ptr0 = passStringToWasm0(ret, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len0;
    getInt32Memory0()[arg0 / 4 + 0] = ptr0;
};

function __wbg_toImageURL_5509edbc6b2e977a(arg0, arg1, arg2, arg3) {
    var ret = getObject(arg0).toImageURL(getStringFromWasm0(arg1, arg2), arg3);
    return addHeapObject(ret);
};

function __wbg_localTimezone_5cf6ae3c216ea328(arg0) {
    var ret = (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.localTimezone)();
    var ptr0 = passStringToWasm0(ret, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len0;
    getInt32Memory0()[arg0 / 4 + 0] = ptr0;
};

function __wbindgen_json_parse(arg0, arg1) {
    var ret = JSON.parse(getStringFromWasm0(arg0, arg1));
    return addHeapObject(ret);
};

function __wbg_parse_6b72b788b27befad(arg0) {
    var ret = (0,vega__WEBPACK_IMPORTED_MODULE_0__.parse)(takeObject(arg0));
    return addHeapObject(ret);
};

function __wbg_new_028cf17de51aff60(arg0) {
    var ret = new vega__WEBPACK_IMPORTED_MODULE_0__.View(takeObject(arg0));
    return addHeapObject(ret);
};

function __wbg_initialize_a8353b0d8d0972b6(arg0, arg1) {
    getObject(arg0).initialize(takeObject(arg1));
};

function __wbg_hover_a39bfd113c0ce79a(arg0) {
    getObject(arg0).hover();
};

function __wbg_setupTooltip_d7bb97330f0eaeb1(arg0) {
    (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.setupTooltip)(getObject(arg0));
};

function __wbindgen_object_clone_ref(arg0) {
    var ret = getObject(arg0);
    return addHeapObject(ret);
};

function __wbg_addSignalListener_a5e9038b891854bf(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8) {
    (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.addSignalListener)(getObject(arg0), getStringFromWasm0(arg1, arg2), getArrayU32FromWasm0(arg3, arg4), takeObject(arg5), arg6, arg7 === 0 ? undefined : arg8);
};

function __wbg_addDataListener_456995b220390fcc(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8) {
    (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.addDataListener)(getObject(arg0), getStringFromWasm0(arg1, arg2), getArrayU32FromWasm0(arg3, arg4), takeObject(arg5), arg6, arg7 === 0 ? undefined : arg8);
};

function __wbg_vegaversion_d841aed44b4b676c(arg0) {
    var ret = (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.vega_version)();
    var ptr0 = passStringToWasm0(ret, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len0;
    getInt32Memory0()[arg0 / 4 + 0] = ptr0;
};

function __wbg_makegrpcsendmessagefn_8c78e0b86571e064(arg0, arg1, arg2) {
    try {
        var ret = (0,_snippets_vegafusion_wasm_7be8a8f8730f9217_js_vega_utils_js__WEBPACK_IMPORTED_MODULE_2__.make_grpc_send_message_fn)(takeObject(arg0), getStringFromWasm0(arg1, arg2));
        return addHeapObject(ret);
    } finally {
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(arg1, arg2);
    }
};

function __wbg_new_693216e109162396() {
    var ret = new Error();
    return addHeapObject(ret);
};

function __wbg_stack_0ddaca5d1abfb52f(arg0, arg1) {
    var ret = getObject(arg1).stack;
    var ptr0 = passStringToWasm0(ret, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len0;
    getInt32Memory0()[arg0 / 4 + 0] = ptr0;
};

function __wbg_error_09919627ac0992f5(arg0, arg1) {
    try {
        console.error(getStringFromWasm0(arg0, arg1));
    } finally {
        _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_free(arg0, arg1);
    }
};

function __wbg_instanceof_Window_c4b70662a0d2c5ec(arg0) {
    var ret = getObject(arg0) instanceof Window;
    return ret;
};

function __wbg_document_1c64944725c0d81d(arg0) {
    var ret = getObject(arg0).document;
    return isLikeNone(ret) ? 0 : addHeapObject(ret);
};

function __wbg_newnoargs_be86524d73f67598(arg0, arg1) {
    var ret = new Function(getStringFromWasm0(arg0, arg1));
    return addHeapObject(ret);
};

function __wbg_call_888d259a5fefc347() { return handleError(function (arg0, arg1) {
    var ret = getObject(arg0).call(getObject(arg1));
    return addHeapObject(ret);
}, arguments) };

function __wbg_call_8a893cac80deeb51() { return handleError(function (arg0, arg1, arg2, arg3) {
    var ret = getObject(arg0).call(getObject(arg1), getObject(arg2), getObject(arg3));
    return addHeapObject(ret);
}, arguments) };

function __wbg_getTimezoneOffset_d3e5a22a1b7fb1d8(arg0) {
    var ret = getObject(arg0).getTimezoneOffset();
    return ret;
};

function __wbg_new0_fd3a3a290b25cdac() {
    var ret = new Date();
    return addHeapObject(ret);
};

function __wbg_self_c6fbdfc2918d5e58() { return handleError(function () {
    var ret = self.self;
    return addHeapObject(ret);
}, arguments) };

function __wbg_window_baec038b5ab35c54() { return handleError(function () {
    var ret = window.window;
    return addHeapObject(ret);
}, arguments) };

function __wbg_globalThis_3f735a5746d41fbd() { return handleError(function () {
    var ret = globalThis.globalThis;
    return addHeapObject(ret);
}, arguments) };

function __wbg_global_1bc0b39582740e95() { return handleError(function () {
    var ret = __webpack_require__.g.global;
    return addHeapObject(ret);
}, arguments) };

function __wbindgen_is_undefined(arg0) {
    var ret = getObject(arg0) === undefined;
    return ret;
};

function __wbg_buffer_397eaa4d72ee94dd(arg0) {
    var ret = getObject(arg0).buffer;
    return addHeapObject(ret);
};

function __wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff(arg0, arg1, arg2) {
    var ret = new Uint8Array(getObject(arg0), arg1 >>> 0, arg2 >>> 0);
    return addHeapObject(ret);
};

function __wbg_new_a7ce447f15ff496f(arg0) {
    var ret = new Uint8Array(getObject(arg0));
    return addHeapObject(ret);
};

function __wbindgen_debug_string(arg0, arg1) {
    var ret = debugString(getObject(arg1));
    var ptr0 = passStringToWasm0(ret, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_malloc, _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.__wbindgen_realloc);
    var len0 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len0;
    getInt32Memory0()[arg0 / 4 + 0] = ptr0;
};

function __wbindgen_throw(arg0, arg1) {
    throw new Error(getStringFromWasm0(arg0, arg1));
};

function __wbindgen_memory() {
    var ret = _vegafusion_wasm_bg_wasm__WEBPACK_IMPORTED_MODULE_1__.memory;
    return addHeapObject(ret);
};

function __wbindgen_closure_wrapper1193(arg0, arg1, arg2) {
    var ret = makeMutClosure(arg0, arg1, 210, __wbg_adapter_18);
    return addHeapObject(ret);
};



/***/ }),

/***/ "../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm":
/*!*********************************************************!*\
  !*** ../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm ***!
  \*********************************************************/
/***/ ((module, exports, __webpack_require__) => {

"use strict";
// Instantiate WebAssembly module
var wasmExports = __webpack_require__.w[module.id];
__webpack_require__.r(exports);
// export exports from WebAssembly module
for(var name in wasmExports) if(name) exports[name] = wasmExports[name];
// exec imports from WebAssembly module (for esm order)
/* harmony import */ var m0 = __webpack_require__(/*! ./vegafusion_wasm_bg.js */ "../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js");


// exec wasm module
wasmExports[""]()

/***/ })

}]);
//# sourceMappingURL=vegafusion-wasm_pkg_vegafusion_wasm_js.c3c4e811dfdf0fcb9cfc.js.map