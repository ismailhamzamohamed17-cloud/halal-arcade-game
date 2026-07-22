import streamlit as st

st.set_page_config(
    page_title="Arcade Mobile Pro", 
    page_icon="🕹️", 
    layout="centered"
)

st.markdown("""<style>
    .cab { 
        background:#0b0f19; 
        padding:5px; 
        border-radius:12px; 
        border:2px solid #1e1b4b; 
        text-align:center; 
    }
    .bn { 
        background:#1e293b; 
        padding:10px; 
        border-radius:8px; 
        color:#e2e8f0; 
        font-family:monospace; 
        font-size:12px;
        text-align:left; 
        margin-bottom:8px; 
    }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="bn"><b>📖 GRAPHICS ENGINE ENGAGED</b><br>Dynamic pixel-art backgrounds are loaded for each environment!</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<style>
    body { background:#000; margin:0; padding:5px; display:flex; flex-direction:column; align-items:center; font-family:monospace; user-select:none; -webkit-user-select:none; }
    canvas { border:3px solid #0284c7; background:#000; border-radius:8px; width:100%; max-width:280px; height:auto; }
    #ui { color:#fff; font-size:15px; font-weight:bold; width:280px; display:flex; justify-content:space-between; margin:4px 0; }
    #ctl { display:grid; grid-template-columns:repeat(3,60px); gap:8px; margin-top:5px; margin-bottom:15px; }
    .b { background:#0284c7; color:#fff; border:2px solid #38bdf8; border-radius:50%; font-size:24px; display:flex; justify-content:center; align-items:center; height:60px; width:60px; box-shadow:0 4px 6px rgba(0,0,0,0.3); touch-action:manipulation; }
    .b:active { background:#075985; } .e { visibility:hidden; }
</style></head><body>
    <div id="ui"><div id="stg">STAGE 1</div><div>🥇 <span id="sc">0</span></div><div>❤️ <span id="lv">3</span></div></div>
    <canvas id="cv" width="280" height="280"></canvas>
    <div id="ctl">
        <div class="e"></div><div class="b" id="u">▲</div><div class="e"></div>
        <div class="b" id="l">◀</div><div class="e"></div><div class="b" id="r">▶</div>
        <div class="e"></div><div class="b" id="d">▼</div><div class="e"></div>
    </div>
<script>
    const canvas=document.getElementById("cv"), ctx=canvas.getContext("2d"), scEl=document.getElementById("sc"), lvEl=document.getElementById("lv"), stgEl=document.getElementById("stg");
    let score=0, lives=3, stage=1, dots=[], p={x:140,y:210,dx:0,dy:0,r:9,a:0.2,s:0.02}, g={x:140,y:50,sz:18,c:"#ef4444",sp:0.22};
    
    // Create an image object in browser memory to house backgrounds
    const bgImg = new Image();

    const cfgs={
        1:{
            n:"📍 MALE' STREETS", c:"#0284c7", gc:"#ef4444", sp:0.22,
            bg:"https://unsplash.com", // Cyber street colors
            gen:()=>{for(let i=35;i<=245;i+=52)for(let j=35;j<=245;j+=52)if(!(i==140&&j==210))dots.push({x:i,y:j,v:1})}
        },
        2:{
            n:"📍 CROSSROADS", c:"#f59e0b", gc:"#a855f7", sp:0.26,
            bg:"https://unsplash.com", // Harbor lights theme
            gen:()=>{for(let i=40;i<=240;i+=40){dots.push({x:i,y:i,v:1});dots.push({x:i,y:280-i,v:1})}}
        },
        3:{
            n:"📍 CORAL REEF", c:"#10b981", gc:"#f43f5e", sp:0.30,
            bg:"https://unsplash.com", // Abyssal neon blue reef theme
            gen:()=>{for(let a=0;a<Math.PI*2;a+=Math.PI/4)dots.push({x:140+Math.cos(a)*70,y:140+Math.sin(a)*70,v:1})}
        }
    };

    function load(n){
        stage=n; let c=cfgs[n]; stgEl.innerText=c.n; canvas.style.borderColor=c.c; g.c=c.gc; g.sp=c.sp;
        bgImg.src = c.bg; // Instantly load the new web asset into memory
        p.x=140; p.y=210; p.dx=0; p.dy=0; g.x=140; g.y=35; dots=[]; c.gen();
    }
    
    function move(d){
        if(d=='U'){p.dx=0;p.dy=-1.2} if(d=='D'){p.dx=0;p.dy=1.2} if(d=='L'){p.dx=-1.2;p.dy=0} if(d=='R'){p.dx=1.2;p.dy=0}
    }
    const bind=(id,d)=>{let el=document.getElementById(id);el.addEventListener("touchstart",(e)=>{e.preventDefault();move(d)});el.addEventListener("mousedown",()=>move(d))};
    bind("u","U"); bind("d","D"); bind("l","L"); bind("r","R");
    
    function loop(){
        ctx.clearRect(0,0,280,280);
        
        // 1. Draw the background image behind the game elements
        if (bgImg.complete) {
            ctx.drawImage(bgImg, 0, 0, 280, 280);
            // Optional: Draw a dark overlay so the gold dots stay perfectly visible
            ctx.fillStyle = "rgba(0, 0, 0, 0.55)";
            ctx.fillRect(0, 0, 280, 280);
        }

        let active=0;
        dots.forEach(d=>{if(d.v){active++;ctx.beginPath();ctx.arc(d.x,d.y,4,0,Math.PI*2);ctx.fillStyle="#fbbf24";ctx.fill();if(Math.hypot(p.x-d.x,p.y-d.y)<p.r+4){d.v=0;score+=10;scEl.innerText=score}}});
        if(!active){if(stage<3){alert("📖 LEVEL CLEAR!");load(stage+1)}else{alert("👑 CHAMPION!");score=0;scEl.innerText=0;lives=3;lvEl.innerText=3;load(1)};requestAnimationFrame(loop);return;}
        
        p.x+=p.dx; p.y+=p.dy; p.x=p.x<p.r?280-p.r:(p.x>280-p.r?p.r:p.x); p.y=p.y<p.r?280-p.r:(p.y>280-p.r?p.r:p.y);
        p.a+=p.s; if(p.a>0.4||p.a<0.05)p.s=-p.s;
        if(g.x<p.x)g.x+=g.sp;else g.x-=g.sp; if(g.y<p.y)g.y+=g.sp;else g.y-=g.sp;
        
        ctx.beginPath();let rot=p.dx>0?0:(p.dx<0?Math.PI:(p.dy>0?Math.PI/2:(p.dy<0?Math.PI*1.5:0)));ctx.arc(p.x,p.y,p.r,rot+p.a,rot+Math.PI*2-p.a);ctx.lineTo(p.x,p.y);ctx.fillStyle="#facc15";ctx.fill();ctx.closePath();
        ctx.beginPath();ctx.arc(g.x+9,g.y+9,9,Math.PI,0,false);ctx.lineTo(g.x+18,g.y+18);ctx.lineTo(g.x,g.y+18);ctx.fillStyle=g.c;ctx.fill();ctx.closePath();
        
        if(Math.hypot(p.x-(g.x+9),p.y-(g.y+9))<p.r+9){
            lives--; lvEl.innerText=lives;
            if(lives<=0){alert("💥 GAME OVER!");score=0;scEl.innerText=0;lives=3;lvEl.innerText=3;load(1)}
            else{alert("💥 CAUGHT!");p.x=140;p.y=210;p.dx=0;p.dy=0;g.x=140;g.y=35}
        }
        requestAnimationFrame(loop);
    }
    const btn=document.createElement("button"); btn.innerText="🟢 START GAME"; Object.assign(btn.style,{position:"absolute",top:"35%",left:"10%",width:"80%",padding:"15px",fontSize:"18px",fontWeight:"bold",background:"#0284c7",color:"#fff",border:"2px solid #38bdf8",borderRadius:"8px",zIndex:"999"});
    document.body.appendChild(btn); btn.onclick=()=>{btn.remove();load(1);loop()};
</script></body></html>"""

st.markdown('<div class="cab">', unsafe_allow_html=True)
st.components.v1.html(game_html, height=580, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
