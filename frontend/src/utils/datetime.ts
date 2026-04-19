export function formatPublishedAt(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const h = String(d.getHours()).padStart(2, "0");
  const min = String(d.getMinutes()).padStart(2, "0");
  const s = String(d.getSeconds()).padStart(2, "0");
  // 与后端 _format_published_at 规则一致：分秒都为 0 → 降级为小时级
  if (d.getMinutes() === 0 && d.getSeconds() === 0) {
    return `${y}-${m}-${day} ${h}:00:00`;
  }
  return `${y}-${m}-${day} ${h}:${min}:${s}`;
}
