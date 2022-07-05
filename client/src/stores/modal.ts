import { defineStore } from 'pinia'

export const useModalStore = defineStore({
  id: 'modal',
  state: () => ({
    isOpened: false,
  }),
  actions: {
    open() {
      this.isOpened = true
    },
    close() {
      this.isOpened = false
    },
    toggle() {
      this.isOpened = !this.isOpened
    }
  }
})