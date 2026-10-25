/* Google Finance destinations. Prices are shown at the source, never invented. */
const GOOGLE_QUOTES={
 '^DJI':'.DJI:INDEXDJX','^IXIC':'.IXIC:INDEXNASDAQ','^GSPC':'.INX:INDEXSP','^SOX':'SOX:INDEXNASDAQ','^RUT':'RUT:INDEXRUSSELL',
 '000001.SS':'000001:SHA','399001.SZ':'399001:SHE','000300.SS':'000300:SHA','000688.SS':'000688:SHA','399006.SZ':'399006:SHE',
 '^N225':'NI225:INDEXNIKKEI','^TOPX':'TOPIX:INDEXTOPIX','^NSEI':'NIFTY_50:INDEXNSE','^BSESN':'SENSEX:INDEXBOM','^NSEBANK':'NIFTY_BANK:INDEXNSE',
 '^HSI':'HSI:INDEXHANGSENG','^HSCE':'HSCEI:INDEXHANGSENG','HSTECH.HK':'HSTECH:INDEXHANGSENG','^GSPTSE':'OSPTX:INDEXTSI','TX60.TS':'TX60:INDEXTSI',
 '^FTSE':'UKX:INDEXFTSE','^FTMC':'MCX:INDEXFTSE','^FTAS':'ASX:INDEXFTSE','^FCHI':'PX1:INDEXEURO','^SBF120':'PX4:INDEXEURO',
 '^GDAXI':'DAX:INDEXDB','^MDAXI':'MDAX:INDEXDB','^SDAXI':'SDAX:INDEXDB','^TECDAX':'TECDAX:INDEXDB',
 '^TWII':'TAIEX:INDEXTPE','^TWOII':'TWO:INDEXTPEX','^KS11':'KOSPI:KRX','^KQ11':'KOSDAQ:KOSDAQ','^AXJO':'XJO:INDEXASX','^AORD':'XAO:INDEXASX','^TASI.SR':'TASI:INDEXTADAWUL','^SSMI':'SMI:INDEXSWX','^SPI':'SPI:INDEXSWX'
};
function googleFinanceURL(name,key){return GOOGLE_QUOTES[key]?'https://www.google.com/finance/quote/'+encodeURIComponent(GOOGLE_QUOTES[key]):'https://www.google.com/finance/?q='+encodeURIComponent(name)}
const originalMarketPage=markets;
markets=function(){return pageHead('GLOBAL MARKETS / GOOGLE FINANCE','Your markets, in one place.','Choose a benchmark to open its current Google Finance quote, chart, and source timestamp. Quotes are displayed by Google Finance and may be delayed by the exchange.')+`<p class="fine market-source-note">No AI commentary. No historical prices presented as current. <a href="https://www.google.com/googlefinance/disclaimer/" target="_blank" rel="noopener noreferrer">Exchange coverage and delays ↗</a></p><div class="market-directory">${MARKETS.map(m=>`<section class="card"><div class="section-line"><h2>${escapeHTML(m[0])}</h2><span class="fine">${escapeHTML(m[1])} · ${escapeHTML(m[3])}</span></div><ul>${m[4].map(([name,key])=>`<li><a href="${googleFinanceURL(name,key)}" target="_blank" rel="noopener noreferrer"><span>${escapeHTML(name)}</span><small>Open Google Finance ↗</small></a></li>`).join('')}</ul></section>`).join('')}</div><p class="fine">On-page quote redistribution is not enabled. For the latest available value and its delay, follow the Google Finance link. Some indices may not be covered by Google Finance.</p>`};
