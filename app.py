import streamlit as st

st.set_page_config(page_title="Mobile Cloud Arcade", page_icon="🕹️", layout="centered")

st.markdown("""
    <style>
    .arcade-cabinet { background-color: #1e1b4b; padding: 10px; border-radius: 12px; border: 4px solid #4338ca; text-align: center; }
    .rules-box { background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #1e293b; color: #94a3b8; font-size: 13px; text-align: left; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Mobile Retro Arcade")

with st.container():
    st.markdown("""
    <div class="rules-box">
        <strong>📱 Phone Controls Support Active:</strong><br>
        • Tap or hold the visual **Blue Directional Arrow Buttons** below the game canvas with your thumbs to guide Pac-Man on your phone touch screen!
    </div>
    """, unsafe_allow_html=True)

# Mobile-Optimized HTML5 Engine with Built-in Touch Buttons Matrix
mobile_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background-color: #000; margin: 0; display: flex; justify-content: center; align-items: center; flex-direction: column; font-family: monospace; user-select: none; -webkit-user-select: none; }
        canvas { border: 3px solid #4f46e5; background-color: #000; box-shadow: 0 0 15px #4f46e5; border-radius: 8px; max-width: 100%; height: auto; }
        #ui { color: #fff; font-size: 18px; font-weight: bold; margin-bottom: 8px; width: 320px; display: flex; justify-content: space-between; }
        
        /* Touch Controller Layout Grid Engine */
        #controller { display: grid; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(3, 60px); gap: 8px; margin-top: 15px; justify-content: center; }
        .btn { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; border: 2px solid #60a5fa; border-radius: 50%; font-size: 24px; font-weight: bold; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); touch-action: manipulation; }
        .btn:active { background: #1e40af; transform: scale(0.92); }
        .empty { visibility: hidden; }
    </style>
</head>
<body>

    <div id="ui">
        <div>SCORE: <span id="score">0</span></div>
        <div style="color: #ef4444;">GOAL: 120</div>
    </div>
    
    <canvas id="arcadeCanvas" width="320" height="320"></canvas>

    <!-- Visual Touch D-Pad Layout Interface Block -->
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

        let score = 0;
        let ghostSpeed = 0.22; // Kept slow for phone touchscreen mobility

        let pacman = { x: 160, y: 240, dx: 0, dy: 0, radius: 10, angle: 0.2, speed: 0.02 };
        let ghost = { x: 160, y: 60, size: 20, color: "#ef4444" };

        let dots = [];
        for (let i = 40; i <= 280; i += 60) {
            for (let j = 40; j <= 280; j += 60) {
                if (!(i === 160 && j === 240)) {
                    dots.push({ x: i, y: j, active: true });
                }
            }
        }

        // --- DIRECTION CHANGE ROUTINE ---
        function setDir(direction) {
            if (direction === 'UP')    { pacman.dx = 0;    pacman.dy = -1.2; }
            if (direction === 'DOWN')  { pacman.dx = 0;    pacman.dy = 1.2;  }
            if (direction === 'LEFT')  { pacman.dx = -1.2; pacman.dy = 0;    }
            if (direction === 'RIGHT') { pacman.dx = 1.2;  pacman.dy = 0;    }
        }

        // Mobile Screen Touch Event Bindings (Supports smooth multi-touch taps)
        document.getElementById("btnUp").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('UP'); });
        document.getElementById("btnDown").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('DOWN'); });
        document.getElementById("btnLeft").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('LEFT'); });
        document.getElementById("btnRight").addEventListener("touchstart", (e) => { e.preventDefault(); setDir('RIGHT'); });
        
        // Desktop Click fallbacks for sidebar window simulation tests
        document.getElementById("btnUp").addEventListener("mousedown", () => setDir('UP'));
        document.getElementById("btnDown").addEventListener("mousedown", () => setDir('DOWN'));
        document.getElementById("btnLeft").addEventListener("mousedown", () => setDir('LEFT'));
        document.getElementById("btnRight").addEventListener("mousedown", () => setDir('RIGHT'));

        // Keyboard support backup mapping
        window.addEventListener("keydown", (e) => {
            if (e.key === "ArrowUp")    setDir('UP');
            if (e.key === "ArrowDown")  setDir('DOWN');
            if (e.key === "ArrowLeft")  setDir('LEFT');
            if (e.key === "ArrowRight") setDir('RIGHT');
            if(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
        });

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Move Player
            pacman.x += pacman.dx; pacman.y += pacman.dy;
            if (pacman.x < pacman.radius) pacman.x = canvas.width - pacman.radius;
            if (pacman.x > canvas.width - pacman.radius) pacman.x = pacman.radius;
            if (pacman.y < pacman.radius) pacman.y = canvas.height - pacman.radius;
            if (pacman.y > canvas.height - pacman.radius) pacman.y = pacman.radius;

            pacman.angle += pacman.speed;
            if (pacman.angle > 0.4 || pacman.angle < 0.05) pacman.speed = -pacman.speed;

            // Tracking AI Enemy
            if (ghost.x < pacman.x) ghost.x += ghostSpeed;
            if (ghost.x > pacman.x) ghost.x -= ghostSpeed;
            if (ghost.y < pacman.y) ghost.y += ghostSpeed;
            if (ghost.y > pacman.y) ghost.y -= ghostSpeed;

            // Render Dots
            let activeDotsCount = 0;
            dots.forEach(dot => {
                if (dot.active) {
                    activeDotsCount++;
                    ctx.beginPath(); ctx.arc(dot.x, dot.y, 4, 0, Math.PI * 2); ctx.fillStyle = "#facc15"; ctx.fill();
                    if (Math.hypot(pacman.x - dot.x, pacman.y - dot.y) < pacman.radius + 4) {
                        dot.active = false; score += 10; scoreEl.innerText = score;
                    }
                }
            });

            // Win Checking
            if (activeDotsCount === 0) {
                alert("🎉 REWARD MILESTONE MET! Level cleared with " + score + " points! Take a screenshot!");
                resetGame();
                return;
            }

            // Draw Geometry Pacman
            ctx.beginPath();
            let rot = 0;
            if (pacman.dx > 0) rot = 0; if (pacman.dx < 0) rot = Math.PI;
            if (pacman.dy > 0) rot = Math.PI / 2; if (pacman.dy < 0) rot = Math.PI * 1.5;
            ctx.arc(pacman.x, pacman.y, pacman.radius, rot + pacman.angle, rot + Math.PI * 2 - pacman.angle);
            ctx.lineTo(pacman.x, pacman.y); ctx.fillStyle = "#facc15"; ctx.fill(); ctx.closePath();

            // Draw Enemy Ghost
            ctx.beginPath(); ctx.arc(ghost.x + 10, ghost.y + 10, 10, Math.PI, 0, false);
            ctx.lineTo(ghost.x + 20, ghost.y + 20); ctx.lineTo(ghost.x, ghost.y + 20);
            ctx.fillStyle = ghost.color; ctx.fill(); ctx.closePath();

            // Catching Collision Mechanics
            if (Math.hypot(pacman.x - (ghost.x + 10), pacman.y - (ghost.y + 10)) < pacman.radius + 10) {
                alert("💥 CAUGHT BY THE GHOST! Game Over. Give it another try!");
                resetGame();
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        function resetGame() {
            score = 0; scoreEl.innerText = score;
            pacman.x = 160; pacman.y = 240; pacman.dx = 0; pacman.dy = 0;
            ghost.x = 160; ghost.y = 60;
            dots.forEach(d => d.active = true);
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.markdown('<div class="arcade-cabinet">', unsafe_allow_html=True)
# Adjusted execution container box dimensions to perfectly accommodate touch padding grid
st.components.v1.html(mobile_game_html, height=560, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)


