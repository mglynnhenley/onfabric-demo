/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Playfair Display', 'serif'],
        serif: ['Source Serif 4', 'serif'],
      },
      colors: {
        'cream': '#FAF8F3',
        'warm-gray': '#E8E3DB',
        'charcoal': '#2D2A26',
        'terracotta': '#C17858',
        'sage': '#8C9C7C',
        'accent-sage': '#8C9C7C',
        'accent-navy': '#2B3A4F',
      },
    },
  },
  plugins: [],
}
