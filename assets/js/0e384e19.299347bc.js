"use strict";(self.webpackChunkblaze=self.webpackChunkblaze||[]).push([[671],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>f});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)n=o[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var s=a.createContext({}),p=function(e){var t=a.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},c=function(e){var t=p(e.components);return a.createElement(s.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},d=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,o=e.originalType,s=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),u=p(n),d=r,f=u["".concat(s,".").concat(d)]||u[d]||m[d]||o;return n?a.createElement(f,i(i({ref:t},c),{},{components:n})):a.createElement(f,i({ref:t},c))}));function f(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=d;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[u]="string"==typeof e?e:r,i[1]=l;for(var p=2;p<o;p++)i[p]=n[p];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}d.displayName="MDXCreateElement"},9881:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>s,contentTitle:()=>i,default:()=>m,frontMatter:()=>o,metadata:()=>l,toc:()=>p});var a=n(7462),r=(n(7294),n(3905));const o={sidebar_position:1},i="Intro",l={unversionedId:"intro",id:"intro",title:"Intro",description:"Let's discover Blaze in less than 5 minutes.",source:"@site/docs/intro.md",sourceDirName:".",slug:"/intro",permalink:"/docs/intro",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/intro.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",next:{title:"Features",permalink:"/docs/category/features"}},s={},p=[{value:"BLAZE - Building Language Applications Easily \ud83d\udd25",id:"blaze---building-language-applications-easily-",level:2},{value:"What is BLAZE?",id:"what-is-blaze",level:2}],c={toc:p},u="wrapper";function m(e){let{components:t,...n}=e;return(0,r.kt)(u,(0,a.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"intro"},"Intro"),(0,r.kt)("p",null,"Let's discover ",(0,r.kt)("strong",{parentName:"p"},"Blaze in less than 5 minutes"),"."),(0,r.kt)("h2",{id:"blaze---building-language-applications-easily-"},"BLAZE - Building Language Applications Easily \ud83d\udd25"),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},(0,r.kt)("em",{parentName:"strong"},"tl;dr"))," - Cisco Research proudly presents BLAZE, a ",(0,r.kt)("strong",{parentName:"p"},"flexible, standardized, no-code, open-source platform")," to easily ",(0,r.kt)("em",{parentName:"p"},"assemble, modify, and deploy")," various NLP models, datasets, and components"),(0,r.kt)("p",null,"Check out our ",(0,r.kt)("a",{parentName:"p",href:"https://techblog.cisco.com/"},"TechBlog")," and ",(0,r.kt)("a",{parentName:"p",href:"https://research.cisco.com/research-projects/blaze"},"Homepage")," for more information and exciting applications!"),(0,r.kt)("p",null,"Further technical documentation can also be found at our ",(0,r.kt)("a",{parentName:"p",href:"https://cisco-open.github.io/BLAZE/"},"Cisco Research GitHub Pages"),". "),(0,r.kt)("blockquote",null,(0,r.kt)("p",{parentName:"blockquote"},"Section-specific documentation can be found at the following smaller ",(0,r.kt)("inlineCode",{parentName:"p"},"README.md"),"'s:"),(0,r.kt)("ul",{parentName:"blockquote"},(0,r.kt)("li",{parentName:"ul"},"Drag-and-Drop YAML Builder - ",(0,r.kt)("a",{parentName:"li",href:"./drag/README.md"},(0,r.kt)("inlineCode",{parentName:"a"},"drag/README.md"))),(0,r.kt)("li",{parentName:"ul"},"Generated YAML Files Folder - ",(0,r.kt)("a",{parentName:"li",href:"./yaml/README.md"},(0,r.kt)("inlineCode",{parentName:"a"},"yaml/README.md"))),(0,r.kt)("li",{parentName:"ul"},"Models Usage Instructions - ",(0,r.kt)("a",{parentName:"li",href:"./backend/models/README.md"},(0,r.kt)("inlineCode",{parentName:"a"},"backend/models/README.md"))))),(0,r.kt)("h2",{id:"what-is-blaze"},"What is BLAZE?"),(0,r.kt)("p",null,"BLAZE is designed to ",(0,r.kt)("strong",{parentName:"p"},"streamline the integration of Natural Language Pipelines into software solutions"),(0,r.kt)("sup",{parentName:"p",id:"fnref-1"},(0,r.kt)("a",{parentName:"sup",href:"#fn-1",className:"footnote-ref"},"1")),". We offer an open, extensible framework to benchmark existing solutions and compare them with novel ones."),(0,r.kt)("p",null,"The building blocks of BLAZE are ",(0,r.kt)("strong",{parentName:"p"},"flexible blocks of the NLP pipeline"),". The functionality of different stages in the pipeline are abstracted out to create ",(0,r.kt)("em",{parentName:"p"},"blocks that can be combined in various ways"),". Users can arrange these Lego-like blocks to create new recipes of varying NLP pipelines. "),(0,r.kt)("p",null,"In such, BLAZE will help democratize NLP applications, providing a no-code solution to experiment with SOTA research and serving as a framework to implement NLP pipeline recipes into usable solutions. "),(0,r.kt)("div",{className:"footnotes"},(0,r.kt)("hr",{parentName:"div"}),(0,r.kt)("ol",{parentName:"div"},(0,r.kt)("li",{parentName:"ol",id:"fn-1"},"Check out our first ",(0,r.kt)("a",{parentName:"li",href:"https://techblog.cisco.com/"},"TechBlog")," to learn more about BLAZE's background! ",(0,r.kt)("a",{parentName:"li",href:"#fnref-1",className:"footnote-backref"},"\u21a9")))))}m.isMDXComponent=!0}}]);