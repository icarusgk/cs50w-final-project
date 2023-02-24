import { defineConfig } from 'windicss/helpers'

export default defineConfig({
  darkMode: 'class',
  theme: {
    extend: {
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1160px',
      },
      fontFamily: {
        sans: ['Lexend', 'sans-serif'],
      },
    }
  }
})