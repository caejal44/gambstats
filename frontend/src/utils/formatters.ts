export function formatDate(dateString: string | null) {
  if (!dateString) return "";

  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function toDateTimeLocal(value: string | null) {
  if (!value) return "";
  return value.slice(0, 16);
}