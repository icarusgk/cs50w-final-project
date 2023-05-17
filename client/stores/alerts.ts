import { nanoid } from 'nanoid';

export type AlertStyle = 'error' | 'success' | 'info' | 'none';

export interface AlertOptions {
  closable?: boolean;
  timeout?: number | false;
  style?: AlertStyle;
}

const defaultOptions: Required<AlertOptions> = {
  closable: true,
  timeout: 2000,
  style: 'info',
};

export interface Alert extends AlertOptions {
  id: string;
  message: string;
}

export const useAlertStore = defineStore('alerts', () => {
  const items = reactive<Alert[]>([])

  function notify(message: string, style: AlertStyle, options?: AlertOptions) {
    options = { ...defaultOptions, style, ...options };
    const id = nanoid();

    items.push({ message, id, ...options });

    if (options.timeout) {
      setTimeout(() => { remove(id) }, options.timeout)
    }
  }

  function success(message: string, options?: AlertOptions) {
    notify(message, 'success', options);
  }

  function error(message: string, options?: AlertOptions) {
    notify(message, 'error', options);
  }

  function info(message: string, options?: AlertOptions) {
    notify(message, 'info', options);
  }

  function remove(id: string) {
    const index = items.findIndex((item) => item.id === id);
    if (index > -1) {
      items.splice(index, 1);
    }
  }

  return { items, success, error, info }
});
