import { ValidationResult } from '../types/validation';

const API_URL = 'https://deep-research-agent-backend-hbej.onrender.com';

export const fetchValidationResult = async (
  topic: string,
  timeout: number = 300000
): Promise<ValidationResult> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${API_URL}/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ research_topic: topic }),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
};