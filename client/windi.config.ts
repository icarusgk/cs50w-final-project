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
        'xs': '460px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1160px',
        '2xl': '1400px',
        '3xl': '1600px'
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

      function actionButton(baseColor: string, ligherColor: string) {
        return {
          ...button(baseColor, ligherColor),
          padding: '.5rem .7rem',
          color: '#fff',
          borderRadius: '8px',
          fontWeight: '500',
          transition: 'box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)',
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
        '.restart-timer-btn': timerButton('#ff8c00', '#ffa333'),
        '.add-item-btn': {
          'box-shadow': '3px 4px rgba(208, 208, 208)',
          'transition': 'box-shadow 0.1s cubic-bezier(0.075, 0.82, 0.165, 1)',
          '&:active': {
            'box-shadow': '0 0 #000'
          }
        },
        '.modal': {
          'background': 'rgba(136, 136, 136, 0.3)',
          'box-shadow': '0 4px 30px rgba(0, 0, 0, 0.1)',
          'backdrop-filter': 'blur(11.2px)',
        },
        '.cancel-btn': actionButton('#636363', '#303030'),
        '.save-btn': actionButton('#ed4747', '#bc1212'),
        '.delete-tag': {
          'box-shadow': '1px 3px 0 1px #f27575',
          'transition': 'box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)',
          '&:active': {
            'box-shadow': '0 0 #ed4747'
          }
        },
        '.depth': {
          'box-shadow': '3px 4px rgb(71, 71, 71)',
          transition: 'box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)',
        }
      }
      addComponents(buttons)
    }),
  ],
  shortcuts: {
    'pointer': 'hover:cursor-pointer active:cursor-pointer focus:cursor-pointer',
    'responsive-modal': 'fixed left-[5%] right-[5%] w-[90%] h-[90%] top-[3%] overflow-y-scroll sm:overflow-auto md:left-[23%] md:top-1/8 md:w-[600px] md:h-auto lg:absolute lg:top-1/5 lg:z-10 lg:left-[5%] lg:right-0 lg:mx-auto lg:w-[700px] lg:h-auto text-white p-8 rounded-2xl',
    'paginate-btn': 'py-1 px-2 lg:py-2 lg:px-4 bg-[rgb(67,67,67)] text-white ml-3 rounded-lg pointer transition-all duration-100 ease-in-out hover:text-black hover:bg-white active:text-black active:bg-white',
  }
})