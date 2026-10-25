/* Preview-only adapters: no subscriptions are transmitted. */
function captureSubscriptionDraft(){return null}
function restoreSubscriptionDraft(){}
function preloadCardExports(){}
function currentEdition(){return SELECTED_EDITION||DATA.english}
function activeLessons(){return currentEdition()?.lessons||[]}
function subscriptionSection(route){const next={news:['markets','Global markets','Put the numbers in context.'],markets:['news','World & SI','Read the stories behind the markets.'],health:['recipes','Family kitchen','Take an idea into the kitchen.'],recipes:['english','Everyday English','A little practice after dinner.'],english:['home','Our world','Return to the world of James Real.']}[route];return `<section class="preview-subscribe"><div><p class="eyebrow">CONTINUE READING</p><h2>${next[1]}</h2><p>${next[2]}</p></div><a class="button" href="#${next[0]}">Visit ${next[1]} ↗</a></section>`}
