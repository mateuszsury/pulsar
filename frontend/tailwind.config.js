/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // VS Code dark theme colors
        'vscode': {
          'bg': '#1e1e1e',
          'sidebar': '#252526',
          'editor': '#1e1e1e',
          'panel': '#1e1e1e',
          'border': '#3c3c3c',
          'text': '#cccccc',
          'text-dim': '#858585',
          'accent': '#007acc',
          'accent-hover': '#1177bb',
          'success': '#4ec9b0',
          'warning': '#dcdcaa',
          'error': '#f14c4c',
          'info': '#3794ff',
          'selection': '#264f78',
          'hover': '#2a2d2e',
          'active': '#37373d',
          'input': '#3c3c3c',
          'button': '#0e639c',
          'button-hover': '#1177bb',
        }
      },
      fontFamily: {
        'mono': ['Consolas', 'Menlo', 'Monaco', 'Courier New', 'monospace'],
        'sans': ['Segoe UI', 'Helvetica', 'Arial', 'sans-serif'],
      },
      fontSize: {
        'xs': '11px',
        'sm': '12px',
        'base': '13px',
        'lg': '14px',
      },
    },
  },
  plugins: [],
}
