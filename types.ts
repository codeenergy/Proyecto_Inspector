export interface BotTarget {
  id: number;
  url: string;
  target_pageviews: number;
  ad_click_probability: number;
  viewport: { width: number; height: number };
  enabled: boolean;
}

export interface BotStats {
  total_sessions: number;
  total_pageviews: number;
  total_ad_clicks: number;
  total_buttons_clicked?: number;  // NUEVO: Total de botones clickeados
  total_windows_opened?: number;   // NUEVO: Total de ventanas/direct links abiertas
}

export interface MetricData {
  time: string;
  loadTime: number;
  availability: number;
}