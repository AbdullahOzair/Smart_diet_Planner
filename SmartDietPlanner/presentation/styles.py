"""
Smart Diet & Lifestyle Planner - UI Styles and Themes
Presentation Layer: Centralized Styling Configuration
"""

# Color scheme definitions
COLORS = {
    # Primary colors
    'primary': '#2E7D32',      # Green
    'secondary': '#1976D2',    # Blue
    'accent': '#FF6F00',       # Orange
    
    # Background colors
    'bg_main': '#FFFFFF',      # White
    'bg_secondary': '#F5F5F5', # Light Gray
    'bg_dark': '#263238',      # Dark Gray
    
    # Text colors
    'text_primary': '#212121',   # Almost Black
    'text_secondary': '#757575', # Gray
    'text_light': '#FFFFFF',     # White
    
    # Status colors
    'success': '#4CAF50',      # Green
    'warning': '#FF9800',      # Orange
    'error': '#F44336',        # Red
    'info': '#2196F3',         # Blue
}

# Font configurations
FONTS = {
    'heading': ('Arial', 18, 'bold'),
    'subheading': ('Arial', 14, 'bold'),
    'normal': ('Arial', 11),
    'small': ('Arial', 9),
    'button': ('Arial', 11, 'bold'),
}

# Widget styles
BUTTON_STYLE = {
    # Primary button style
    'primary': {
        # 'bg': COLORS['primary'],
        # 'fg': COLORS['text_light'],
        # 'font': FONTS['button'],
        # 'padx': 20,
        # 'pady': 10,
    },
    
    # Secondary button style
    'secondary': {
        # 'bg': COLORS['secondary'],
        # 'fg': COLORS['text_light'],
        # 'font': FONTS['button'],
    },
}

# Entry field styles
ENTRY_STYLE = {
    # 'font': FONTS['normal'],
    # 'bg': COLORS['bg_main'],
    # 'fg': COLORS['text_primary'],
}

# Label styles
LABEL_STYLE = {
    # 'font': FONTS['normal'],
    # 'bg': COLORS['bg_main'],
    # 'fg': COLORS['text_primary'],
}


def apply_theme(widget, theme_type='default'):
    """
    Apply predefined theme to a widget
    Args:
        widget: Tkinter widget to style
        theme_type: Theme name to apply
    """
    pass


def get_color(color_name):
    """
    Get color code by name
    Args:
        color_name: Name of the color from COLORS dictionary
    Returns:
        str: Hex color code
    """
    pass


def get_font(font_name):
    """
    Get font configuration by name
    Args:
        font_name: Name of the font from FONTS dictionary
    Returns:
        tuple: Font configuration tuple
    """
    pass
