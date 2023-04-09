import { defineConfig, presetWind, presetWebFonts, toEscapedSelector as e  } from 'unocss'

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

// TODO
const obj = {
  '.depth': {
    'box-shadow': '3px 4px rgb(71, 71, 71)',
    transition: 'box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)',
  }
}

function settingsButton(selector: string, baseColor: string, padding: string, opts?: string) {
  return `
    ${selector} {
      background-color: ${baseColor};
      padding: ${padding};
      transition: box-shadow 0.1s cubic-bezier(0.075, 0.82, 0.165, 1);
      ${opts}
    }
    ${selector}:active {
      box-shadow: 0 0 ${baseColor};
    }
  `
}

function timerButton(selector: string, baseColor: string, lighterColor: string) {
  return `
    ${selector} {
      padding: 1rem;
      width: 160px;
      border-radius: 18px;
      font-size: 1.5rem;
      background-color: ${baseColor};
      color: white;
      font-weight: 900;
      border: none;
      margin-top: 1rem;
      box-shadow: 0 4px 0 0 ${lighterColor};
      transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1)
    }
    ${selector}:active {
      box-shadow: 0 0 ${baseColor}
    }
  `
}

function actionButton(selector: string, baseColor: string, lighterColor: string) {
  return `
    ${selector} {
      padding: .5rem .7rem;
      color: #fff;
      border-radius: 8px;
      font-weight: 500;
      box-shadow: 0 4px 0 0 ${lighterColor};
      transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);
      background-color: ${baseColor}
    }
    ${selector}:active {
      box-shadow: 0 0 ${baseColor}
    }
  `
}

export default defineConfig({
  rules: [
    ['modal', {
      'background-color': 'rgba(136, 136, 136, 0.3)',
      'box-shadow': '0 4px 30px rgba(0, 0, 0, 0.1)',
      'backdrop-filter': 'blur(11.2px)',
    }],
    [/^timer-btn-(.+)$/, ([, name], { rawSelector }) => {
      const selector = e(rawSelector);
      const baseColor = btnColors[name].base
      return `
      ${selector} {
        padding: .5rem .8rem;
        color: #fff;
        border-radius: 8px;
        font-weight: 600;
        transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);
        background-color: ${baseColor};
        box-shadow: 0 4px 0 0 ${btnColors[name].lighter};
      }
      ${selector}:active {
        box-shadow: 0 0 ${baseColor};
        cursor: pointer;
      }
      ${selector}:focus { cursor: pointer; }
      ${selector}:hover { cursor: pointer; }
      `;
    }],
    [/add-item-btn/, ([], { rawSelector }) => {
      const selector = e(rawSelector);
      return `
      ${selector} {
        box-shadow: 3px 4px rgba(208, 208, 208);
        transition: box-shadow 0.6s cubic-bezier(0.075, 0.82, 0.165, 1);
      }
      ${selector}:active { box-shadow: 0 0 #000; }
      `
    }],
    [/pomo|stop\-timer\-btn|restart\-timer\-btn|short_break|long_break/, ([], { rawSelector }) => {
      const selector = e(rawSelector);
      if (rawSelector === 'pomo') {
        return timerButton(selector, '#ed4747', '#f27575');
      }
      if (rawSelector === 'short_break') {
        return timerButton(selector, '#1ba7b1', '#22d1dd');
      }
      if (rawSelector === 'long_break') {
        return timerButton(selector, '#1eaf58', '#26da6e')
      }
      if (rawSelector === 'stop-timer-btn') {
        return timerButton(selector, '#1b6eb1', '#228add');
      }
      if (rawSelector === 'restart-timer-btn') {
        return timerButton(selector, '#ff8c00', '#ffa333');
      }
    }],
    [/back\-to\-default|new\-mode\-btn|create\-mode\-btn/, ([], { rawSelector }) => {
      const selector = e(rawSelector);
      const opts = {
        base: `box-shadow: 3px 4px #ccc`,
        create: `box-shadow: 3px 4px #e80015`
      };
      if (rawSelector === 'create-mode-btn') {
        return settingsButton(selector, '#ff4f5f', '0.8rem', opts.create);
      } else {
        return settingsButton(selector, '#fff', '0.5rem', opts.base);
      }
    }],
    [/cancel|save\-btn/, ([], { rawSelector }) => {
      const selector = e(rawSelector);
      return rawSelector === 'cancel-btn'
        ? actionButton(selector, '#636363', '#303030')
        : actionButton(selector, '#ed4747', '#bc1212')
    }],
    [/delete\-tag/, ([], { rawSelector }) => {
      const selector = e(rawSelector);
      return `
        ${selector} {
          box-shadow: 1px 3px 0 1px #f27575;
          transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);
        }
        ${selector}:active {
          box-shadow: 0 0 #ed4747
        }
      `
    }]
  ],
  presets: [
    presetWind(),
    presetWebFonts({
      provider: 'google',
      fonts: {
        sans: 'Lexend'
      }
    })
  ],
  theme: {
    breakpoints: {
      'xs': '460px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1160px',
      '2xl': '1400px',
      '3xl': '1600px'
    },
    colors: {
      'lighterGray': btnColors.lighterGray,
      'vividRed': btnColors.vividRed,
      'lightRed': btnColors.lightRed,
      'darkGray': btnColors.darkGray,
      'lightGray': btnColors.lightGray,
      'lightBlue': btnColors.lightBlue,
      'shortRest': btnColors.shortRest,
      'longRest': btnColors.longRest,
    }
  },
  shortcuts: {
    'pointer': 'hover:cursor-pointer active:cursor-pointer focus:cursor-pointer',
    'responsive-modal': 'fixed left-[5%] right-[5%] w-[90%] h-[90%] top-[3%] overflow-y-scroll sm:overflow-auto md:left-[23%] md:top-1/8 md:w-[600px] md:h-auto lg:absolute lg:top-1/5 lg:z-10 lg:left-[5%] lg:right-0 lg:mx-auto lg:w-[700px] lg:h-auto text-white p-8 rounded-2xl',
    'paginate-btn': 'py-1 px-2 lg:py-2 lg:px-4 bg-[rgb(67,67,67)] text-white ml-3 rounded-lg pointer transition-all duration-100 ease-in-out hover:text-black hover:bg-white active:text-black active:bg-white',
    'settings-btn': 'border-none rounded-md mt-4 pointer',
  }
})