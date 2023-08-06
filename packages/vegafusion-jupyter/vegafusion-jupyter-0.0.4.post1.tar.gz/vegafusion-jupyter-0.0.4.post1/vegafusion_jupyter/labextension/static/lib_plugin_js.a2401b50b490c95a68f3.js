"use strict";
(self["webpackChunkvegafusion_jupyter"] = self["webpackChunkvegafusion_jupyter"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ "./lib/version.js");
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



const EXTENSION_ID = 'vegafusion-jupyter:plugin';
/**
 * The example plugin.
 */
const examplePlugin = {
    id: EXTENSION_ID,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (examplePlugin);
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION,
        exports: _widget__WEBPACK_IMPORTED_MODULE_1__,
    });
}
//# sourceMappingURL=plugin.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

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
const data = __webpack_require__(/*! ../package.json */ "./package.json");
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

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "VegaFusionModel": () => (/* binding */ VegaFusionModel),
/* harmony export */   "VegaFusionView": () => (/* binding */ VegaFusionView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./version */ "./lib/version.js");
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
// -----------------------------------------------------------
// Dropdown menu implementation is based heavily on vega-embed
// (https://github.com/vega/vega-embed) which is released
// under the BSD-3-Clause License: https://github.com/vega/vega-embed/blob/next/LICENSE


class VegaFusionModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: VegaFusionModel.model_name, _model_module: VegaFusionModel.model_module, _model_module_version: VegaFusionModel.model_module_version, _view_name: VegaFusionModel.view_name, _view_module: VegaFusionModel.view_module, _view_module_version: VegaFusionModel.view_module_version, spec: null, full_vega_spec: null, client_vega_spec: null, server_vega_spec: null, vegafusion_handle: null, verbose: null, debounce_wait: 30, debounce_max_wait: 60, download_source_link: null, _request_msg: null, _response_msg: null });
    }
}
VegaFusionModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers), { 
    // Add any extra serializers here
    _request_msg: {
        serialize: (value) => {
            if (value.buffer) {
                return new DataView(value.buffer.slice(0));
            }
            else {
                return null;
            }
        },
    } });
VegaFusionModel.model_name = 'VegaFusionModel';
VegaFusionModel.model_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
VegaFusionModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
VegaFusionModel.view_name = 'VegaFusionView'; // Set to null if no view
VegaFusionModel.view_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME; // Set to null if no view
VegaFusionModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
class VegaFusionView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetView {
    async render() {
        const { embedVegaFusion } = await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_vegafusion-embed_vegafusion-embed").then(__webpack_require__.t.bind(__webpack_require__, /*! vegafusion-embed */ "webpack/sharing/consume/default/vegafusion-embed/vegafusion-embed", 23));
        this.embedVegaFusion = embedVegaFusion;
        const { compile } = await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_vega-lite_vega-lite").then(__webpack_require__.t.bind(__webpack_require__, /*! vega-lite */ "webpack/sharing/consume/default/vega-lite/vega-lite", 23));
        this.vegalite_compile = compile;
        this.value_changed();
        this.model.on('change:spec', this.value_changed, this);
        this.model.on('change:verbose', this.value_changed, this);
        this.model.on('change:debounce_wait', this.value_changed, this);
        this.model.on('change:debounce_max_wait', this.value_changed, this);
        this.model.on('change:download_source_link', this.value_changed, this);
        this.model.on('change:_response_msg', () => {
            const msgBytes = this.model.get("_response_msg");
            if (msgBytes !== null) {
                if (this.model.get("verbose")) {
                    console.log("VegaFusion(js): Received response");
                    console.log(msgBytes.buffer);
                }
                const bytes = new Uint8Array(msgBytes.buffer);
                this.vegafusion_handle.receive(bytes);
            }
        });
    }
    value_changed() {
        let spec = this.model.get('spec');
        if (spec !== null) {
            let parsed = JSON.parse(spec);
            let vega_spec_json;
            if (parsed["$schema"].endsWith("schema/vega/v5.json")) {
                vega_spec_json = spec;
            }
            else {
                // Assume we have a Vega-Lite spec, compile to vega
                let vega_spec = this.vegalite_compile(parsed);
                vega_spec_json = JSON.stringify(vega_spec.spec);
            }
            let config = {
                verbose: this.model.get("verbose") || false,
                debounce_wait: this.model.get("debounce_wait") || 30,
                debounce_max_wait: this.model.get("debounce_max_wait"),
                download_source_link: this.model.get('download_source_link')
            };
            // this.vegafusion_handle = this.embedVegaFusion(
            this.vegafusion_handle = this.embedVegaFusion(this.el, vega_spec_json, (request) => {
                if (this.model.get("verbose")) {
                    console.log("VegaFusion(js): Send request");
                }
                this.model.set("_request_msg", new DataView(request.buffer));
                this.touch();
                this.model.set("_request_msg", {});
            }, config);
            // Update vega spec properties
            this.model.set('full_vega_spec', vega_spec_json);
            this.model.set('client_vega_spec', this.vegafusion_handle.client_spec_json());
            this.model.set('server_vega_spec', this.vegafusion_handle.server_spec_json());
            this.model.set('comm_plan', this.vegafusion_handle.comm_plan_json());
            this.touch();
        }
    }
}
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"vegafusion-jupyter","version":"0.0.4","description":"Altair Jupyter Widget library that relies on VegaFusion for serverside calculations","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","dist/*.wasm","css/*.css","css/*.scss","images/*.svg"],"homepage":"https://github.com/vegafusion/vegafusion","bugs":{"url":"https://github.com/vegafusion/vegafusion/issues"},"license":"AGPL-3.0-or-later","author":{"name":"Jon Mease","email":"jonmmease@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/jonmmease/vegafusion"},"scripts":{"build:dev":"npm run build:lib && npm run build:nbextension && npm run build:labextension:dev && pip install --force-reinstall --no-deps -e .","build:prod":"npm run clean && npm run build:lib && npm run build:nbextension && npm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc && sass scss:css","build:nbextension":"webpack","clean":"npm run clean:lib && npm run clean:nbextension && npm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf vegafusion_jupyter/labextension","clean:nbextension":"rimraf vegafusion_jupyter/nbextension/* && cp src/nbextension/extension.js vegafusion_jupyter/nbextension/","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"npm run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@jupyterlab/notebook":"^3.0.0 || ^4.0.0","marked":"^4.0.10","vega-lite":"^4.17.0","vegafusion-embed":"../../javascript/vegafusion-embed"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.16.3","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"6.5.1","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","sass":"^1.45.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","svg-inline-loader":"^0.8.2","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.65.0","webpack-cli":"^4.9.1","webpack-require-from":"^1.8.6"},"jupyterlab":{"extension":"lib/plugin","outputDir":"vegafusion_jupyter/labextension/","webpackConfig":"webpack.config.experimental.js","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.a2401b50b490c95a68f3.js.map