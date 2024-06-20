/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ['Montserrat', 'sans-serif']
      },
      colors: {
        'imdb-gold': '#F5C518',
        'imdb-black': '#000000',
        'imdb-white': '#FFFFFF',
        'unive-red': '#A50033'
      },
      zIndex: {
        '1': '1'
      }
    }
  },
  plugins: []
}
