import streamlit as st

# 1. SETUP PAGE LAYOUT
st.set_page_config(
    page_title="Mobile Story Arcade",
    page_icon="🕹️",
    layout="centered",
)

# Custom Styling for the Interface
st.markdown(
    """
    <style>
    .arcade-cabinet {
        background-color: #0b0f19;
        padding: 10px;
        border-radius: 16px;
        border: 4px solid #1e1b4b;
        text-align: center;
    }
    .story-banner {
        background: linear-gradient(
            135deg,
            #1e293b,
            #0f172a
        );
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        color: #e2e8f0;
        font-size: 14px;
        text-align: left;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    .chapter-title {
        color: #38bdf8;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 5px;
        font-family: monospace;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🏝️ Island Adventure Arcade")

with st.container():
    st.markdown(
        """
    <div class="story-banner">
        <div class="chapter-title">
            📖 THE JOURNEY OF DHIVEHI PAC
        </div>
        Clear all dots across 3 famous 
        Maldivian spots to beat the story!
    </div>
    """,
        unsafe_allow_html=True,
    )

# 2. EMBEDDED RETRO ARCADE ENGINE
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="
        width=device-width, 
        initial-scale=1.0, 
        maximum-scale=1.0, 
        user-scalable=no">
    <style>
        body {
            background-color: #000;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            font-family: monospace;
            user-select: none;
            -webkit-user-select: none;
        }
        canvas {
            border: 3px solid #0284c7;
            background-color: #000;
            border-radius: 8px;
            max-width: 100%;
            height: auto;
        }
        #ui {
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 8px;
            width: 320px;
            display: flex;
            justify-content: space-between;
        }
        #stage-banner {
            color: #38bdf8;
            font-size: 14px;
            margin-bottom: 5px;
            font-weight: bold;
        }
        #controller {
            display: grid;
            grid-template-columns: repeat(3, 55px);
            grid-template-rows: repeat(3, 55px);
            gap: 10px;
            margin-top: 15px;
        }
        .btn {
            background: #0284c7;
            color: white;
            border: 2px solid #38bdf8;
            border-radius: 50%;
            font-size: 22px;
            display: flex;
            justify-content: center;
            align-items: center;
            touch-action: manipulation;
        }
        .btn:active { background: #075985; }
        .empty { visibility: hidden; }
    </style>
</head>
<body>

    <div id="stage-banner">STAGE 1</div>
    <div id="ui">
        <div>SCORE: <span id="score">0</span></div>
        <div>LIVES: <span id="lives">3</span></div>
    </div>
    
    <canvas id="arcadeCanvas" width="320" height="320"></canvas>

    <div id="controller">
        <div class="empty"></div>
        <div class="btn" id="btnUp">▲</div>
        <div class="empty"></div>
        
        <div class="btn" id="btnLeft">◀</div>
        <div class="empty"></div>
        <div class="btn" id="btnRight">▶</div>
        
        <div class="empty"></div>
        <div class="btn" id="btnDown">▼</div>
        <div class="empty"></div>
    </div>

    <script>
        const canvas = document.getElementById("arcadeCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");
        const livesEl = document.getElementById("lives");
        const stageBanner = document.getElementById("stage-banner");

        let score = 0, lives = 3, currentStage = 1, ghostSpeed = 0.22;
        let pacman = { x: 160, y: 240, dx: 0, dy: 0, radius: 10, angle: 0.2, speed: 0.02 };
        let ghost = { x: 160, y: 60, size: 20, color: "#ef4444" };
        let dots = [];

        const STAGE_CONFIGS = {
            1: {
                name: "📍 STAGE 1: MALE' STREETS",
                color: "#0284c7", gColor: "#ef4444", speed: 0.22,
                generate: function() {
                    let arr = [];
                    for (let i = 40; i <= 280; i += 60) {
                        for (let j = 40; j <= 280; j += 60) {
                            if (!(i === 160 && j === 240)) arr.push({ x: i, y: j, active: true });
                        }
                    }
                    return arr;
                }
            },
            2: {
                name: "📍 STAGE 2: CROSSROADS MARINA",
                color: "#f59e0b", gColor: "#a855f7", speed: 0.26,
                generate: function() {
                    let arr = [];
                    for (let i = 50; i <= 270; i += 50) {
                        arr.push({ x: i, y: i, active: true });
                        arr.push({ x: i, y: 320 - i, active: true });
                    }
                    return arr;
                }
            },
            3: {
                name: "📍 STAGE 3: DEEP CORAL REEF",
                color: "#10b981", gColor: "#f43f5e", speed: 0.30,
                generate: function() {
                    let arr = [];
                    for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
                        arr.push({ x: 160 + Math.cos(a) * 80, y: 160 + Math.sin(a) * 80, active: true });
                    }
                    return arr;
                }
            }
        };

        function loadStage(num) {
            currentStage = num;
            let cfg = STAGE_CONFIGS[num];
            stageBanner.innerText = cfg.name;
            canvas.style.borderColor = cfg.color;
            ghost.color = cfg.gColor;
            ghostSpeed = cfg.speed;
            pacman.x = 160; pacman.y = 240; pacman.dx = 0; pacman.dy = 0;
            ghost.x = 160; ghost.y = 40;
            dots = cfg.generate();
        }

        function setDir(d) {
            if (d === 'UP')    { pacman.dx = 0;    pacman.dy = -1.3; }
            if (d === 'DOWN')  { pacman.dx = 0;    pacman.dy = 1.3;  }
            if (d === 'LEFT')  { pacman.dx = -1.3; pacman.dy = 0;    }
            if (d === 'RIGHT') { pacman.dx = 1.3;  pacman.dy = 0;    }
        }

        document.getElementById("btnUp").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('UP'); });
        document.getElementById("btnDown").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('DOWN'); });
        document.getElementById("btnLeft").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('LEFT'); });
        document.getElementById("btnRight").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('RIGHT'); });
        
        document.getElementById("btnUp").addEventListener("mousedown", () => setDir('UP'));
        document.getElementById("btnDown").addEventListener("mousedown", () => setDir('DOWN'));
        document.getElementById("btnLeft").addEventListener("mousedown", () => setDir('LEFT'));
        document.getElementById("btnRight").addEventListener("mousedown", () => setDir('RIGHT'));

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            pacman.x += pacman.dx; pacman.y += pacman.dy;
            if (pacman.x < pacman.radius) pacman.x = canvas.width - pacman.radius;
            if (pacman.x > canvas.width - pacman.radius) pacman.x = pacman.radius;
            if (pacman.y < pacman.radius) pacman.y = canvas.height - pacman.radius;
            if (pacman.y > canvas.height - pacman.radius) pacman.y = pacman.radius;

            pacman.angle += pacman.speed;
            if (pacman.angle > 0.4 || pacman.angle < 0.05) pacman.speed = -pacman.speed;

            if (ghost.x < pacman.x) ghost.x += ghostSpeed;
            if (ghost.x > pacman.x) ghost.x -= ghostSpeed;
            if (ghost.y < pacman.y) ghost.y += ghostSpeed;
            if (ghost.y > pacman.y) ghost.y -= ghostSpeed;

            let activeCount = 0;
            dots.forEach(d => {
                if (d.active) {
                    activeCount++;
                    ctx.beginPath(); ctx.arc(d.x, d.y, 4, 0, Math.PI * 2); ctx.fillStyle = "#fbbf24"; ctx.fill();
                    if (Math.hypot(pacman.x - d.x, pacman.y - d.y) < pacman.radius + 4) {
                        d.active = false; score += 10; scoreEl.innerText = score;
                    }
                }
            });

            if (activeCount === 0) {
                if (currentStage < 3) {
                    alert("📖 LEVEL CLEAR! Heading to next spot...");
                    loadStage(currentStage + 1);
                } else {
                    alert("👑 CHAMPION! You beat the Maldivian Campaign!");
                    score = 0; scoreEl.innerText = score;
                    lives = 3; livesEl.innerText = lives;
                    loadStage(1);
                    return;
                }
            }

            // Draw Player
            ctx.beginPath();
            let r = 0;
            if (pacman.dx > 0) r = 0; if (pacman.dx < 0) r = Math.PI;
            if (pacman.dy > 0) r = Math.PI / 2; if (pacman.dy < 0) r = Math.PI * 1.5;
            ctx.arc(pacman.x, pacman.y, pacman.radius, r + pacman.angle, r + Math.PI * 2 - pacman.angle);
            ctx.lineTo(pacman.x, pacman.y); ctx.fillStyle = "#facc15"; ctx.fill(); ctx.closePath();

            // Draw Ghost
            ctx.beginPath(); ctx.arc(ghost.x + 10, ghost.y + 10, 10, Math.PI, 0, false);
            ctx.lineTo(ghost.x + 20, ghost.y + 20); ctx.lineTo(ghost.x, ghost.y + 20);
            ctx.fillStyle = ghost.color; ctx.fill(); ctx.closePath();
            if (Math.hypot(pacman.x - (ghost.x + 10), pacman.y - (ghost.y + 10)) < pacman.radius + 10) {
            lives--; livesEl.innerText = lives;
            if (lives <= 0) {
            alert("💥 GAME OVER! Starting back at Stage 1.");
            score = 0; scoreEl.innerText = score;
            lives = 3; livesEl.innerText = lives;
            loadStage(1);
            } else {
            alert("💥 CAUGHT! Lost 1 life.");
            pacman.x = 160; pacman.y = 240; pacman.dx = 0; pacman.dy = 0;
            ghost.x = 160; ghost.y = 40;
            }
            return;
            }
            requestAnimationFrame(gameLoop);
            }
            loadStage(1);
            gameLoop();
            """
3. RENDER THE CABINET CONTAINER
st.markdown('', unsafe_allow_html=True)
st.components.v1.html(game_html, height=540, scrolling=False)
st.markdown("", unsafe_allow_html=True)
