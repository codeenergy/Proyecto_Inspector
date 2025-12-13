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
}

export interface MetricData {
  time: string;
  loadTime: number;
  availability: number;
}