/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#0b0f19',
          card: '#111827',
          border: '#1f2937',
          accent: '#06b6d4',
          clean: '#10b981',
          warning: '#f59e0b',
          danger: '#ef4444',
          muted: '#6b7280'
        }
      }
    },
  },
  plugins: [],
}
