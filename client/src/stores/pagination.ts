import { defineStore } from "pinia";

export const usePageStore = defineStore('pagination', {
  state: () => ({
    projectPagination: {
      count: 0,
      page: 1,
      added: 1,
      page_size: 2,
    },
    taskPagination: {
      count: 0,
      page: 1,
      added: 1,
      page_size: 4,
    }
  }),
  getters: {
    totalProjectPages(state) {
      return Math.ceil(state.projectPagination.count / state.projectPagination.page_size)
    },
    totalTaskPages(state) {
      return Math.ceil(state.taskPagination.count / state.taskPagination.page_size)
    }
  },
  actions: {
    decreaseProjectPagination() {
      this.projectPagination.page -= 1;
      this.projectPagination.count -= 1;
      this.projectPagination.added -= 1;
    },
    decreaseTaskPagination() {
      this.taskPagination.page -= 1;
      this.taskPagination.count -= 1;
      this.taskPagination.added -= 1;
    },
    previousProjectPage() {
      if (this.projectPagination.page > 1) {
        this.projectPagination.page--;
      }
    },
    setProjectPage(page: number) {
      this.projectPagination.page = page;
    },
    setProjectAdded(added: number) {
      this.projectPagination.added = added;
    },
    nextProjectPage() {
      if (this.projectPagination.page < this.totalProjectPages) {
        this.projectPagination.page++;
      }
    },
    previousTaskPage() {
      if (this.taskPagination.page > 1) {
        this.taskPagination.page--;
      }
    },
    setTaskPage(page: number) {
      this.taskPagination.page = page;
    },
    setTaskAdded(added: number) {
      this.taskPagination.added = added;
    },
    nextTaskPage() {
      if (this.taskPagination.page < this.totalTaskPages) {
        this.taskPagination.page++;
      }
    }
  }
})