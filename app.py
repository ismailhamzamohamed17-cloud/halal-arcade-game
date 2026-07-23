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
        padding: 10px; 
        border-radius: 16px; 
        border: 2px solid #1e1b4b; 
        text-align: center; 
        max-width: 400px;
        margin: auto;
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
        max-width: 380px;
        margin-left: auto;
        margin-right: auto;
    }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="bn"><b>🕹️ BALANCED CANVAS SPACING FRAMEWORK</b><br>All 10 stages have been upgraded with wide-grid calculation logic to distribute 3D tokens smoothly across the 360px display layout.</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<style>
    body { background:#030712; margin:0; padding:4px; display:flex; flex-direction:column; align-items:center; font-family:monospace; user-select:none; -webkit-user-select:none; }
    
    #arenaWrapper { position: relative; width: 360px; height: 360px; }
    canvas { border:3px solid #0284c7; background:#01040f; border-radius:12px; width:360px; height:360px; box-shadow: 0 12px 30px rgba(0,0,0,0.6); touch-action: none; cursor: crosshair; }
    
    #ui { color:#fff; font-size:14px; font-weight:bold; width:360px; display:flex; justify-content:space-between; margin:6px 0; letter-spacing:0.5px; }
    #ticketVault { color: #22c55e; font-size:13px; font-weight:bold; width:360px; text-align:left; margin-bottom:4px; }
    
    .msg-overlay { 
        position: absolute; inset: 0; background: rgba(3, 7, 18, 0.92); border-radius: 12px; 
        display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 100; color: #fff; text-align: center; padding: 15px;
    }
    .msg-title { font-size: 26px; font-weight: bold; margin-bottom: 8px; font-family: sans-serif; letter-spacing: 1px; }
    .msg-btn { margin-top: 15px; padding: 10px 24px; font-size: 14px; font-weight: bold; border-radius: 6px; border: none; cursor: pointer; text-transform: uppercase; font-family: monospace; }
    
    .overlay-clear { color: #22c55e; text-shadow: 0 0 10px rgba(34,197,94,0.4); }
    .overlay-fail { color: #ef4444; text-shadow: 0 0 10px rgba(239,68,68,0.4); }
    .overlay-win { color: #eab308; text-shadow: 0 0 12px rgba(234,179,8,0.5); }
    .overlay-warn { color: #f59e0b; text-shadow: 0 0 10px rgba(245,158,11,0.4); }

    .ad-container-slot {
        width: 360px; height: 50px; background: #0f172a; border: 1px dashed #334155;
        border-radius: 6px; margin-top: 15px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; color: #475569; font-size: 10px;
    }
</style></head>
<body>
    <div id="ticketVault">🎟️ TERMINAL TICKETS: <span id="tix">0</span></div>
    <div id="ui"><div id="stg">STAGE 1</div><div>🥇 <span id="sc">0</span></div><div>❤️ <span id="lv">3</span></div></div>

    <div id="arenaWrapper">
        <canvas id="cv" width="360" height="360"></canvas>
        
        <div id="clearScreen" class="msg-overlay">
            <div class="msg-title overlay-clear">STAGE CLEARED! 🎉</div>
            <div style="color:#94a3b8;font-size:12px;">Get ready for the next checkpoint challenge.</div>
            <button class="msg-btn" style="background:#22c55e;color:#000;" onclick="confirmAdvance()">CONTINUE MISSION ➡️</button>
        </div>

        <div id="caughtScreen" class="msg-overlay">
            <div class="msg-title overlay-warn">CAUGHT BY GHOST! 💥</div>
            <div style="color:#94a3b8;font-size:12px;">Resetting position. Be careful, officer!</div>
            <button class="msg-btn" style="background:#f59e0b;color:#000;" onclick="confirmRespawn()">RESPAWN HERO 🛡️</button>
        </div>

        <div id="failScreen" class="msg-overlay">
            <div class="msg-title overlay-fail">GAME OVER 💀</div>
            <div id="finalScoreInfo" style="color:#94a3b8;font-size:12px;margin-bottom:5px;">Your final score has been saved.</div>
            <button class="msg-btn" style="background:#ef4444;color:#fff;" onclick="confirmRestart()">RETRY MISSION 🔄</button>
        </div>

        <div id="victoryScreen" class="msg-overlay">
            <div class="msg-title overlay-win">CONGRATULATIONS! 🏆</div>
            <div style="color:#fff;font-size:13px;font-weight:bold;line-height:1.4;">YOU FINISHED THE GAME!<br>You are the Ultimate Arcade Champion!</div>
            <button class="msg-btn" style="background:#eab308;color:#000;" onclick="confirmRestart()">PLAY AGAIN 🎮</button>
        </div>
    </div>
    <div class="ad-container-slot">
        <div style="font-weight:bold;color:#64748b;">ADVERTISEMENT AD BANNER</div>
        <div style="font-size:8px;color:#475569;">Google AdSense Responsive Unit Slot</div>
    </div>

<script>
    const canvas=document.getElementById("cv"), ctx=canvas.getContext("2d"), scEl=document.getElementById("sc"), lvEl=document.getElementById("lv"), stgEl=document.getElementById("stg"), tixEl=document.getElementById("tix");
    const clearScreen=document.getElementById("clearScreen"), failScreen=document.getElementById("failScreen"), victoryScreen=document.getElementById("victoryScreen"), caughtScreen=document.getElementById("caughtScreen");
    
    let score=0, lives=3, stage=1, dots=[], p={x:180,y:260,dx:0,dy:0,r:12,a:0.2,s:0.0015};
    let arcadeTickets = parseInt(localStorage.getItem("arcade_tix_vault") || "0");
    tixEl.innerText = arcadeTickets;
    let ghosts = []; let gameRunning = false;

    const pSpeed = 0.085; 
    let lastTime = 0;

    // --- 🔟 BALANCED 360px POSITION GENERATION MATRIX FOR ALL 10 STAGES ---
    const cfgs={
        1:{n:"📍 MALE' STREETS", c:"#0284c7", d:"#fbbf24", numG:1, sp:0.016, gen:()=>{for(let i=40;i<=320;i+=70)for(let j=40;j<=320;j+=70)if(!(i==180&&j==260))dots.push({x:i,y:j,v:1})}},
        2:{n:"📍 HULHUMALE' PHASE 2", c:"#f59e0b", d:"#f43f5e", numG:1, sp:0.020, gen:()=>{for(let i=40;i<=320;i+=40){dots.push({x:i,y:i,v:1});dots.push({x:i,y:360-i,v:1})}}},
        3:{n:"📍 CROSSROADS HARBOR", c:"#10b981", d:"#a855f7", numG:2, sp:0.024, gen:()=>{for(let a=0;a<Math.PI*2;a+=Math.PI/5)dots.push({x:180+Math.cos(a)*110,y:180+Math.sin(a)*110,v:1})}},
        4:{n:"📍 MAAFUSHI LAGOON", c:"#ec4899", d:"#06b6d4", numG:2, sp:0.028, gen:()=>{for(let i=35;i<=325;i+=40)dots.push({x:i,y:180,v:1}),dots.push({x:180,y:i,v:1})}},
        5:{n:"📍 BANOS ATOLL RESORT", c:"#8b5cf6", d:"#10b981", numG:2, sp:0.032, gen:()=>{for(let i=45;i<=315;i+=45)for(let j=45;j<=315;j+=45)dots.push({x:i,y:j,v:1})}},
        6:{n:"📍 DHIGURAH SHIPWRECK", c:"#3b82f6", d:"#f97316", numG:3, sp:0.036, gen:()=>{for(let i=35;i<=325;i+=35)dots.push({x:i,y:55,v:1}),dots.push({x:i,y:305,v:1})}},
        7:{n:"📍 THODDOO FARMLANDS", c:"#22c55e", d:"#eab308", numG:3, sp:0.040, gen:()=>{for(let r=45;r<=135;r+=45)for(let a=0;a<Math.PI*2;a+=Math.PI/4)dots.push({x:180+Math.cos(a)*r,y:180+Math.sin(a)*r,v:1})}},
        8:{n:"📍 GAN AIRFIELD BASE", c:"#64748b", d:"#ec4899", numG:3, sp:0.044, gen:()=>{for(let i=30;i<=330;i+=30){dots.push({x:i,y:180,v:1});dots.push({x:i,y:90,v:1});dots.push({x:i,y:270,v:1})}}},
        9:{n:"📍 HANIFARU BAY REEF", c:"#06b6d4", d:"#3b82f6", numG:3, sp:0.048, gen:()=>{for(let i=45;i<=315;i+=54)for(let j=45;j<=315;j+=54)dots.push({x:i,y:j,v:1})}},
        10:{n:"👑 ADDU CITY FINALS", c:"#ef4444", d:"#ffffff", numG:4, sp:0.054, gen:()=>{for(let i=30;i<=330;i+=42)for(let j=30;j<=330;j+=42)dots.push({x:i,y:j,v:1})}}
    };

    function load(n){
        stage=n; let c=cfgs[n]; stgEl.innerText=c.n; canvas.style.borderColor=c.c;
        p.x=180; p.y=260; p.dx=0; p.dy=0; dots=[]; c.gen();
        
        ghosts = [];
        const colors = ["#ef4444", "#a855f7", "#06b6d4", "#10b981"];
        for(let i=0; i<c.numG; i++) {
            ghosts.push({
                x: 60 + (i * 65), y: 60 + (i * 45), r: 11, c: colors[i % colors.length], sp: c.sp * (1 + (i * 0.12))
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
        if (!gameRunning) return;
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

    window.confirmAdvance = function() {
        clearScreen.style.display = "none"; gameRunning = true; lastTime = 0; load(stage + 1); requestAnimationFrame(loop);
    };
    window.confirmRestart = function() {
        failScreen.style.display = "none"; victoryScreen.style.display = "none";
        score = 0; scEl.innerText = 0; lives = 3; lvEl.innerText = 3;
        gameRunning = true; lastTime = 0; load(1); requestAnimationFrame(loop);
    };
    window.confirmRespawn = function() {
        caughtScreen.style.display = "none"; gameRunning = true; lastTime = 0; p.x=180; p.y=260; p.dx=0; p.dy=0; load(stage); requestAnimationFrame(loop);
    };

    function loop(timestamp){
        if (!gameRunning) return;
        if (!lastTime) lastTime = timestamp;
        let dt = timestamp - lastTime; if (dt > 60) dt = 60; lastTime = timestamp;

        ctx.clearRect(0,0,360,360); let active=0;
        let c=cfgs[stage];

        dots.forEach(d=>{
            if(d.v){
                active++;
                ctx.beginPath();
                let dotGrad = ctx.createRadialGradient(d.x-1.5, d.y-1.5, 0.5, d.x, d.y, 5);
                dotGrad.addColorStop(0, "#ffffff"); dotGrad.addColorStop(0.3, c.d); dotGrad.addColorStop(1, "#030712");
                ctx.arc(d.x,d.y,5,0,Math.PI*2); ctx.fillStyle=dotGrad; ctx.fill(); ctx.closePath();
                
                if(Math.hypot(p.x-d.x,p.y-d.y)<p.r+5){
                    d.v=0; score+=10; scEl.innerText=score; sound("waka");
                    arcadeTickets += 1; localStorage.setItem("arcade_tix_vault", arcadeTickets.toString()); tixEl.innerText = arcadeTickets;
                }
            }
        });

        if(!active){
            gameRunning = false; sound("level");
            if(stage < 10){ clearScreen.style.display = "flex"; } 
            else { victoryScreen.style.display = "flex"; }
            return;
        }

        p.x += p.dx * dt; p.y += p.dy * dt; 
        p.x = p.x < p.r ? 360 - p.r : (p.x > 360 - p.r ? p.r : p.x); 
        p.y = p.y < p.r ? 360 - p.r : (p.y > 360 - p.r ? p.r : p.y);
        p.a += p.s * dt; if(p.a > 0.45 || p.a < 0.05) p.s = -p.s;

        // Render 3D Pacman Hero
        ctx.beginPath();
        let pGrad = ctx.createRadialGradient(p.x-4, p.y-4, 2, p.x, p.y, p.r);
        pGrad.addColorStop(0, "#ffffff"); pGrad.addColorStop(0.2, "#facc15"); pGrad.addColorStop(0.7, "#ca8a04"); pGrad.addColorStop(1, "#1e1b4b"); 
        let rot=p.dx>0?0:(p.dx<0?Math.PI:(p.dy>0?Math.PI/2:(p.dy<0?Math.PI*1.5:0)));
        ctx.arc(p.x,p.y,p.r,rot+p.a,rot+Math.PI*2-p.a); ctx.lineTo(p.x,p.y); ctx.fillStyle=pGrad; ctx.fill(); ctx.closePath();

        // Render 3D Ghosts
        ghosts.forEach(g => {
            if(g.x < p.x) g.x += g.sp * dt; else g.x -= g.sp * dt; 
            if(g.y < p.y) g.y += g.sp * dt; else g.y -= g.sp * dt;
            
            ctx.beginPath();
            let gGrad = ctx.createRadialGradient(g.x+4, g.y+4, 1, g.x+11, g.y+11, g.r);
            gGrad.addColorStop(0, "#ffffff"); gGrad.addColorStop(0.25, g.c); gGrad.addColorStop(0.85, "#150002"); gGrad.addColorStop(1, "#000000");
            ctx.arc(g.x+11, g.y+11, g.r, Math.PI, 0, false); ctx.lineTo(g.x+22, g.y+22); ctx.lineTo(g.x, g.y+22); ctx.fillStyle=gGrad; ctx.fill(); ctx.closePath();

            if(Math.hypot(p.x-(g.x+11),p.y-(g.y+11))<p.r+g.r){
                lives--; lvEl.innerText=lives;
                if(lives<=0){ 
                    gameRunning = false; sound("boom");
                    finalScoreInfo.innerText = "Final Operation Score: " + score;
                    failScreen.style.display = "flex";
                } else { 
                    gameRunning = false; sound("lose");
                    caughtScreen.style.display = "flex"; 
                }
            }
        });

        if (gameRunning) requestAnimationFrame(loop);
    }

    const btn=document.createElement("button"); btn.innerText="🟢 RUN ARCADE PRO"; Object.assign(btn.style,{position:"absolute",top:"35%",left:"10%",width:"80%",padding:"15px",fontSize:"18px",fontWeight:"bold",background:"#0284c7",color:"#fff",border:"2px solid #38bdf8",borderRadius:"8px",zIndex:"999"});
    document.body.appendChild(btn); btn.onclick=()=>{btn.remove(); setupAudio(); sound("level"); gameRunning=true; load(1); requestAnimationFrame(loop)};
</script></body></html>
"""

st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=520, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
