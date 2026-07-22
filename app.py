import streamlit as st

st.set_page_config(page_title="Cloud Arcade Pro", page_icon="🕹️", layout="centered")

st.markdown("""
    <style>
    .arcade-cabinet { background-color: #1e1b4b; padding: 20px; border-radius: 12px; border: 4px solid #4338ca; text-align: center; }
    .rules-box { background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #1e293b; color: #94a3b8; font-size: 14px; text-align: left; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Balanced Skill Arcade")

with st.container():
    st.markdown("""
    <div class="rules-box">
        <strong>🏆 Smooth Gameplay Instructions:</strong><br>
        • Click inside the black box first to focus your controls.<br>
        • Use your keyboard Arrow Keys to guide Pac-Man. <br>
        • The enemy speed is now heavily reduced for a fair, winnable challenge!
    </div>
    """, unsafe_allow_html=True)

# Fixed Speed HTML5 Canvas Game Engine
balanced_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: #000; margin: 0; display: flex; justify-content: center; align-items: center; flex-direction: column; font-family: monospace; }
        canvas { border: 4px solid #4f46e5; background-color: #000; box-shadow: 0 0 20px #4f46e5; border-radius: 8px; }
        #ui { color: #fff; font-size: 22px; font-weight: bold; margin-bottom: 10px; letter-spacing: 2px; width: 400px; display: flex; justify-content: space-between; }
    </style>
</head>
<body>

    <div id="ui">
        <div>SCORE: <span id="score">0</span></div>
        <div style="color: #ef4444;">GOAL: 120</div>
    </div>
    <canvas id="arcadeCanvas" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("arcadeCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");

        let score = 0;
        
        // FIXED: Ghost speed cut down from 1.0 to 0.25 for slow, fair chasing movement
        let ghostSpeed = 0.25; 

        // FIXED: Balanced Pacman step speed for precision moving
        let pacman = { x: 200, y: 300, dx: 0, dy: 0, radius: 12, angle: 0.2, speed: 0.02 };
        let ghost = { x: 200, y: 80, size: 24, color: "#ef4444" };

        let dots = [];
        for (let i = 50; i <= 350; i += 75) {
            for (let j = 50; j <= 350; j += 75) {
                if (!(i === 200 && j === 300)) {
                    dots.push({ x: i, y: j, active: true });
                }
            }
        }

        window.addEventListener("keydown", (e) => {
            // FIXED: Clean velocity step limits
            if (e.key === "ArrowUp")    { pacman.dx = 0;  pacman.dy = -1.5; }
            if (e.key === "ArrowDown")  { pacman.dx = 0;  pacman.dy = 1.5;  }
            if (e.key === "ArrowLeft")  { pacman.dx = -1.5; pacman.dy = 0;  }
            if (e.key === "ArrowRight") { pacman.dx = 1.5;  pacman.dy = 0;  }
            if(["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
        });

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Move Pacman and trap inside boundary walls
            pacman.x += pacman.dx; pacman.y += pacman.dy;
            if (pacman.x < pacman.radius) pacman.x = canvas.width - pacman.radius;
            if (pacman.x > canvas.width - pacman.radius) pacman.x = pacman.radius;
            if (pacman.y < pacman.radius) pacman.y = canvas.height - pacman.radius;
            if (pacman.y > canvas.height - pacman.radius) pacman.y = pacman.radius;

            pacman.angle += pacman.speed;
            if (pacman.angle > 0.4 || pacman.angle < 0.05) pacman.speed = -pacman.speed;

            // FIXED SMART GHOST AI: Moves exceptionally slow towards your current x/y matrix
            if (ghost.x < pacman.x) ghost.x += ghostSpeed;
            if (ghost.x > pacman.x) ghost.x -= ghostSpeed;
            if (ghost.y < pacman.y) ghost.y += ghostSpeed;
            if (ghost.y > pacman.y) ghost.y -= ghostSpeed;

            // Draw Dots
            let activeDotsCount = 0;
            dots.forEach(dot => {
                if (dot.active) {
                    activeDotsCount++;
                    ctx.beginPath(); ctx.arc(dot.x, dot.y, 5, 0, Math.PI * 2); ctx.fillStyle = "#facc15"; ctx.fill();
                    
                    if (Math.hypot(pacman.x - dot.x, pacman.y - dot.y) < pacman.radius + 5) {
                        dot.active = false; score += 10; scoreEl.innerText = score;
                    }
                }
            });

            // Check Win
            if (activeDotsCount === 0) {
                alert("🎉 LEVEL CLEARED! Perfect Score of " + score + "! You beat the chasing ghost!");
                resetGame();
                return;
            }

            // Draw Pacman
            ctx.beginPath();
            let rot = 0;
            if (pacman.dx > 0) rot = 0; if (pacman.dx < 0) rot = Math.PI;
            if (pacman.dy > 0) rot = Math.PI / 2; if (pacman.dy < 0) rot = Math.PI * 1.5;
            ctx.arc(pacman.x, pacman.y, pacman.radius, rot + pacman.angle, rot + Math.PI * 2 - pacman.angle);
            ctx.lineTo(pacman.x, pacman.y); ctx.fillStyle = "#facc15"; ctx.fill(); ctx.closePath();

            // Draw Ghost
            ctx.beginPath(); ctx.arc(ghost.x + 12, ghost.y + 12, 12, Math.PI, 0, false);
            ctx.lineTo(ghost.x + 24, ghost.y + 24); ctx.lineTo(ghost.x, ghost.y + 24);
            ctx.fillStyle = ghost.color; ctx.fill(); ctx.closePath();

            // Ghost Collision (Game Over)
            if (Math.hypot(pacman.x - (ghost.x + 12), pacman.y - (ghost.y + 12)) < pacman.radius + 12) {
                alert("💥 CAUGHT! Game Over. Practice makes perfect, try again!");
                resetGame();
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        function resetGame() {
            score = 0; scoreEl.innerText = score;
            pacman.x = 200; pacman.y = 300; pacman.dx = 0; pacman.dy = 0;
            ghost.x = 200; ghost.y = 80;
            dots.forEach(d => d.active = true);
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.markdown('<div class="arcade-cabinet">', unsafe_allow_html=True)
st.components.v1.html(balanced_game_html, height=470, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

