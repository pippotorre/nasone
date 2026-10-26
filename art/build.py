import asyncio, re, os
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
svg=open(ROOT+'/art/nasone.svg').read()
BG='#efe6d2'
def fig(h): 
    w=h*280/430
    return svg.replace('<svg ',f'<svg width="{w:.1f}" height="{h:.1f}" style="display:block" ')
def tile(size, h, radius=0, bg=BG):
    return f'<style>html,body{{margin:0;background:transparent}}.t{{width:{size}px;height:{size}px;background:{bg};border-radius:{radius}px;display:grid;place-items:center}}</style><div class="t">{fig(h)}</div>'
async def shot(b, html, w, h, out, transparent=True):
    pg=await b.new_page(viewport={'width':w,'height':h}); await pg.set_content(html); await pg.screenshot(path=out, omit_background=transparent); await pg.close()
async def main():
    I=ROOT+'/img/'; S=ROOT+'/store/'
    async with async_playwright() as p:
        b=await p.chromium.launch()
        await shot(b,tile(512,410,112),512,512,I+'icon-512.png')
        await shot(b,tile(192,154,42),192,192,I+'icon-192.png')
        await shot(b,tile(48,39,11),48,48,I+'icon-48.png')
        await shot(b,tile(512,300,0),512,512,I+'icon-maskable-512.png',False)
        await shot(b,tile(180,146,0),180,180,I+'apple-touch-icon.png',False)
        await shot(b,tile(512,410,0),512,512,S+'play-icon-512.png',False)
        feat=f'''<style>html,body{{margin:0}}.f{{width:1024px;height:500px;background:linear-gradient(120deg,#f4ecda 0%,#efe6d2 55%,#e2d4b6 100%);display:flex;align-items:center;gap:56px;padding:0 90px;box-sizing:border-box;font-family:Georgia,'Times New Roman',serif;color:#3b2449}}
        h1{{font-size:112px;margin:0;letter-spacing:-2px;line-height:1}}p{{font-size:34px;margin:14px 0 0;color:#5a3a6e;font-family:system-ui,sans-serif;line-height:1.25}}</style>
        <div class="f">{fig(420)}<div><h1>Nasone</h1><p>Trova la fontanella<br>di Roma più vicina</p></div></div>'''
        await shot(b,feat,1024,500,S+'feature-graphic-1024x500.png',False)
        await b.close()
asyncio.run(main())
