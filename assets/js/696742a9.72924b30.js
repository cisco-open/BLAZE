"use strict";(self.webpackChunkblaze=self.webpackChunkblaze||[]).push([[87],{3905:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>h});var a=r(7294);function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function o(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,a,n=function(e,t){if(null==e)return{};var r,a,n={},i=Object.keys(e);for(a=0;a<i.length;a++)r=i[a],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)r=i[a],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}var l=a.createContext({}),c=function(e){var t=a.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):o(o({},t),e)),r},p=function(e){var t=c(e.components);return a.createElement(l.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},m=a.forwardRef((function(e,t){var r=e.components,n=e.mdxType,i=e.originalType,l=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=c(r),m=n,h=u["".concat(l,".").concat(m)]||u[m]||d[m]||i;return r?a.createElement(h,o(o({ref:t},p),{},{components:r})):a.createElement(h,o({ref:t},p))}));function h(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var i=r.length,o=new Array(i);o[0]=m;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:n,o[1]=s;for(var c=2;c<i;c++)o[c]=r[c];return a.createElement.apply(null,o)}return a.createElement.apply(null,r)}m.displayName="MDXCreateElement"},2079:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>o,default:()=>d,frontMatter:()=>i,metadata:()=>s,toc:()=>c});var a=r(7462),n=(r(7294),r(3905));const i={sidebar_position:2},o="Usage - As Easy as 1, 2, 3",s={unversionedId:"Features/usage",id:"Features/usage",title:"Usage - As Easy as 1, 2, 3",description:"The BLAZE framework operates in three stages: Build, Execute, and Interact",source:"@site/docs/Features/usage.md",sourceDirName:"Features",slug:"/Features/usage",permalink:"/BLAZE/docs/Features/usage",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/Features/usage.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Current Features",permalink:"/BLAZE/docs/Features/current-features"},next:{title:"Installation",permalink:"/BLAZE/docs/installation"}},l={},c=[{value:"Build",id:"build",level:3},{value:"Execute",id:"execute",level:3},{value:"Interact",id:"interact",level:3}],p={toc:c},u="wrapper";function d(e){let{components:t,...i}=e;return(0,n.kt)(u,(0,a.Z)({},p,i,{components:t,mdxType:"MDXLayout"}),(0,n.kt)("h1",{id:"usage---as-easy-as-1-2-3"},"Usage - As Easy as 1, 2, 3"),(0,n.kt)("p",null,"The BLAZE framework operates in three stages: ",(0,n.kt)("strong",{parentName:"p"},"Build"),", ",(0,n.kt)("strong",{parentName:"p"},"Execute"),", and ",(0,n.kt)("strong",{parentName:"p"},"Interact")),(0,n.kt)("h3",{id:"build"},"Build"),(0,n.kt)("p",null,"In the Build stage, users can ",(0,n.kt)("strong",{parentName:"p"},"specify the models, data, and processing components")," of their pipeline using a YAML format. THey can create a fresh ",(0,n.kt)("em",{parentName:"p"},"recipe")," via a block-based drag-and-drop UI, modify a pre-existing recipe, or use one directly out of the box. The YAML file contains the specifications of their custom pipeline. "),(0,n.kt)("blockquote",null,(0,n.kt)("p",{parentName:"blockquote"},"Our drag-and-drop builder tool allows one to create, visualize, upload, and download YAML recipes. ")),(0,n.kt)("p",null,"Upon completing the drag-and-drop step, users can examine their generated YAML recipes. For example, here we can examine what the generated YAML recipe looks like for a virtual meeting assistant. "),(0,n.kt)("p",null,(0,n.kt)("img",{alt:"YamlExample",src:r(7108).Z,width:"960",height:"540"})),(0,n.kt)("blockquote",null,(0,n.kt)("p",{parentName:"blockquote"},"We provide several pre-made YAML files recipes in the ",(0,n.kt)("inlineCode",{parentName:"p"},"yaml")," folder as well! ")),(0,n.kt)("h3",{id:"execute"},"Execute"),(0,n.kt)("p",null,"In the Execute stage, BLAZE utilizes the YAML file generated or chosen in the preceding stage to ",(0,n.kt)("strong",{parentName:"p"},"establish a server, hosting the appropriate models, datasets, and components as specified"),". This server servers as the heart of the pipeline, allowing users to ",(0,n.kt)("em",{parentName:"p"},"interact with their specified configuration of components")," to run their task. "),(0,n.kt)("p",null,"The following diagram represnts the architecture, illustrating how the server enables pipeline functionality. "),(0,n.kt)("p",null,(0,n.kt)("img",{alt:"Architecture",src:r(2150).Z,width:"960",height:"540"})),(0,n.kt)("blockquote",null,(0,n.kt)("p",{parentName:"blockquote"},"YAML files can be executed via the ",(0,n.kt)("inlineCode",{parentName:"p"},"run.py")," script, which is discussed in ",(0,n.kt)("strong",{parentName:"p"},"Installation")," below! ")),(0,n.kt)("h3",{id:"interact"},"Interact"),(0,n.kt)("p",null,"In the Interact stage, users can choose to interact with their hosted, active pipelines through a number of pre-build interfaces, or directly access each functionality through REST API services. Our current offering of interfaces include: "),(0,n.kt)("ul",null,(0,n.kt)("li",{parentName:"ul"},"WebApps (both in React and Dash)"),(0,n.kt)("li",{parentName:"ul"},"ChatBots (powered by WebEx, MindMeld)"),(0,n.kt)("li",{parentName:"ul"},"Plugins (both WebEx bots and WebEx Meeting Apps)"),(0,n.kt)("li",{parentName:"ul"},"Postman (or any other REST API Client)")),(0,n.kt)("p",null,"All of these interfaces are ",(0,n.kt)("strong",{parentName:"p"},(0,n.kt)("em",{parentName:"strong"},"automatically generated"))," and are ",(0,n.kt)("strong",{parentName:"p"},"specific")," to the ",(0,n.kt)("strong",{parentName:"p"},"user's pipeline"),". "),(0,n.kt)("blockquote",null,(0,n.kt)("p",{parentName:"blockquote"},"Steps to launch each of the above interfaces are discussed in the ",(0,n.kt)("strong",{parentName:"p"},"Installation")," below!")),(0,n.kt)("p",null,"Powered by BLAZE's modular design, these varying interfaces were made ",(0,n.kt)("strong",{parentName:"p"},"without a single line of code"),". All a user has to do is ",(0,n.kt)("em",{parentName:"p"},"specify their task")," in either the drag-and-drop builder or in the YAML recipe directly. "))}d.isMDXComponent=!0},2150:(e,t,r)=>{r.d(t,{Z:()=>a});const a=r.p+"assets/images/Architecture-e41c51e0646d09a53cb24678e96331b4.png"},7108:(e,t,r)=>{r.d(t,{Z:()=>a});const a=r.p+"assets/images/YAML_Example-a58248fdcc1a06101372764566be2920.png"}}]);