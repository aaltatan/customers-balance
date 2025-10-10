function numToString(value: number) {
  return value.toString().padStart(2, "0");
}

export function dateToString(date: Date) {
  let month = date.getMonth() + 1;
  let day = date.getDate();
  return `${date.getFullYear()}-${numToString(month)}-${numToString(day)}`;
}

export function stringToDate(value: string) {
  let date = new Date();
  if (value) date = new Date(value);
  if (isNaN(date.getTime())) date = new Date();
  return date;
}
