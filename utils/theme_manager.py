import streamlit as st
from pathlib import Path

def load_css(theme="light"):
    """Load the correct theme file based on state."""
    css_path = Path(__file__).parent.parent / "assets" / f"{theme}_theme.css"
    if css_path.exists():
        with css_path.open() as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"Theme file not found: {css_path}")


def inject_theme_toggle():
    """Floating light/dark toggle — NO RELOAD required."""
    toggle_script = """
    <script>
    const btn = document.createElement("div");
    btn.id = "theme-toggle-btn";
    btn.innerHTML = "🌙";
    btn.style.position = "fixed";
    btn.style.top = "20px";
    btn.style.right = "25px";
    btn.style.padding = "8px";
    btn.style.fontSize = "22px";
    btn.style.cursor = "pointer";
    btn.style.zIndex = "99999";
    btn.style.background = "rgba(0,0,0,0.2)";
    btn.style.borderRadius = "8px";
    btn.style.backdropFilter = "blur(6px)";
    btn.style.transition = "0.3s";
    document.body.appendChild(btn);

    // Load theme
    let theme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", theme);
    btn.innerHTML = theme === "light" ? "🌙" : "☀️";

    btn.onclick = () => {
        theme = (theme === "light") ? "dark" : "light";
        localStorage.setItem("theme", theme);
        document.documentElement.setAttribute("data-theme", theme);
        btn.innerHTML = theme === "light" ? "🌙" : "☀️";
    };
    </script>
    """
    st.markdown(toggle_script, unsafe_allow_html=True)
