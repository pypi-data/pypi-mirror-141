var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/vegafusion-jupyter":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base"), __webpack_require__.e("lib_plugin_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/plugin */ "./lib/plugin.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/async module */
/******/ 	(() => {
/******/ 		var webpackThen = typeof Symbol === "function" ? Symbol("webpack then") : "__webpack_then__";
/******/ 		var webpackExports = typeof Symbol === "function" ? Symbol("webpack exports") : "__webpack_exports__";
/******/ 		var completeQueue = (queue) => {
/******/ 			if(queue) {
/******/ 				queue.forEach((fn) => (fn.r--));
/******/ 				queue.forEach((fn) => (fn.r-- ? fn.r++ : fn()));
/******/ 			}
/******/ 		}
/******/ 		var completeFunction = (fn) => (!--fn.r && fn());
/******/ 		var queueFunction = (queue, fn) => (queue ? queue.push(fn) : completeFunction(fn));
/******/ 		var wrapDeps = (deps) => (deps.map((dep) => {
/******/ 			if(dep !== null && typeof dep === "object") {
/******/ 				if(dep[webpackThen]) return dep;
/******/ 				if(dep.then) {
/******/ 					var queue = [];
/******/ 					dep.then((r) => {
/******/ 						obj[webpackExports] = r;
/******/ 						completeQueue(queue);
/******/ 						queue = 0;
/******/ 					});
/******/ 					var obj = {};
/******/ 												obj[webpackThen] = (fn, reject) => (queueFunction(queue, fn), dep['catch'](reject));
/******/ 					return obj;
/******/ 				}
/******/ 			}
/******/ 			var ret = {};
/******/ 								ret[webpackThen] = (fn) => (completeFunction(fn));
/******/ 								ret[webpackExports] = dep;
/******/ 								return ret;
/******/ 		}));
/******/ 		__webpack_require__.a = (module, body, hasAwait) => {
/******/ 			var queue = hasAwait && [];
/******/ 			var exports = module.exports;
/******/ 			var currentDeps;
/******/ 			var outerResolve;
/******/ 			var reject;
/******/ 			var isEvaluating = true;
/******/ 			var nested = false;
/******/ 			var whenAll = (deps, onResolve, onReject) => {
/******/ 				if (nested) return;
/******/ 				nested = true;
/******/ 				onResolve.r += deps.length;
/******/ 				deps.map((dep, i) => (dep[webpackThen](onResolve, onReject)));
/******/ 				nested = false;
/******/ 			};
/******/ 			var promise = new Promise((resolve, rej) => {
/******/ 				reject = rej;
/******/ 				outerResolve = () => (resolve(exports), completeQueue(queue), queue = 0);
/******/ 			});
/******/ 			promise[webpackExports] = exports;
/******/ 			promise[webpackThen] = (fn, rejectFn) => {
/******/ 				if (isEvaluating) { return completeFunction(fn); }
/******/ 				if (currentDeps) whenAll(currentDeps, fn, rejectFn);
/******/ 				queueFunction(queue, fn);
/******/ 				promise['catch'](rejectFn);
/******/ 			};
/******/ 			module.exports = promise;
/******/ 			body((deps) => {
/******/ 				if(!deps) return outerResolve();
/******/ 				currentDeps = wrapDeps(deps);
/******/ 				var fn, result;
/******/ 				var promise = new Promise((resolve, reject) => {
/******/ 					fn = () => (resolve(result = currentDeps.map((d) => (d[webpackExports]))));
/******/ 					fn.r = 0;
/******/ 					whenAll(currentDeps, fn, reject);
/******/ 				});
/******/ 				return fn.r ? promise : result;
/******/ 			}).then(outerResolve, reject);
/******/ 			isEvaluating = false;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/create fake namespace object */
/******/ 	(() => {
/******/ 		var getProto = Object.getPrototypeOf ? (obj) => (Object.getPrototypeOf(obj)) : (obj) => (obj.__proto__);
/******/ 		var leafPrototypes;
/******/ 		// create a fake namespace object
/******/ 		// mode & 1: value is a module id, require it
/******/ 		// mode & 2: merge all properties of value into the ns
/******/ 		// mode & 4: return value when already ns object
/******/ 		// mode & 16: return value when it's Promise-like
/******/ 		// mode & 8|1: behave like require
/******/ 		__webpack_require__.t = function(value, mode) {
/******/ 			if(mode & 1) value = this(value);
/******/ 			if(mode & 8) return value;
/******/ 			if(typeof value === 'object' && value) {
/******/ 				if((mode & 4) && value.__esModule) return value;
/******/ 				if((mode & 16) && typeof value.then === 'function') return value;
/******/ 			}
/******/ 			var ns = Object.create(null);
/******/ 			__webpack_require__.r(ns);
/******/ 			var def = {};
/******/ 			leafPrototypes = leafPrototypes || [null, getProto({}), getProto([]), getProto(getProto)];
/******/ 			for(var current = mode & 2 && value; typeof current == 'object' && !~leafPrototypes.indexOf(current); current = getProto(current)) {
/******/ 				Object.getOwnPropertyNames(current).forEach((key) => (def[key] = () => (value[key])));
/******/ 			}
/******/ 			def['default'] = () => (value);
/******/ 			__webpack_require__.d(ns, def);
/******/ 			return ns;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"webpack_sharing_consume_default_jupyter-widgets_base":"d11655a8230743c37918","lib_index_js":"3af62f0c69a6157b2c21","lib_plugin_js":"a2401b50b490c95a68f3","vendors-node_modules_vega-lite_build_src_index_js":"73a27a8f8c09d3592f4f","vendors-javascript_vegafusion-embed_node_modules_grpc-web_index_js-node_modules_css-loader_di-1ca8f2":"1e30c053528bee415732","javascript_vegafusion-embed_lib_index_js":"3296face9376db262fb0","webpack_sharing_consume_default_vegafusion-embed_vegafusion-embed":"4b6802414118c272441f","webpack_sharing_consume_default_vega-lite_vega-lite":"caa43411934a44feeb16","vendors-vegafusion-wasm_node_modules_grpc-web_index_js-vegafusion-wasm_node_modules_lodash_lo-68e19e":"2cbf752fa1085c10a942","vegafusion-wasm_pkg_vegafusion_wasm_js":"c3c4e811dfdf0fcb9cfc"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/harmony module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.hmd = (module) => {
/******/ 			module = Object.create(module);
/******/ 			if (!module.children) module.children = [];
/******/ 			Object.defineProperty(module, 'exports', {
/******/ 				enumerable: true,
/******/ 				set: () => {
/******/ 					throw new Error('ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: ' + module.id);
/******/ 				}
/******/ 			});
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "vegafusion-jupyter:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/node module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.nmd = (module) => {
/******/ 			module.paths = [];
/******/ 			if (!module.children) module.children = [];
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "vegafusion-jupyter";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("vega-lite", "4.17.0", () => (__webpack_require__.e("vendors-node_modules_vega-lite_build_src_index_js").then(() => (() => (__webpack_require__(/*! ./node_modules/vega-lite/build/src/index.js */ "./node_modules/vega-lite/build/src/index.js"))))));
/******/ 					register("vegafusion-embed", "0.0.5", () => (Promise.all([__webpack_require__.e("vendors-javascript_vegafusion-embed_node_modules_grpc-web_index_js-node_modules_css-loader_di-1ca8f2"), __webpack_require__.e("javascript_vegafusion-embed_lib_index_js")]).then(() => (() => (__webpack_require__(/*! ../../javascript/vegafusion-embed/lib/index.js */ "../../javascript/vegafusion-embed/lib/index.js"))))));
/******/ 					register("vegafusion-jupyter", "0.0.4", () => (Promise.all([__webpack_require__.e("webpack_sharing_consume_default_jupyter-widgets_base"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/@jupyter-widgets/base": () => (loadSingletonVersionCheck("default", "@jupyter-widgets/base", [,[1,4,0,0],[1,3,0,0],[1,2,0,0],[1,1,1,10],1,1,1])),
/******/ 			"webpack/sharing/consume/default/vegafusion-embed/vegafusion-embed": () => (loadStrictVersionCheckFallback("default", "vegafusion-embed", [8,"","","/","","/javascript/vegafusion",,"embed"], () => (Promise.all([__webpack_require__.e("vendors-javascript_vegafusion-embed_node_modules_grpc-web_index_js-node_modules_css-loader_di-1ca8f2"), __webpack_require__.e("javascript_vegafusion-embed_lib_index_js")]).then(() => (() => (__webpack_require__(/*! vegafusion-embed */ "../../javascript/vegafusion-embed/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/vega-lite/vega-lite": () => (loadStrictVersionCheckFallback("default", "vega-lite", [1,4,17,0], () => (__webpack_require__.e("vendors-node_modules_vega-lite_build_src_index_js").then(() => (() => (__webpack_require__(/*! vega-lite */ "./node_modules/vega-lite/build/src/index.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_jupyter-widgets_base": [
/******/ 				"webpack/sharing/consume/default/@jupyter-widgets/base"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_vegafusion-embed_vegafusion-embed": [
/******/ 				"webpack/sharing/consume/default/vegafusion-embed/vegafusion-embed"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_vega-lite_vega-lite": [
/******/ 				"webpack/sharing/consume/default/vega-lite/vega-lite"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"vegafusion-jupyter": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(vega(\-lite_vega\-lite|fusion\-embed_vegafusion\-embed)|jupyter\-widgets_base)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkvegafusion_jupyter"] = self["webpackChunkvegafusion_jupyter"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/wasm chunk loading */
/******/ 	(() => {
/******/ 		// object to store loaded and loading wasm modules
/******/ 		var installedWasmModules = {};
/******/ 		
/******/ 		function promiseResolve() { return Promise.resolve(); }
/******/ 		
/******/ 		var wasmImportedFuncCache0;
/******/ 		var wasmImportedFuncCache1;
/******/ 		var wasmImportedFuncCache2;
/******/ 		var wasmImportedFuncCache3;
/******/ 		var wasmImportedFuncCache4;
/******/ 		var wasmImportedFuncCache5;
/******/ 		var wasmImportedFuncCache6;
/******/ 		var wasmImportedFuncCache7;
/******/ 		var wasmImportedFuncCache8;
/******/ 		var wasmImportedFuncCache9;
/******/ 		var wasmImportedFuncCache10;
/******/ 		var wasmImportedFuncCache11;
/******/ 		var wasmImportedFuncCache12;
/******/ 		var wasmImportedFuncCache13;
/******/ 		var wasmImportedFuncCache14;
/******/ 		var wasmImportedFuncCache15;
/******/ 		var wasmImportedFuncCache16;
/******/ 		var wasmImportedFuncCache17;
/******/ 		var wasmImportedFuncCache18;
/******/ 		var wasmImportedFuncCache19;
/******/ 		var wasmImportedFuncCache20;
/******/ 		var wasmImportedFuncCache21;
/******/ 		var wasmImportedFuncCache22;
/******/ 		var wasmImportedFuncCache23;
/******/ 		var wasmImportedFuncCache24;
/******/ 		var wasmImportedFuncCache25;
/******/ 		var wasmImportedFuncCache26;
/******/ 		var wasmImportedFuncCache27;
/******/ 		var wasmImportedFuncCache28;
/******/ 		var wasmImportedFuncCache29;
/******/ 		var wasmImportedFuncCache30;
/******/ 		var wasmImportedFuncCache31;
/******/ 		var wasmImportedFuncCache32;
/******/ 		var wasmImportedFuncCache33;
/******/ 		var wasmImportedFuncCache34;
/******/ 		var wasmImportedFuncCache35;
/******/ 		var wasmImportedFuncCache36;
/******/ 		var wasmImportedFuncCache37;
/******/ 		var wasmImportedFuncCache38;
/******/ 		var wasmImportedFuncCache39;
/******/ 		var wasmImportedFuncCache40;
/******/ 		var wasmImportedFuncCache41;
/******/ 		var wasmImportObjects = {
/******/ 			"../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm": function() {
/******/ 				return {
/******/ 					"./vegafusion_wasm_bg.js": {
/******/ 						"__wbindgen_object_drop_ref": function(p0i32) {
/******/ 							if(wasmImportedFuncCache0 === undefined) wasmImportedFuncCache0 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache0["__wbindgen_object_drop_ref"](p0i32);
/******/ 						},
/******/ 						"__wbg_msgreceiver_new": function(p0i32) {
/******/ 							if(wasmImportedFuncCache1 === undefined) wasmImportedFuncCache1 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache1["__wbg_msgreceiver_new"](p0i32);
/******/ 						},
/******/ 						"__wbg_log_9539b89e3b2388e4": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache2 === undefined) wasmImportedFuncCache2 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache2["__wbg_log_9539b89e3b2388e4"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_setSignalValue_da3d818ea510b40c": function(p0i32,p1i32,p2i32,p3i32,p4i32,p5i32) {
/******/ 							if(wasmImportedFuncCache3 === undefined) wasmImportedFuncCache3 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache3["__wbg_setSignalValue_da3d818ea510b40c"](p0i32,p1i32,p2i32,p3i32,p4i32,p5i32);
/******/ 						},
/******/ 						"__wbg_setDataValue_efb68a2714885f8f": function(p0i32,p1i32,p2i32,p3i32,p4i32,p5i32) {
/******/ 							if(wasmImportedFuncCache4 === undefined) wasmImportedFuncCache4 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache4["__wbg_setDataValue_efb68a2714885f8f"](p0i32,p1i32,p2i32,p3i32,p4i32,p5i32);
/******/ 						},
/******/ 						"__wbg_run_225748bf1790e173": function(p0i32) {
/******/ 							if(wasmImportedFuncCache5 === undefined) wasmImportedFuncCache5 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache5["__wbg_run_225748bf1790e173"](p0i32);
/******/ 						},
/******/ 						"__wbindgen_json_serialize": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache6 === undefined) wasmImportedFuncCache6 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache6["__wbindgen_json_serialize"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_toImageURL_5509edbc6b2e977a": function(p0i32,p1i32,p2i32,p3f64) {
/******/ 							if(wasmImportedFuncCache7 === undefined) wasmImportedFuncCache7 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache7["__wbg_toImageURL_5509edbc6b2e977a"](p0i32,p1i32,p2i32,p3f64);
/******/ 						},
/******/ 						"__wbg_localTimezone_5cf6ae3c216ea328": function(p0i32) {
/******/ 							if(wasmImportedFuncCache8 === undefined) wasmImportedFuncCache8 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache8["__wbg_localTimezone_5cf6ae3c216ea328"](p0i32);
/******/ 						},
/******/ 						"__wbindgen_json_parse": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache9 === undefined) wasmImportedFuncCache9 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache9["__wbindgen_json_parse"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_parse_6b72b788b27befad": function(p0i32) {
/******/ 							if(wasmImportedFuncCache10 === undefined) wasmImportedFuncCache10 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache10["__wbg_parse_6b72b788b27befad"](p0i32);
/******/ 						},
/******/ 						"__wbg_new_028cf17de51aff60": function(p0i32) {
/******/ 							if(wasmImportedFuncCache11 === undefined) wasmImportedFuncCache11 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache11["__wbg_new_028cf17de51aff60"](p0i32);
/******/ 						},
/******/ 						"__wbg_initialize_a8353b0d8d0972b6": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache12 === undefined) wasmImportedFuncCache12 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache12["__wbg_initialize_a8353b0d8d0972b6"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_hover_a39bfd113c0ce79a": function(p0i32) {
/******/ 							if(wasmImportedFuncCache13 === undefined) wasmImportedFuncCache13 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache13["__wbg_hover_a39bfd113c0ce79a"](p0i32);
/******/ 						},
/******/ 						"__wbg_setupTooltip_d7bb97330f0eaeb1": function(p0i32) {
/******/ 							if(wasmImportedFuncCache14 === undefined) wasmImportedFuncCache14 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache14["__wbg_setupTooltip_d7bb97330f0eaeb1"](p0i32);
/******/ 						},
/******/ 						"__wbindgen_object_clone_ref": function(p0i32) {
/******/ 							if(wasmImportedFuncCache15 === undefined) wasmImportedFuncCache15 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache15["__wbindgen_object_clone_ref"](p0i32);
/******/ 						},
/******/ 						"__wbg_addSignalListener_a5e9038b891854bf": function(p0i32,p1i32,p2i32,p3i32,p4i32,p5i32,p6f64,p7i32,p8f64) {
/******/ 							if(wasmImportedFuncCache16 === undefined) wasmImportedFuncCache16 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache16["__wbg_addSignalListener_a5e9038b891854bf"](p0i32,p1i32,p2i32,p3i32,p4i32,p5i32,p6f64,p7i32,p8f64);
/******/ 						},
/******/ 						"__wbg_addDataListener_456995b220390fcc": function(p0i32,p1i32,p2i32,p3i32,p4i32,p5i32,p6f64,p7i32,p8f64) {
/******/ 							if(wasmImportedFuncCache17 === undefined) wasmImportedFuncCache17 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache17["__wbg_addDataListener_456995b220390fcc"](p0i32,p1i32,p2i32,p3i32,p4i32,p5i32,p6f64,p7i32,p8f64);
/******/ 						},
/******/ 						"__wbg_vegaversion_d841aed44b4b676c": function(p0i32) {
/******/ 							if(wasmImportedFuncCache18 === undefined) wasmImportedFuncCache18 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache18["__wbg_vegaversion_d841aed44b4b676c"](p0i32);
/******/ 						},
/******/ 						"__wbg_makegrpcsendmessagefn_8c78e0b86571e064": function(p0i32,p1i32,p2i32) {
/******/ 							if(wasmImportedFuncCache19 === undefined) wasmImportedFuncCache19 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache19["__wbg_makegrpcsendmessagefn_8c78e0b86571e064"](p0i32,p1i32,p2i32);
/******/ 						},
/******/ 						"__wbg_new_693216e109162396": function() {
/******/ 							if(wasmImportedFuncCache20 === undefined) wasmImportedFuncCache20 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache20["__wbg_new_693216e109162396"]();
/******/ 						},
/******/ 						"__wbg_stack_0ddaca5d1abfb52f": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache21 === undefined) wasmImportedFuncCache21 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache21["__wbg_stack_0ddaca5d1abfb52f"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_error_09919627ac0992f5": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache22 === undefined) wasmImportedFuncCache22 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache22["__wbg_error_09919627ac0992f5"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_instanceof_Window_c4b70662a0d2c5ec": function(p0i32) {
/******/ 							if(wasmImportedFuncCache23 === undefined) wasmImportedFuncCache23 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache23["__wbg_instanceof_Window_c4b70662a0d2c5ec"](p0i32);
/******/ 						},
/******/ 						"__wbg_document_1c64944725c0d81d": function(p0i32) {
/******/ 							if(wasmImportedFuncCache24 === undefined) wasmImportedFuncCache24 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache24["__wbg_document_1c64944725c0d81d"](p0i32);
/******/ 						},
/******/ 						"__wbg_newnoargs_be86524d73f67598": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache25 === undefined) wasmImportedFuncCache25 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache25["__wbg_newnoargs_be86524d73f67598"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_call_888d259a5fefc347": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache26 === undefined) wasmImportedFuncCache26 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache26["__wbg_call_888d259a5fefc347"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbg_call_8a893cac80deeb51": function(p0i32,p1i32,p2i32,p3i32) {
/******/ 							if(wasmImportedFuncCache27 === undefined) wasmImportedFuncCache27 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache27["__wbg_call_8a893cac80deeb51"](p0i32,p1i32,p2i32,p3i32);
/******/ 						},
/******/ 						"__wbg_getTimezoneOffset_d3e5a22a1b7fb1d8": function(p0i32) {
/******/ 							if(wasmImportedFuncCache28 === undefined) wasmImportedFuncCache28 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache28["__wbg_getTimezoneOffset_d3e5a22a1b7fb1d8"](p0i32);
/******/ 						},
/******/ 						"__wbg_new0_fd3a3a290b25cdac": function() {
/******/ 							if(wasmImportedFuncCache29 === undefined) wasmImportedFuncCache29 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache29["__wbg_new0_fd3a3a290b25cdac"]();
/******/ 						},
/******/ 						"__wbg_self_c6fbdfc2918d5e58": function() {
/******/ 							if(wasmImportedFuncCache30 === undefined) wasmImportedFuncCache30 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache30["__wbg_self_c6fbdfc2918d5e58"]();
/******/ 						},
/******/ 						"__wbg_window_baec038b5ab35c54": function() {
/******/ 							if(wasmImportedFuncCache31 === undefined) wasmImportedFuncCache31 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache31["__wbg_window_baec038b5ab35c54"]();
/******/ 						},
/******/ 						"__wbg_globalThis_3f735a5746d41fbd": function() {
/******/ 							if(wasmImportedFuncCache32 === undefined) wasmImportedFuncCache32 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache32["__wbg_globalThis_3f735a5746d41fbd"]();
/******/ 						},
/******/ 						"__wbg_global_1bc0b39582740e95": function() {
/******/ 							if(wasmImportedFuncCache33 === undefined) wasmImportedFuncCache33 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache33["__wbg_global_1bc0b39582740e95"]();
/******/ 						},
/******/ 						"__wbindgen_is_undefined": function(p0i32) {
/******/ 							if(wasmImportedFuncCache34 === undefined) wasmImportedFuncCache34 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache34["__wbindgen_is_undefined"](p0i32);
/******/ 						},
/******/ 						"__wbg_buffer_397eaa4d72ee94dd": function(p0i32) {
/******/ 							if(wasmImportedFuncCache35 === undefined) wasmImportedFuncCache35 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache35["__wbg_buffer_397eaa4d72ee94dd"](p0i32);
/******/ 						},
/******/ 						"__wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff": function(p0i32,p1i32,p2i32) {
/******/ 							if(wasmImportedFuncCache36 === undefined) wasmImportedFuncCache36 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache36["__wbg_newwithbyteoffsetandlength_4b9b8c4e3f5adbff"](p0i32,p1i32,p2i32);
/******/ 						},
/******/ 						"__wbg_new_a7ce447f15ff496f": function(p0i32) {
/******/ 							if(wasmImportedFuncCache37 === undefined) wasmImportedFuncCache37 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache37["__wbg_new_a7ce447f15ff496f"](p0i32);
/******/ 						},
/******/ 						"__wbindgen_debug_string": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache38 === undefined) wasmImportedFuncCache38 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache38["__wbindgen_debug_string"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbindgen_throw": function(p0i32,p1i32) {
/******/ 							if(wasmImportedFuncCache39 === undefined) wasmImportedFuncCache39 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache39["__wbindgen_throw"](p0i32,p1i32);
/******/ 						},
/******/ 						"__wbindgen_memory": function() {
/******/ 							if(wasmImportedFuncCache40 === undefined) wasmImportedFuncCache40 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache40["__wbindgen_memory"]();
/******/ 						},
/******/ 						"__wbindgen_closure_wrapper1193": function(p0i32,p1i32,p2i32) {
/******/ 							if(wasmImportedFuncCache41 === undefined) wasmImportedFuncCache41 = __webpack_require__.c["../../vegafusion-wasm/pkg/vegafusion_wasm_bg.js"].exports;
/******/ 							return wasmImportedFuncCache41["__wbindgen_closure_wrapper1193"](p0i32,p1i32,p2i32);
/******/ 						}
/******/ 					}
/******/ 				};
/******/ 			},
/******/ 		};
/******/ 		
/******/ 		var wasmModuleMap = {
/******/ 			"vegafusion-wasm_pkg_vegafusion_wasm_js": [
/******/ 				"../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm"
/******/ 			]
/******/ 		};
/******/ 		
/******/ 		// object with all WebAssembly.instance exports
/******/ 		__webpack_require__.w = {};
/******/ 		
/******/ 		// Fetch + compile chunk loading for webassembly
/******/ 		__webpack_require__.f.wasm = function(chunkId, promises) {
/******/ 		
/******/ 			var wasmModules = wasmModuleMap[chunkId] || [];
/******/ 		
/******/ 			wasmModules.forEach(function(wasmModuleId, idx) {
/******/ 				var installedWasmModuleData = installedWasmModules[wasmModuleId];
/******/ 		
/******/ 				// a Promise means "currently loading" or "already loaded".
/******/ 				if(installedWasmModuleData)
/******/ 					promises.push(installedWasmModuleData);
/******/ 				else {
/******/ 					var importObject = wasmImportObjects[wasmModuleId]();
/******/ 					var req = fetch(__webpack_require__.p + "" + {"vegafusion-wasm_pkg_vegafusion_wasm_js":{"../../vegafusion-wasm/pkg/vegafusion_wasm_bg.wasm":"ce15fbd9481486e625ed"}}[chunkId][wasmModuleId] + ".module.wasm");
/******/ 					var promise;
/******/ 					if(importObject && typeof importObject.then === 'function' && typeof WebAssembly.compileStreaming === 'function') {
/******/ 						promise = Promise.all([WebAssembly.compileStreaming(req), importObject]).then(function(items) {
/******/ 							return WebAssembly.instantiate(items[0], items[1]);
/******/ 						});
/******/ 					} else if(typeof WebAssembly.instantiateStreaming === 'function') {
/******/ 						promise = WebAssembly.instantiateStreaming(req, importObject);
/******/ 					} else {
/******/ 						var bytesPromise = req.then(function(x) { return x.arrayBuffer(); });
/******/ 						promise = bytesPromise.then(function(bytes) {
/******/ 							return WebAssembly.instantiate(bytes, importObject);
/******/ 						});
/******/ 					}
/******/ 					promises.push(installedWasmModules[wasmModuleId] = promise.then(function(res) {
/******/ 						return __webpack_require__.w[wasmModuleId] = (res.instance || res).exports;
/******/ 					}));
/******/ 				}
/******/ 			});
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/vegafusion-jupyter");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB)["vegafusion-jupyter"] = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.53eb035a5b58bcc38a76.js.map