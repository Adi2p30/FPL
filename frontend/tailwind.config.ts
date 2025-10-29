import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // EA FC / FPL Theme Colors
        primary: {
          DEFAULT: '#37003c', // FPL Purple
          dark: '#1a001b',
          light: '#4d0052',
        },
        accent: {
          pink: '#e90052', // PL Pink
          purple: '#04f5ff', // Cyan accent
          gold: '#ffd700',
        },
        background: {
          DEFAULT: '#0a0a0b',
          card: '#12121a',
          hover: '#1a1a24',
        },
        border: {
          DEFAULT: '#1f1f2e',
          bright: '#38003c',
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #37003c 0%, #e90052 100%)',
        'gradient-card': 'linear-gradient(135deg, #12121a 0%, #1a1a24 100%)',
        'gradient-glow': 'radial-gradient(circle at center, rgba(233, 0, 82, 0.15) 0%, transparent 70%)',
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(233, 0, 82, 0.3)',
        'glow-md': '0 0 20px rgba(233, 0, 82, 0.4)',
        'glow-lg': '0 0 30px rgba(233, 0, 82, 0.5)',
        'neon': '0 0 5px theme("colors.accent.pink"), 0 0 10px theme("colors.accent.pink")',
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'fade-in': 'fadeIn 0.2s ease-in',
      },
      keyframes: {
        glow: {
          'from': { boxShadow: '0 0 5px rgba(233, 0, 82, 0.2), 0 0 10px rgba(233, 0, 82, 0.2)' },
          'to': { boxShadow: '0 0 10px rgba(233, 0, 82, 0.4), 0 0 20px rgba(233, 0, 82, 0.4)' },
        },
        slideUp: {
          'from': { opacity: '0', transform: 'translateY(10px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          'from': { opacity: '0', transform: 'translateY(-10px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          'from': { opacity: '0' },
          'to': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
export default config
