export interface IPage<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}