/**
 * CareerBoost Design Tokens
 * Inspired by HackerRank Chakra's dark glassmorphism aesthetic
 */

export const theme = {
  colors: {
    // Base backgrounds
    background: {
      primary: '#0A0E14',
      secondary: '#111827',
      tertiary: '#1A2332',
      glass: 'rgba(17, 24, 39, 0.6)',
      glassLight: 'rgba(255, 255, 255, 0.05)',
    },

    // Accent — teal/cyan (Chakra signature)
    accent: {
      primary: '#2DD4BF',
      secondary: '#06B6D4',
      glow: 'rgba(45, 212, 191, 0.4)',
      gradient: 'linear-gradient(135deg, #2DD4BF 0%, #06B6D4 100%)',
    },

    // Text
    text: {
      primary: '#F9FAFB',
      secondary: '#9CA3AF',
      muted: '#6B7280',
      inverse: '#0A0E14',
    },

    // Status colors
    status: {
      success: '#34D399',
      warning: '#FBBF24',
      error: '#F87171',
      info: '#60A5FA',
    },

    // Borders
    border: {
      default: 'rgba(255, 255, 255, 0.08)',
      hover: 'rgba(45, 212, 191, 0.3)',
      focus: '#2DD4BF',
    },

    // Fit badges (report page)
    fit: {
      strong: '#34D399',
      moderate: '#FBBF24',
      weak: '#F87171',
    },
  },

  typography: {
    fontFamily: {
      sans: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
      mono: "'JetBrains Mono', 'Fira Code', monospace",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '3.75rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
    },
  },

  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
    '4xl': '6rem',
  },

  borderRadius: {
    sm: '0.375rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    '2xl': '1.5rem',
    full: '9999px',
  },

  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px rgba(0, 0, 0, 0.4)',
    lg: '0 10px 25px rgba(0, 0, 0, 0.5)',
    glow: '0 0 20px rgba(45, 212, 191, 0.3)',
    glowStrong: '0 0 40px rgba(45, 212, 191, 0.5)',
  },

  blur: {
    sm: '4px',
    md: '12px',
    lg: '24px',
    xl: '40px',
  },

  transitions: {
    fast: '150ms ease',
    normal: '250ms ease',
    slow: '400ms ease',
    bounce: '400ms cubic-bezier(0.34, 1.56, 0.64, 1)',
  },

  zIndex: {
    background: -1,
    base: 0,
    dropdown: 10,
    sticky: 20,
    overlay: 30,
    modal: 40,
    toast: 50,
  },

  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
};

export default theme;
