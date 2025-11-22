# utils/theme_manager.py
# NiceGUI-compatible Theme Manager

class ThemeManager:
    """Provides CSS for Light/Dark theme support in NiceGUI."""
    
    @staticmethod
    def get_css():
        """Returns CSS string with theme variables."""
        return """
        /* Light Theme (Default) */
        :root {
            --bg-gradient-start: #e0f2fe;
            --bg-gradient-end: #ffffff;
            --glass-bg: rgba(255, 255, 255, 0.4);
            --glass-border: rgba(0, 0, 0, 0.1);
            --glass-shadow: rgba(0, 0, 0, 0.05);
            --header-bg: rgba(255, 255, 255, 0.3);
            --header-border: rgba(0, 0, 0, 0.05);
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --scrollbar-track: rgba(0, 0, 0, 0.02);
            --scrollbar-thumb: rgba(0, 0, 0, 0.1);
            --scrollbar-thumb-hover: rgba(0, 0, 0, 0.2);
        }
        
        /* Dark Theme */
        body.body--dark {
            --bg-gradient-start: #000000;
            --bg-gradient-end: #000000;
            --glass-bg: rgba(20, 20, 20, 0.6);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: rgba(0, 0, 0, 0.1);
            --header-bg: rgba(0, 0, 0, 0.3);
            --header-border: rgba(255, 255, 255, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --scrollbar-track: rgba(255, 255, 255, 0.02);
            --scrollbar-thumb: rgba(255, 255, 255, 0.1);
            --scrollbar-thumb-hover: rgba(255, 255, 255, 0.2);
        }
        
        /* Apply theme variables */
        body {
            background: radial-gradient(circle at top left, var(--bg-gradient-start), var(--bg-gradient-end)) !important;
            color: var(--text-primary) !important;
        }
        
        .glass-panel {
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 0 4px 30px var(--glass-shadow) !important;
        }
        
        .glass-header {
            background: var(--header-bg) !important;
            border-bottom: 1px solid var(--header-border) !important;
        }
        
        .hide-scroll::-webkit-scrollbar-track {
            background: var(--scrollbar-track) !important;
        }
        
        .hide-scroll::-webkit-scrollbar-thumb {
            background: var(--scrollbar-thumb) !important;
        }
        
        .hide-scroll::-webkit-scrollbar-thumb:hover {
            background: var(--scrollbar-thumb-hover) !important;
        }
        """
