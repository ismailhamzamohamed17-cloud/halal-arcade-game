import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Coconut Hunter: Advanced 3D Arcade", 
    page_icon="🥥", 
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
        color: #e2e8f0; 
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

st.markdown('<div class="bn"><b>🥥 COCONUT HUNTER: ADVANCED 3D PIPELINE</b><br>Glitches wiped! Coconuts now feature clean 3-dot triangular pores. Characters upgraded with minimal horizontal black tracking eyes over an advanced moonlit island backdrop.</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<style>
    body { background:#030712; margin:0; padding:4px; display:flex; flex-direction:column; align-items:center; font-family:monospace; user-select:none; -webkit-user-select:none; }
    
    #arenaWrapper { position: relative; width: 360px; height: 360px; }
    /* Advanced 3D Perspective Border Frame Styling */
    canvas { border:3px solid #10b981; background:#020617; border-radius:12px; width:360px; height:360px; box-shadow: 0 16px 40px rgba(0,0,0,0.85); touch-action: none; cursor: crosshair; }
    
    #ui { color:#fff; font-size:14px; font-weight:bold; width:360px; display:flex; justify-content:space-between; margin:6px 0; letter-spacing:0.5px; }
    #ticketVault { color: #10b981; font-size:13px; font-weight:bold; width:360px; text-align:left; margin-bottom:4px; }
    
    .msg-overlay { 
        position: absolute; inset: 0; background: rgba(2, 6, 23, 0.94); border-radius: 12px; 
        display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 100; color: #fff; text-align: center; padding: 15px;
    }
    .msg-title { font-size: 26px; font-weight: bold; margin-bottom: 8px; font-family: sans-serif; letter-spacing: 1px; }
    .msg-btn { margin-top: 15px; padding: 10px 24px; font-size: 14px; font-weight: bold; border-radius: 6px; border: none; cursor: pointer; text-transform: uppercase; font-family: monospace; }
    
    .overlay-clear { color: #10b981; text-shadow: 0 0 10px rgba(16,185,129,0.4); }
    .overlay-fail { color: #ef4444; text-shadow: 0 0 10px rgba(239,68,68,0.4); }
    .overlay-win { color: #f59e0b; text-shadow: 0 0 12px rgba(245,158,11,0.5); }
    .overlay-warn { color: #f59e0b; text-shadow: 0 0 10px rgba(245,158,11,0.4); }

    .ad-container-slot {
        width: 360px; height: 50px; background: #0f172a; border: 1px dashed #1e293b;
        border-radius: 6px; margin-top: 15px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; color: #475569; font-size: 10px;
    }
</style></head>
<body>
    <div id="ticketVault">🎟️ ECO VAULT TICKETS: <span id="tix">0</span></div>
    <div id="ui"><div id="stg">STAGE 1</div><div>🥇 SCORE: <span id="sc">0</span></div><div>❤️ LIVES: <span id="lv">3</span></div></div>
    <div id="arenaWrapper">
        <canvas id="cv" width="360" height="360"></canvas>
        
        <div id="clearScreen" class="msg-overlay">
            <div class="msg-title overlay-clear">STAGE CLEARED! 🌴</div>
            <div style="color:#94a3b8;font-size:12px;">Island routes secured. Prepare for next checkpoint.</div>
            <button class="msg-btn" style="background:#10b981;color:#000;" onclick="confirmAdvance()">NEXT ISLAND ➡️</button>
        </div>

        <div id="caughtScreen" class="msg-overlay">
            <div class="msg-title overlay-warn">INTERCEPTED! 💥</div>
            <div style="color:#94a3b8;font-size:12px;">Rival hunter stole your yield. Resetting position.</div>
            <button class="msg-btn" style="background:#f59e0b;color:#000;" onclick="confirmRespawn()">REDEPLOY HUNTER 🥥</button>
        </div>

        <div id="failScreen" class="msg-overlay">
            <div class="msg-title overlay-fail">GAME OVER 💀</div>
            <div id="finalScoreInfo" style="color:#94a3b8;font-size:12px;margin-bottom:5px;">Your final harvest has been logged.</div>
            <button class="msg-btn" style="background:#ef4444;color:#fff;" onclick="confirmRestart()">RETRY HARVEST 🔄</button>
        </div>

        <div id="victoryScreen" class="msg-overlay">
            <div class="msg-title overlay-win">GRAND CHAMPION! 👑</div>
            <div style="color:#fff;font-size:13px;font-weight:bold;line-height:1.4;">YOU HARVESTED ALL 10 ISLANDS!<br>You dominate the global leaderboard!</div>
            <button class="msg-btn" style="background:#f59e0b;color:#000;" onclick="confirmRestart()">RESTART CAMPAIGN 🎮</button>
        </div>
    </div>

    <div class="ad-container-slot">
        <div style="font-weight:bold;color:#475569;">ADVERTISEMENT REVENUE STREAM</div>
        <div style="font-size:8px;color:#334155;">Google AdSense Mobile H5 SDK Container Slot</div>
    </div>

<script>
    const canvas=document.getElementById("cv"), ctx=canvas.getContext("2d"), scEl=document.getElementById("sc"), lvEl=document.getElementById("lv"), stgEl=document.getElementById("stg"), tixEl=document.getElementById("tix");
    const clearScreen=document.getElementById("clearScreen"), failScreen=document.getElementById("failScreen"), victoryScreen=document.getElementById("victoryScreen"), caughtScreen=document.getElementById("caughtScreen"), finalScoreInfo=document.getElementById("finalScoreInfo");
    
    let score=0, lives=3, stage=1, dots=[], p={x:180,y:260,dx:0,dy:0,r:13,a:0.2,s:0.0015};
    let arcadeTickets = parseInt(localStorage.getItem("arcade_tix_vault") || "0");
    tixEl.innerText = arcadeTickets;
    let ghosts = []; let gameRunning = false;

    const pSpeed = 0.085; 
    let lastTime = 0;

    const cfgs={
        1:{n:"🌴 MALE' ATOL ROAD", c:"#0284c7", d:"#78350f", numG:1, sp:0.016, gen:()=>{for(let i=40;i<=320;i+=70)for(let j=40;j<=320;j+=70)if(!(i==180&&j==260))dots.push({x:i,y:j,v:1})}},
        2:{n:"🌴 HULHUMALE' PLAINS", c:"#f59e0b", d:"#78350f", numG:1, sp:0.020, gen:()=>{for(let i=40;i<=320;i+=40){dots.push({x:i,y:i,v:1});dots.push({x:i,y:360-i,v:1})}}},
        3:{n:"🌴 CROSSROADS LAGOON", c:"#10b981", d:"#78350f", numG:2, sp:0.024, gen:()=>{for(let a=0;a<Math.PI*2;a+=Math.PI/5)dots.push({x:180+Math.cos(a)*110,y:180+Math.sin(a)*110,v:1})}},
        4:{n:"🌴 MAAFUSHI COASTS", c:"#ec4899", d:"#78350f", numG:2, sp:0.028, gen:()=>{for(let i=35;i<=325;i+=40)dots.push({x:i,y:180,v:1}),dots.push({x:180,y:i,v:1})}},
        5:{n:"🌴 BANOS SAND BAR", c:"#8b5cf6", d:"#78350f", numG:2, sp:0.032, gen:()=>{for(let i=45;i<=315;i+=45)for(let j=45;j<=315;j+=45)dots.push({x:i,y:j,v:1})}},
        6:{n:"🌴 DHIGURAH REEF BAY", c:"#3b82f6", d:"#78350f", numG:3, sp:0.036, gen:()=>{for(let i=35;i<=325;i+=35)dots.push({x:i,y:55,v:1}),dots.push({x:i,y:305,v:1})}},
        7:{n:"🌴 THODDOO COCONUT GROVE", c:"#22c55e", d:"#78350f", numG:3, sp:0.040, gen:()=>{for(let r=45;r<=135;r+=45)for(let a=0;a<Math.PI*2;a+=Math.PI/4)dots.push({x:180+Math.cos(a)*r,y:180+Math.sin(a)*r,v:1})}},
        8:{n:"🌴 GAN AIRSTRIP GRID", c:"#64748b", d:"#78350f", numG:3, sp:0.044, gen:()=>{for(let i=30;i<=330;i+=30){dots.push({x:i,y:180,v:1});dots.push({x:i,y:90,v:1});dots.push({x:i,y:270,v:1})}}},
        9:{n:"🌴 HANIFARU OCEAN WAY", c:"#06b6d4", d:"#78350f", numG:3, sp:0.048, gen:()=>{for(let i=45;i<=315;i+=54)for(let j=45;j<=315;j+=54)dots.push({x:i,y:j,v:1})}},
        10:{n:"👑 ADDU FINALS", c:"#ef4444", d:"#ffffff", numG:4, sp:0.054, gen:()=>{for(let i=30;i<=330;i+=42)for(let j=30;j<=330;j+=42)dots.push({x:i,y:j,v:1})}}
    };

    function load(n){
        stage=n; let c=cfgs[n]; stgEl.innerText=c.n; canvas.style.borderColor=c.c;
        p.x=180; p.y=260; p.dx=0; p.dy=0; dots=[]; c.gen();
        
        ghosts = [];
        const targetHunterColors = ["#ef4444", "#a855f7", "#00f0ff", "#eab308"];
        for(let i=0; i<c.numG; i++) {
            ghosts.push({
                x: 70 + (i * 60), y: 60 + (i * 50), r: 13, a: 0.2, s: 0.0015, dx: -1, dy: 0,
                c: targetHunterColors[i % targetHunterColors.length], sp: c.sp * (1 + (i * 0.12))
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
            osc.type = "triangle"; osc.frequency.setValueAtTime(420, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(700, audioCtx.currentTime + 0.06);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.06);
        } else if (type === "lose") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(350, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(90, audioCtx.currentTime);
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
            handleScreenInput(e.touches.clientX, e.touches.clientY);
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

        ctx.clearRect(0,0,360,360);

        // --- 🌅 ADVANCED 3D ENVIRONMENT: MOONLIT ISLAND COASTLINE ENGINE BACKGROUND ---
        // 1. Dark Ocean Blue Horizon Sky Gradient
        let skyGrad = ctx.createLinearGradient(0, 0, 0, 160);
        skyGrad.addColorStop(0, "#020617"); skyGrad.addColorStop(1, "#1e1b4b");
        ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, 360, 160);
        
        // 2. Layered Deep Sea Puddle Water Mesh
        let seaGrad = ctx.createLinearGradient(0, 160, 0, 360);
        seaGrad.addColorStop(0, "#030712"); seaGrad.addColorStop(1, "#022c22");
        ctx.fillStyle = seaGrad; ctx.fillRect(0, 160, 360, 200);

        // 3. Vector Shaded Curved Island Island Coastline silhouette
        ctx.beginPath(); ctx.moveTo(0, 240);
        ctx.bezierCurveTo(90, 200, 270, 290, 360, 220);
        ctx.lineTo(360, 360); ctx.lineTo(0, 360);
        ctx.fillStyle = "rgba(4, 47, 46, 0.4)"; ctx.fill(); ctx.closePath();

        let active=0;
        // --- 🥥 RENDER DETAILED COCONUTS WITH EXACT 3-DOT TRIANGULAR PORE MATRIX ---
        dots.forEach(d=>{
            if(d.v){
                active++;
                ctx.beginPath();
                let dotGrad = ctx.createRadialGradient(d.x-1.5, d.y-1.5, 0.5, d.x, d.y, 7);
                dotGrad.addColorStop(0, "#b45309"); // Shell gloss top shine highlight
                dotGrad.addColorStop(0.5, "#78350f"); // Core brown coconut meat coloring
                dotGrad.addColorStop(1, "#1e0700"); // Depth shadows edge
                ctx.arc(d.x, d.y, 7, 0, Math.PI*2); ctx.fillStyle=dotGrad; ctx.fill(); ctx.closePath();
                
                // FIXED: Draws three precise dark brown dots positioned cleanly in a triangular formation
                ctx.fillStyle = "#120300";
                ctx.beginPath(); ctx.arc(d.x, d.y - 2.5, 1, 0, Math.PI*2); ctx.fill(); ctx.closePath();     // Top corner dot
                ctx.beginPath(); ctx.arc(d.x - 2, d.y + 1.5, 1, 0, Math.PI*2); ctx.fill(); ctx.closePath();   // Bottom left corner dot
                ctx.beginPath(); ctx.arc(d.x + 2, d.y + 1.5, 1, 0, Math.PI*2); ctx.fill(); ctx.closePath();   // Bottom right corner dot
                
                if(Math.hypot(p.x-d.x,p.y-d.y)<p.r+7){
                    d.v=0; score+=10; scEl.innerText=score; sound("waka");
                    arcadeTickets += 1; localStorage.setItem("arcade_tix_vault", arcadeTickets.toString()); tixEl.innerText = arcadeTickets;
                }
            }
        });

        if(!active){
            gameRunning = false; sound("level");
            if(stage < 10){ clearScreen.style.display = "flex"; } else { victoryScreen.style.display = "flex"; }
            return;
        }

        p.x += p.dx * dt; p.y += p.dy * dt; 
        p.x = p.x < p.r ? 360 - p.r : (p.x > 360 - p.r ? p.r : p.x); 
        p.y = p.y < p.r ? 360 - p.r : (p.y > 360 - p.r ? p.r : p.y);
        p.a += p.s * dt; if(p.a > 0.45 || p.a < 0.05) p.s = -p.s;

        // --- 🥥 3D RE-SHADED COCONUT HERO DISK WITH DYNAMIC ORIENTATION LINES ---
        ctx.beginPath();
        let pGrad = ctx.createRadialGradient(p.x-4, p.y-4, 2, p.x, p.y, p.r);
        pGrad.addColorStop(0, "#fed7aa"); pGrad.addColorStop(0.3, "#92400e"); pGrad.addColorStop(0.8, "#451a03"); pGrad.addColorStop(1, "#1c0700"); 
        let rot=p.dx>0?0:(p.dx<0?Math.PI:(p.dy>0?Math.PI/2:(p.dy<0?Math.PI*1.5:0)));
        ctx.arc(p.x, p.y, p.r, rot+p.a, rot+Math.PI*2-p.a); ctx.lineTo(p.x,p.y); ctx.fillStyle=pGrad; ctx.fill(); ctx.closePath();

        // FIXED: Render sleek horizontal tracking visor band with black dot pupil eye
        let eyeAngle = rot + 0.35;
        let pEyeX = p.x + Math.cos(eyeAngle) * 5.5;
        let pEyeY = p.y + Math.sin(eyeAngle) * 5.5;
        
        // Horizontal slot shade mask background
        ctx.strokeStyle = "rgba(28, 7, 0, 0.6)"; ctx.lineWidth = 2.5; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(pEyeX - 3.5, pEyeY); ctx.lineTo(pEyeX + 3.5, pEyeY); ctx.stroke(); ctx.closePath();
        // Centered minimal sharp black dot eye
        ctx.beginPath(); ctx.arc(pEyeX, pEyeY, 1.4, 0, Math.PI*2); ctx.fillStyle = "#000000"; ctx.fill(); ctx.closePath();

        // --- 🏃 RIVAL COCONUT HUNTERS TRACKING ENGINE MESH ---
        ghosts.forEach(g => {
            if(g.x < p.x) { g.x += g.sp * dt; g.dx = 1; } else { g.x -= g.sp * dt; g.dx = -1; }
            if(g.y < p.y) { g.y += g.sp * dt; g.dy = 1; } else { g.y -= g.sp * dt; g.dy = -1; }
            
            g.a += g.s * dt; if(g.a > 0.45 || g.a < 0.05) g.s = -g.s;

            ctx.beginPath();
            let gGrad = ctx.createRadialGradient(g.x-4, g.y-4, 2, g.x, g.y, g.r);
            gGrad.addColorStop(0, "#ffffff"); gGrad.addColorStop(0.25, g.c); gGrad.addColorStop(0.8, "#090514"); gGrad.addColorStop(1, "#000000");
            let gRot = g.dx > 0 ? 0 : (g.dx < 0 ? Math.PI : (g.dy > 0 ? Math.PI/2 : 0));
            ctx.arc(g.x, g.y, g.r, gRot+g.a, gRot+Math.PI*2-g.a); ctx.lineTo(g.x, g.y); ctx.fillStyle=gGrad; ctx.fill(); ctx.closePath();

            // FIXED: Render matching minimal horizontal black dot eyes for competitive hunters
            let gEyeAngle = gRot + 0.3;
            let gEyeX = g.x + Math.cos(gEyeAngle) * 5;
            let gEyeY = g.y + Math.sin(gEyeAngle) * 5;
            
            ctx.strokeStyle = "rgba(0, 0, 0, 0.5)"; ctx.lineWidth = 2.5; ctx.lineCap = "round";
            ctx.beginPath(); ctx.moveTo(gEyeX - 3, gEyeY); ctx.lineTo(gEyeX + 3, gEyeY); ctx.stroke(); ctx.closePath();
            ctx.beginPath(); ctx.arc(gEyeX, gEyeY, 1.4, 0, Math.PI*2); ctx.fillStyle = "#000000"; ctx.fill(); ctx.closePath();

            if(Math.hypot(p.x-g.x, p.y-g.y) < p.r+g.r){
                lives--; lvEl.innerText=lives;
                if(lives<=0){ 
                    gameRunning = false; sound("boom");
                    finalScoreInfo.innerText = "Final Operation Score: " + score;
                    failScreen.style.display = "flex";
                } else { 
                    gameRunning = false; sound("lose"); caughtScreen.style.display = "flex"; 
                }
            }
        });

        if (gameRunning) requestAnimationFrame(loop);
    }
    const btn=document.createElement("button"); 
    btn.innerText="🥥 LAUNCH COCONUT HUNTER PRO"; 
    Object.assign(btn.style,{
        position:"absolute",
        top:"35%",
        left:"5%",
        width:"90%",
        padding:"15px",
        fontSize:"15px",
        fontWeight:"bold",
        background:"#10b981",
        color:"#000",
        border:"2px solid #34d399",
        borderRadius:"8px",
        zIndex:"999",
        fontFamily:"monospace"
    });
    document.body.appendChild(btn); 
    btn.onclick=()=>{
        btn.remove(); 
        setupAudio(); 
        sound("level"); 
        gameRunning=true; 
        load(1); 
        requestAnimationFrame(loop);
    };
</script>
</body>
</html>
"""

st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=520, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)

