(this.webpackJsonphyperboard=this.webpackJsonphyperboard||[]).push([[0],{53:function(e,t,n){"use strict";n.r(t);var r=n(18),a=n(1),i=n(56),o=n.n(i),s=n(57),c=n(33),d=n(34),p={200:"\u670d\u52a1\u5668\u6210\u529f\u8fd4\u56de\u8bf7\u6c42\u7684\u6570\u636e\u3002",201:"\u65b0\u5efa\u6216\u4fee\u6539\u6570\u636e\u6210\u529f\u3002",202:"\u4e00\u4e2a\u8bf7\u6c42\u5df2\u7ecf\u8fdb\u5165\u540e\u53f0\u6392\u961f\uff08\u5f02\u6b65\u4efb\u52a1\uff09\u3002",204:"\u5220\u9664\u6570\u636e\u6210\u529f\u3002",400:"\u53d1\u51fa\u7684\u8bf7\u6c42\u6709\u9519\u8bef\uff0c\u670d\u52a1\u5668\u6ca1\u6709\u8fdb\u884c\u65b0\u5efa\u6216\u4fee\u6539\u6570\u636e\u7684\u64cd\u4f5c\u3002",401:"\u7528\u6237\u6ca1\u6709\u6743\u9650\uff08\u4ee4\u724c\u3001\u7528\u6237\u540d\u3001\u5bc6\u7801\u9519\u8bef\uff09\u3002",403:"\u7528\u6237\u5f97\u5230\u6388\u6743\uff0c\u4f46\u662f\u8bbf\u95ee\u662f\u88ab\u7981\u6b62\u7684\u3002",404:"\u53d1\u51fa\u7684\u8bf7\u6c42\u9488\u5bf9\u7684\u662f\u4e0d\u5b58\u5728\u7684\u8bb0\u5f55\uff0c\u670d\u52a1\u5668\u6ca1\u6709\u8fdb\u884c\u64cd\u4f5c\u3002",406:"\u8bf7\u6c42\u7684\u683c\u5f0f\u4e0d\u53ef\u5f97\u3002",410:"\u8bf7\u6c42\u7684\u8d44\u6e90\u88ab\u6c38\u4e45\u5220\u9664\uff0c\u4e14\u4e0d\u4f1a\u518d\u5f97\u5230\u7684\u3002",422:"\u5f53\u521b\u5efa\u4e00\u4e2a\u5bf9\u8c61\u65f6\uff0c\u53d1\u751f\u4e00\u4e2a\u9a8c\u8bc1\u9519\u8bef\u3002",500:"\u670d\u52a1\u5668\u53d1\u751f\u9519\u8bef\uff0c\u8bf7\u68c0\u67e5\u670d\u52a1\u5668\u3002",502:"\u7f51\u5173\u9519\u8bef\u3002",503:"\u670d\u52a1\u4e0d\u53ef\u7528\uff0c\u670d\u52a1\u5668\u6682\u65f6\u8fc7\u8f7d\u6216\u7ef4\u62a4\u3002",504:"\u7f51\u5173\u8d85\u65f6\u3002"};function u(e){if(e&&e.status>=200&&e.status<300)return e;var t=p[e.status]||e.statusText;s.a.error({message:"\u8bf7\u6c42\u9519\u8bef ".concat(e.status,": ").concat(e.url),description:t});var n=new Error(t);throw n.name=e.status,n.response=e,n}function h(e,t,n){var r=(t=t||{}).prefix||"";return function(e,t,n){var r=Object(a.a)(Object(a.a)({},{credentials:"include"}),t);return"POST"!==r.method&&"PUT"!==r.method&&"DELETE"!==r.method||(r.body instanceof FormData?r.headers=Object(a.a)({Accept:"application/json"},r.headers):(r.headers=Object(a.a)({Accept:"application/json, text/plain, */*","Content-Type":"application/json; charset=utf-8"},r.headers),r.body=JSON.stringify(r.body))),r.headers=Object(a.a)(Object(a.a)({},r.headers),{},{sessionId:localStorage.getItem("sessionId"),language:localStorage.getItem("intlLang")}),o()(e,r).then(u).then((function(e){try{return e.json()}catch(t){return{code:-2,data:{}}}})).then((function(e){return!0===n&&0!==e.code&&console.warn(JSON.stringify(e)),e}))}(e=e.startsWith(r)?e:Object(c.join)(r,e),t,n)}h.get=function(e,t,n){var r=!(arguments.length>3&&void 0!==arguments[3])||arguments[3];return n=n||{},h(e=t?"".concat(e,"?").concat(Object(d.stringify)(t)):e,n,r)},h.post=function(e,t,n){var r=!(arguments.length>3&&void 0!==arguments[3])||arguments[3];return(n=n||{}).body=t,n.method="POST",h(e,n,r)},h.put=function(e,t,n){var r=!(arguments.length>3&&void 0!==arguments[3])||arguments[3];return(n=n||{}).body=t||{},n.method="PUT",h(e,n,r)},h.delete=function(e,t,n){var r=!(arguments.length>3&&void 0!==arguments[3])||arguments[3];return(n=n||{}).body=t||{},n.method="DELETE",h(e,n,r)};var f=h,l=(r.experimentVis.renderDatasetSummary,r.experimentVis.experimentReducer),v=r.experimentVis.renderExperimentProcess,g=r.experimentVis.ActionType,m=(r.experimentVis.StepStatus,console);m.info(l);var y=v({status:"init",steps:[]},document.getElementById("root"));function b(e){y.dispatch(e)}var E=0,x=null;function S(){var e={begin:E};f.get("/api/events",e).then((function(e){m.info("watchNewEvents begin event "+E.toString()+", response"),m.info(JSON.stringify(e));var t=e.data.events;E+=t.length,t.forEach((function(e){b(e),function(e){var t=e.type;return t===g.ExperimentBreak||t===g.ExperimentEnd}(e)&&(m.info("checked finished event, stop the interval, id: "+x.toString()),null!==x&&clearInterval(x))}))}))}f.get("/api/events").then((function(e){console.info("response"),console.info(e);var t=e.data.events,n=!1,r={};t.forEach((function(e){r=l(r,e);var t=e.type;t!==g.ExperimentBreak&&t!==g.ExperimentEnd||(n=!0)})),b({type:g.ExperimentStart,payload:r}),n?m.info("checked experiment is finished on page start, do not start the watchNewEvent interval"):(E=t.length,x=setInterval(S,1e3),m.info("experiment not finished yet, start a interval to watch new event, interval id: "+x.toString()+", current already received "+E.toString()+" events "))}))}},[[53,1,2]]]);
//# sourceMappingURL=main.824854b4.chunk.js.map