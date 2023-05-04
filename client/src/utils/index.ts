import dayjs from "dayjs";

export function toTimer(minutes: number) {
  return dayjs()
  .set('hours', 0)
  .set('minutes', minutes)
  .set('seconds', 0);
}

export const local = {
  get(key: string) {
    return JSON.parse(localStorage.getItem(key) as string)
  },
  set(key: string, value: any) {
    localStorage.setItem(key, JSON.stringify(value))
  }
}