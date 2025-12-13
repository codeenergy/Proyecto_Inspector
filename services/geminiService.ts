import { GoogleGenAI } from "@google/genai";
import { AdCampaign } from "../types";

// Initialize the Gemini client
// Note: We are using the correct initialization method as per guidelines.
// Ideally, in a production app, the key would be proxied, but for this demo, we assume process.env.API_KEY is available.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const generateDashboardInsight = async (
  campaigns: AdCampaign[],
  globalAvgLoadTime: number
): Promise<string> => {
  try {
    const errorCampaigns = campaigns.filter(c => c.status === 'error');
    const slowCampaigns = campaigns.filter(c => c.loadTime > 3.5);

    const prompt = `
      You are an Ad-Inspector Bot AI Analyst. Analyze the following ad campaign data summary:
      
      - Total Campaigns: ${campaigns.length}
      - Campaigns with Errors: ${errorCampaigns.length} (${errorCampaigns.map(c => c.name).join(', ')})
      - Slow Campaigns (>3.5s): ${slowCampaigns.length}
      - Global Average Load Time: ${globalAvgLoadTime.toFixed(2)}s

      Provide a concise executive summary (max 3 sentences) of the overall health of the ad network.
      Then, provide 2 short, actionable technical recommendations to improve ROI and reduce bounce rates based on this data.
      Format the output as plain text.
    `;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
    });

    return response.text || "No insights generated.";
  } catch (error) {
    console.error("Error generating insight:", error);
    return "Unable to generate AI insights at this time. Please check your API configuration.";
  }
};

export const analyzeCampaignError = async (campaign: AdCampaign): Promise<string> => {
  try {
    const prompt = `
      You are a QA Engineer expert in Selenium and Web Performance.
      
      A campaign "${campaign.name}" pointing to "${campaign.url}" has failed with the following status: ${campaign.status}.
      The last recorded load time was ${campaign.loadTime}s.
      Active Viewports: ${campaign.viewports.join(', ')}.
      Known errors: ${campaign.errors.join(', ') || "Unknown HTTP/Element error"}.

      Suggest 3 specific debugging steps or fixes for the web development team to resolve these issues and restore the conversion funnel.
    `;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
    });

    return response.text || "No specific analysis available.";
  } catch (error) {
    console.error("Error analyzing campaign:", error);
    return "Unable to analyze error.";
  }
};