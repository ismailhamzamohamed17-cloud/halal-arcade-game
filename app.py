import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Arcade Mobile Pro: Secure Economy", 
    page_icon="🕹️", 
    layout="centered"
)

# Custom Global CSS Layout Blocks
st.markdown("""<style>
    .cab { 
        background: #060913; 
        padding: 8px; 
        border-radius: 16px; 
        border: 2px solid #1e1b4b; 
        text-align: center; 
    }
    .bn { 
        background: #0f172a; 
        padding: 12px; 
        border-radius: 10px; 
        color: #94a3b8; 
        font-family: monospace; 
        font-size: 12px;
        text-align: left; 
        margin-bottom: 10px; 
        border: 1px solid #334155;
    }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="bn"><b>🕹️ DELTA-TIME ENGINE STABILIZATION ONLINE</b><br>Pac-Man and ghost speeds are now automatically adjusted to match frame rates, running equally fast on both computers and phones!</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<style>
    body { background:#030712; margin:0; padding:4px; display:flex; flex-direction:column; align-items:center; font-family:monospace; user-select:none; -webkit-user-select:none; }
    canvas { border:3px solid #0284c7; background:#01040f; border-radius:12px; width:100%; max-width:280px; height:280px; box-shadow: 0 12px 30px rgba(0,0,0,0.6); touch-action: none; cursor: crosshair; }
    #ui { color:#fff; font-size:13px; font-weight:bold; width:280px; display:flex; justify-content:space-between; margin:6px 0; letter-spacing:0.5px; }
    #ticketVault { color: #22c55e; font-size:12px; font-weight:bold; width:280px; text-align:left; margin-bottom:4px; }
    
    .ad-container-slot {
        width: 280px; height: 50px; background: #0f172a; border: 1px dashed #334155;
        border-radius: 6px; margin-top: 15px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; color: #475569; font-size: 10px;
    }
</style></head>
<body>
    <div id="ticketVault">🎟️ TERMINAL TICKETS: <span id="tix">0</span></div>
    <div id="ui"><div id="stg">STAGE 1</div><div>🥇 <span id="sc">0</span></div><div>❤️ <span id="lv">3</span></div></div>
    <canvas id="cv" width="280" height="280"></canvas>
    <div class="ad-container-slot">
        <div style="font-weight:bold;color:#64748b;">ADVERTISEMENT AD BANNER</div>
        <div style="font-size:8px;color:#475569;">Google AdSense Responsive Unit Slot</div>
    </div>

<script>
    const canvas=document.getElementById("cv"), ctx=canvas.getContext("2d"), scEl=document.getElementById("sc"), lvEl=document.getElementById("lv"), stgEl=document.getElementById("stg"), tixEl=document.getElementById("tix");
    let score=0, lives=3, stage=1, dots=[], p={x:140,y:210,dx:0,dy:0,r:10,a:0.2,s:0.0015};
    let arcadeTickets = parseInt(localStorage.getItem("arcade_tix_vault") || "0");
    tixEl.innerText = arcadeTickets;
    let ghosts = [];

    // 🏎️ Time-smoothed base velocity speeds (pixels per millisecond)
    const pSpeed = 0.07; 
    let lastTime = 0; // Tracks clock times for delta adjustments

    const cfgs={
        1:{n:"📍 MALE' STREETS", c:"#0284c7", d:"#fbbf24", numG:1, sp:0.015, gen:()=>{for(let i=35;i<=245;i+=52)for(let j=35;j<=245;j+=52)if(!(i==140&&j==210))dots.push({x:i,y:j,v:1})}},
        2:{n:"📍 HULHUMALE' PHASE 2", c:"#f59e0b", d:"#f43f5e", numG:1, sp:0.018, gen:()=>{for(let i=40;i<=240;i+=40){dots.push({x:i,y:i,v:1});dots.push({x:i,y:280-i,v:1})}}},
        3:{n:"📍 CROSSROADS HARBOR", c:"#10b981", d:"#a855f7", numG:2, sp:0.022, gen:()=>{for(let a=0;a<Math.PI*2;a+=Math.PI/4)dots.push({x:140+Math.cos(a)*75,y:140+Math.sin(a)*75,v:1})}},
        4:{n:"📍 MAAFUSHI LAGOON", c:"#ec4899", d:"#06b6d4", numG:2, sp:0.026, gen:()=>{for(let i=30;i<=250;i+=44)dots.push({x:i,y:140,v:1}),dots.push({x:140,y:i,v:1})}},
        5:{n:"📍 BANOS ATOLL RESORT", c:"#8b5cf6", d:"#10b981", numG:2, sp:0.030, gen:()=>{for(let i=40;i<=240;i+=50)for(let j=40;j<=240;j+=50)dots.push({x:i,y:j,v:1})}},
        6:{n:"📍 DHIGURAH SHIPWRECK", c:"#3b82f6", d:"#f97316", numG:3, sp:0.034, gen:()=>{for(let i=30;i<=250;i+=35)dots.push({x:i,y:40,v:1}),dots.push({x:i,y:240,v:1})}},
        7:{n:"📍 THODDOO FARMLANDS", c:"#22c55e", d:"#eab308", numG:3, sp:0.038, gen:()=>{for(let r=30;r<=110;r+=40)for(let a=0;a<Math.PI*2;a+=Math.PI/3)dots.push({x:140+Math.cos(a)*r,y:140+Math.sin(a)*r,v:1})}},
        8:{n:"📍 GAN AIRFIELD BASE", c:"#64748b", d:"#ec4899", numG:3, sp:0.042, gen:()=>{for(let i=20;i<=260;i+=30){dots.push({x:i,y:140,v:1})}}},
        9:{n:"📍 HANIFARU BAY REEF", c:"#06b6d4", d:"#3b82f6", numG:3, sp:0.046, gen:()=>{for(let i=30;i<=250;i+=55)for(let j=30;j<=250;j+=55)dots.push({x:i,y:j,v:1})}},
        10:{n:"👑 ADDU CITY FINALS", c:"#ef4444", d:"#ffffff", numG:4, sp:0.052, gen:()=>{for(let i=20;i<=260;i+=40)for(let j=20;j<=260;j+=40)dots.push({x:i,y:j,v:1})}}
    };

    function load(n){
        stage=n; let c=cfgs[n]; stgEl.innerText=c.n; canvas.style.borderColor=c.c;
        p.x=140; p.y=210; p.dx=0; p.dy=0; dots=[]; c.gen();
        
        ghosts = [];
        const colors = ["#ef4444", "#a855f7", "#06b6d4", "#10b981"];
        for(let i=0; i<c.numG; i++) {
            ghosts.push({
                x: 40 + (i * 35),
                y: 50 + (i * 30),
                r: 9,
                c: colors[i % colors.length],
                sp: c.sp * (1 + (i * 0.12))
            });
        }
    }

    let audioCtx = null;
    function setupAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function sound(type) {
        setupAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);
        
        if (type === "waka") {
            osc.type = "triangle"; osc.frequency.setValueAtTime(450, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(750, audioCtx.currentTime + 0.06);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.06);
        } else if (type === "lose") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(380, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(60, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(100, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.5);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.5);
        } else if (type === "level") {
            osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        }
    }
    function handleScreenInput(clientX, clientY) {
        let rect = canvas.getBoundingClientRect();
        let clickX = clientX - rect.left; let clickY = clientY - rect.top;
        let centerX = rect.width / 2; let centerY = rect.height / 2;
        let dx = clickX - centerX; let dy = clickY - centerY;
        
        if (Math.abs(dx) > Math.abs(dy)) {
            if (dx > 0) { p.dx = pSpeed; p.dy = 0; } else { p.dx = -pSpeed; p.dy = 0; }
        } else {
            if (dy > 0) { p.dx = 0; p.dy = pSpeed; } else { p.dx = 0; p.dy = -pSpeed; }
        }
    }

    canvas.addEventListener("mousedown", (e) => handleScreenInput(e.clientX, e.clientY));
    canvas.addEventListener("touchstart", (e) => {
        e.preventDefault();
        if(e.touches && e.touches.length > 0) {
            handleScreenInput(e.touches[0].clientX, e.touches[0].clientY);
        }
    }, { passive: false });

    function loop(timestamp){
        if (!lastTime) lastTime = timestamp;
        let dt = timestamp - lastTime;
        if (dt > 60) dt = 60; 
        lastTime = timestamp;

        ctx.clearRect(0,0,280,280); let active=0;
        let c=cfgs[stage];

        dots.forEach(d=>{
            if(d.v){
                active++;
                ctx.beginPath();
                let dotGrad = ctx.createRadialGradient(d.x-1.2, d.y-1.5, 0.5, d.x, d.y, 4.5);
                dotGrad.addColorStop(0, "#ffffff"); dotGrad.addColorStop(0.3, c.d); dotGrad.addColorStop(1, "#030712");
                ctx.arc(d.x,d.y,4.5,0,Math.PI*2); ctx.fillStyle=dotGrad; ctx.fill(); ctx.closePath();
                
                if(Math.hypot(p.x-d.x,p.y-d.y)<p.r+4.5){
                    d.v=0; score+=10; scEl.innerText=score;
                    sound("waka");
                    arcadeTickets += 1;
                    localStorage.setItem("arcade_tix_vault", arcadeTickets.toString());
                    tixEl.innerText = arcadeTickets;
                }
            }
        });

        if(!active){
            sound("level");
            lastTime = 0; 
            if(stage<10){ alert("🎉 STAGE CLEARED!"); load(stage+1); }
            else{ alert("🏆 CAMPAIGN COMPLETE! YOU ARE THE CHAMPION!"); score=0; scEl.innerText=0; lives=3; lvEl.innerText=3; load(1); }
            requestAnimationFrame(loop); return;
        }

        p.x += p.dx * dt; 
        p.y += p.dy * dt; 
        p.x = p.x < p.r ? 280 - p.r : (p.x > 280 - p.r ? p.r : p.x); 
        p.y = p.y < p.r ? 280 - p.r : (p.y > 280 - p.r ? p.r : p.y);
        
        p.a += p.s * dt; 
        if(p.a > 0.45 || p.a < 0.05) p.s = -p.s;

        // Render 3D Pacman
        ctx.beginPath();
        let pGrad = ctx.createRadialGradient(p.x-3.5, p.y-3.5, 1.5, p.x, p.y, p.r);
        pGrad.addColorStop(0, "#ffffff"); pGrad.addColorStop(0.2, "#facc15"); pGrad.addColorStop(0.7, "#ca8a04"); pGrad.addColorStop(1, "#1e1b4b"); 
        let rot=p.dx>0?0:(p.dx<0?Math.PI:(p.dy>0?Math.PI/2:(p.dy<0?Math.PI*1.5:0)));
        ctx.arc(p.x,p.y,p.r,rot+p.a,rot+Math.PI*2-p.a); ctx.lineTo(p.x,p.y); ctx.fillStyle=pGrad; ctx.fill(); ctx.closePath();

        ghosts.forEach(g => {
            if(g.x < p.x) g.x += g.sp * dt; else g.x -= g.sp * dt; 
            if(g.y < p.y) g.y += g.sp * dt; else g.y -= g.sp * dt;
            
            ctx.beginPath();
            let gGrad = ctx.createRadialGradient(g.x+6, g.y+5, 1, g.x+9, g.y+9, g.r);
            gGrad.addColorStop(0, "#ffffff"); gGrad.addColorStop(0.25, g.c); gGrad.addColorStop(0.85, "#150002"); gGrad.addColorStop(1, "#000000");
            ctx.arc(g.x+9, g.y+9, g.r, Math.PI, 0, false); ctx.lineTo(g.x+18, g.y+18); ctx.lineTo(g.x, g.y+18); ctx.fillStyle=gGrad; ctx.fill(); ctx.closePath();

            if(Math.hypot(p.x-(g.x+9),p.y-(g.y+9))<p.r+g.r){
                lives--; lvEl.innerText=lives;
                lastTime = 0; 
                if(lives<=0){ 
                    sound("boom");
                    alert("💥 MISSION FAILURE: GAME OVER!"); score=0; scEl.innerText=0; lives=3; lvEl.innerText=3; load(1); 
                } else { 
                    sound("lose");
                    alert("💥 CAUGHT BY TRACKER!"); p.x=140; p.y=210; p.dx=0; p.dy=0; load(stage); 
                }
            }
        });

        requestAnimationFrame(loop);
    }

    const btn=document.createElement("button"); btn.innerText="🟢 RUN ARCADE PRO"; Object.assign(btn.style,{position:"absolute",top:"35%",left:"10%",width:"80%",padding:"15px",fontSize:"18px",fontWeight:"bold",background:"#0284c7",color:"#fff",border:"2px solid #38bdf8",borderRadius:"8px",zIndex:"999"});
    document.body.appendChild(btn); btn.onclick=()=>{btn.remove(); setupAudio(); sound("level"); load(1); requestAnimationFrame(loop)};
</script></body></html>
"""

st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=440, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
