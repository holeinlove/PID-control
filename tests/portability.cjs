const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert/strict'),{pathToFileURL}=require('url');
(async()=>{
const root=path.resolve(__dirname,'..'),isolated=fs.mkdtempSync(path.join(os.tmpdir(),'pid-portable-'));
const browser=await chromium.launch({channel:'chrome',headless:true}),ctx=await browser.newContext({offline:true,acceptDownloads:true,viewport:{width:1280,height:900}});
const errors=[],network=[],results=[];ctx.on('page',p=>{p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});});
for(const name of ['PID control Cart-Pole.html','index.html','PID-control-conversation.html']){
 const folder=path.join(isolated,name.replace(/\W/g,'_'));fs.mkdirSync(folder);const target=path.join(folder,name);fs.copyFileSync(path.join(root,name),target);const p=await ctx.newPage();await p.goto(pathToFileURL(target).href);
 if(name!=='PID-control-conversation.html'){
  await p.click('#balance');await p.waitForFunction(()=>lab.s.t>.3);assert.equal(await p.evaluate(()=>lab.p.kp),6);await p.click('#reset');assert.equal(await p.evaluate(()=>lab.p.V),0);await p.fill('#kp','8');await p.fill('#ki','12');await p.fill('#kd','1');await p.selectOption('#pose','near');await p.click('#restart');assert.equal(await p.evaluate(()=>lab.p.kp),8);
  const [d]=await Promise.all([p.waitForEvent('download'),p.click('#downloadStandalone')]);assert.equal(d.suggestedFilename(),'PID control Cart-Pole.html');const saved=path.join(folder,'downloaded.html');await d.saveAs(saved);const q=await ctx.newPage();await q.goto(pathToFileURL(saved).href);await q.click('#balance');await q.waitForFunction(()=>lab.s.t>.2);await q.close();
 }else{
  assert.equal(await p.locator('.turn').count(),12);await p.fill('#search','Github');assert(await p.locator('.turn:visible').count()>0);await p.click('#clear');await p.locator('#spec').evaluate(e=>e.open=true);await p.locator('#reference').evaluate(e=>e.open=true);await p.locator('img').evaluateAll(async imgs=>{for(const i of imgs){i.loading='eager';await i.decode();}});assert(await p.locator('img').count()>=6);
  await p.locator('#prototype').evaluate(e=>e.open=true);await p.click('#loadPrototype');const frame=p.frameLocator('#prototypeFrame');await frame.locator('#balance').click();await frame.locator('#reset').click();assert.equal(await frame.locator('#V').inputValue(),'0');await p.click('#stopPrototype');
  const [d]=await Promise.all([p.waitForEvent('download'),p.click('#downloadConversation')]);await d.saveAs(path.join(folder,'downloaded-conversation.html'));
 }
 await p.setViewportSize({width:320,height:800});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));results.push({file:name,status:'PASS',isolatedFile:true,offline:true,interactive:true});await p.close();
}
assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
const report={date:new Date().toISOString(),browser:browser.version(),method:'Separate directories, file:// URLs, browser offline. Not a second physical computer.',results,errors,network};fs.writeFileSync(path.join(root,'evidence/portability-tests.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
