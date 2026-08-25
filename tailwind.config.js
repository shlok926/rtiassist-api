/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rti-blue': '#1e3a8a',
        'rti-green': '#059669',
      }
    },
  },
  plugins: [],
}
