import streamlit as st

st.set_page_config(page_title="Arcade", page_icon="🕹️", layout="centered")

st.markdown("""<style>
    .cab { background:#0b0f19; padding:10px; border-radius:16px; border:4px solid #1e1b4b; text-align:center; }
    .bn { background:#1e293b; padding:12px; border-radius:8px; color:#e2e8f0; font-family:monospace; text-align:left; margin-bottom:10px; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="bn"><b>📖 DHIVEHI PAC ADVENTURE</b><br>Clear all 3 Maldivian maps to win!</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<style>
    body { background:#000; margin:0; display:flex; flex-direction:column; align-items:center; font-family:monospace; user-select:none; }
    canvas { border:3px solid #0284c7; background:#000; border-radius:8px; max-width:100%; }
    #ui { color:#fff; font-size:16px; font-weight:bold; width:320px; display:flex; justify-content:space-between; margin:8px 0; }
    #ctl { display:grid; grid-template-columns:repeat(3,55px); gap:10px; margin-top:10px; }
    .b { background:#0284c7; color:#fff; border:2px solid #38bdf8; border-radius:50%; font-size:22px; display:flex; justify-content:center; align-items:center; height:55px; }
    .b:active { background:#075985; } .e { visibility:hidden; }
</style></head><body>
    <div id="ui"><div id="stg">STAGE 1</div><div>SCORE: <span id="sc">0</span></div><div>LIVES: <span id="lv">3</span></div></div>
    <canvas id="cv" width="320" height="320"></canvas>
    <div id="ctl">
        <div class="e"></div><div class="b" id="u">▲</div><div class="e"></div>
        <div class="b" id="l">◀</div><div class="e"></div><div class="b" id="r">▶</div>
        <div class="e"></div><div class="b" id="d">▼</div><div class="e"></div>
    </div>
<script>
    const canvas=document.getElementById("cv"), ctx=canvas.getContext("2d"), scEl=document.getElementById("sc"), lvEl=document.getElementById("lv"), stgEl=document.getElementById("stg");
    let score=0, lives=3, stage=1, dots=[], p={x:160,y:240,dx:0,dy:0,r:10,a:0.2,s:0.02}, g={x:160,y:60,sz:20,c:"#ef4444",sp:0.22};
    const cfgs={
        1:{n:"📍 MALE' STREETS",c:"#0284c7",gc:"#ef4444",sp:0.22,gen:()=>{for(let i=40;i<=280;i+=60)for(let j=40;j<=280;j+=60)if(!(i==160&&j==240))dots.push({x:i,y:j,v:1})}},
        2:{n:"📍 CROSSROADS",c:"#f59e0b",gc:"#a855f7",sp:0.26,gen:()=>{for(let i=50;i<=270;i+=50){dots.push({x:i,y:i,v:1});dots.push({x:i,y:320-i,v:1})}}},
        3:{n:"📍 CORAL REEF",c:"#10b981",gc:"#f43f5e",sp:0.30,gen:()=>{for(let a=0;a<Math.PI*2;a+=Math.PI/4)dots.push({x:160+Math.cos(a)*80,y:160+Math.sin(a)*80,v:1})}}
    };
    function load(n){
        stage=n; let c=cfgs[n]; stgEl.innerText=c.n; canvas.style.borderColor=c.c; g.c=c.gc; g.sp=c.sp;
        p.x=160; p.y=240; p.dx=0; p.dy=0; g.x=160; g.y=40; dots=[]; c.gen();
    }
    function move(d){
        if(d=='U'){p.dx=0;p.dy=-1.3} if(d=='D'){p.dx=0;p.dy=1.3} if(d=='L'){p.dx=-1.3;p.dy=0} if(d=='R'){p.dx=1.3;p.dy=0}
    }
    const bind=(id,d)=>{let el=document.getElementById(id);el.addEventListener("touchstart",(e)=>{e.preventDefault();move(d)});el.addEventListener("mousedown",()=>move(d))};
    bind("u","U"); bind("d","D"); bind("l","L"); bind("r","R");
    function loop(){
        ctx.clearRect(0,0,320,320); let active=0;
        dots.forEach(d=>{if(d.v){active++;ctx.beginPath();ctx.arc(d.x,d.y,4,0,Math.PI*2);ctx.fillStyle="#fbbf24";ctx.fill();if(Math.hypot(p.x-d.x,p.y-d.y)<p.r+4){d.v=0;score+=10;scEl.innerText=score}}});
        if(!active){if(stage<3){alert("📖 NEXT LEVEL!");load(stage+1)}else{alert("👑 CHAMPION!");score=0;scEl.innerText=0;lives=3;lvEl.innerText=3;load(1)};requestAnimationFrame(loop);return;}
        p.x+=p.dx; p.y+=p.dy; p.x=p.x<p.r?320-p.r:(p.x>320-p.r?p.r:p.x); p.y=p.y<p.r?320-p.r:(p.y>320-p.r?p.r:p.y);
        p.a+=p.s; if(p.a>0.4||p.a<0.05)p.s=-p.s;
        if(g.x<p.x)g.x+=g.sp;else g.x-=g.sp; if(g.y<p.y)g.y+=g.sp;else g.y-=g.sp;
        ctx.beginPath();let rot=p.dx>0?0:(p.dx<0?Math.PI:(p.dy>0?Math.PI/2:(p.dy<0?Math.PI*1.5:0)));ctx.arc(p.x,p.y,p.r,rot+p.a,rot+Math.PI*2-p.a);ctx.lineTo(p.x,p.y);ctx.fillStyle="#facc15";ctx.fill();ctx.closePath();
        ctx.beginPath();ctx.arc(g.x+10,g.y+10,10,Math.PI,0,false);ctx.lineTo(g.x+20,g.y+20);ctx.lineTo(g.x,g.y+20);ctx.fillStyle=g.c;ctx.fill();ctx.closePath();
        if(Math.hypot(p.x-(g.x+10),p.y-(g.y+10))<p.r+10){
            lives--; lvEl.innerText=lives;
            if(lives<=0){alert("💥 GAME OVER!");score=0;scEl.innerText=0;lives=3;lvEl.innerText=3;load(1)}
            else{alert("💥 CAUGHT!");p.x=160;p.y=240;p.dx=0;p.dy=0;g.x=160;g.y=40}
        }
        requestAnimationFrame(loop);
    }
    const btn=document.createElement("button"); btn.innerText="🟢 START GAME"; Object.assign(btn.style,{position:"absolute",top:"35%",left:"10%",width:"80%",padding:"15px",fontSize:"18px",fontWeight:"bold",background:"#0284c7",color:"#fff",border:"2px solid #38bdf8",borderRadius:"8px",zIndex:"999"});
    document.body.appendChild(btn); btn.onclick=()=>{btn.remove();load(1);loop()};
</script></body></html>"""

st.markdown('<div class="cab">', unsafe_allow_html=True)
st.components.v1.html(game_html, height=540, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)

