import { defineStore } from 'pinia';
import { v4 as uuid } from 'uuid';

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

export const useAlertStore = defineStore('alerts', {
  state: () => ({
    items: [] as Alert[],
  }),

  actions: {
    notify(message: string, style: AlertStyle, options?: AlertOptions) {
      options = { ...defaultOptions, style, ...options };

      const id = uuid();

      this.items.push({
        message,
        id,
        ...options,
      });

      if (options.timeout) {
        setTimeout(() => {
          this.remove(id);
        }, options.timeout);
      }
    },

    success(message: string, options?: AlertOptions) {
      this.notify(message, 'success', options);
    },

    error(message: string, options?: AlertOptions) {
      this.notify(message, 'error', options);
    },

    info(message: string, options?: AlertOptions) {
      this.notify(message, 'info', options);
    },

    remove(id: string) {
      const index = this.items.findIndex((item) => item.id === id);
      if (index > -1) {
        this.items.splice(index, 1);
      }
    },
  },
});
