import { defineConfig } from 'windicss/helpers'
import plugin from 'windicss/plugin'

const btnColors = {
  lighterGray: '#4a4a4a',
  vividRed: '#ed4747',
  lightRed: '#ff4f5f',
  darkGray: '#212121',
  lightGray: '#2f2f2f',
  lightBlue: '#02b79f',
  shortRest: '#1ba7b1',
  longRest: '#1eaf58',
  red: {
    base: '#ed4747',
    lighter: '#f27575'
  },
  blue: {
    base: '#1ba7b1',
    lighter: '#22d1dd'
  },
  green: {
    base: '#1eaf58',
    lighter: '#26da6e'
  }
}

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
      colors: {
        'lighter-gray': btnColors.lighterGray, 
        'vivid-red': btnColors.vividRed, 
        'light-red': btnColors.lightRed, 
        'dark-gray': btnColors.darkGray, 
        'light-gray': btnColors.lightGray, 
        'light-blue': btnColors.lightBlue, 
        'short-rest': btnColors.shortRest, 
        'long-rest': btnColors.longRest, 
      }
    },
  },
  plugins: [
    plugin(({ addComponents }) => {
      function button(baseColor: string, lighterColor: string) {
        return {
          'backgroundColor': baseColor,
          'box-shadow': `0 4px 0 0 ${lighterColor}`,
          '&:active': {
            'box-shadow': `0 0 ${baseColor}`
          },
        }
      }
      function timerButton(baseColor: string, lighterColor: string) {
        return {
          'padding': '1rem',
          'width': '160px',
          'border-radius': '18px',
          'font-size': '1.5rem',
          'background-color': baseColor,
          'color': 'white',
          'font-weight': '900',
          'border': 'none',
          'margin-top': '1rem',
          ...button(baseColor, lighterColor)
        }
      }
      const buttons = {
        '.timer-btn': {
          padding: '.5rem .8rem',
          color: '#fff',
          borderRadius: '8px',
          fontWeight: '600',
          transition: 'box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)',
          '&:hover, &:focus, &:active': {
            cursor: 'pointer'
          }
        },
        '.timer-btn-red': button('#ed4747', '#f27575'),
        '.timer-btn-blue': button('#1ba7b1', '#22d1dd'),
        '.timer-btn-green': button('#1eaf58', '#26da6e'),
        '.pomo': timerButton('#ed4747', '#f27575'),
        '.short_break': timerButton('#1ba7b1', '#22d1dd'),
        '.long_break': timerButton('#1eaf58', '#26da6e'),
        '.stop-timer-btn': timerButton('#1b6eb1', '#228add'),
        '.restart-timer-btn': timerButton('#ff8c00', '#ffa333')
      }
      addComponents(buttons)
    })
  ]
})