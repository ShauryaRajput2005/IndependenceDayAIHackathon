import { createClient } from '@blinkdotnew/sdk'

export const blink = createClient({
  projectId: import.meta.env.VITE_BLINK_PROJECT_ID || 'trendpilot-ai-studio-tr3cvpyi',
  publishableKey: import.meta.env.VITE_BLINK_PUBLISHABLE_KEY || 'blnk_pk_PveKOhzuAXXG9c1w5KfCcewqzpM_mdSj',
  authRequired: false,
  auth: { mode: 'managed' },
})
