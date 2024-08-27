declare namespace NodeJS {
    interface ProcessEnv {
      SUPABASE_URL: string;
      SUPABASE_KEY: string;
      PROXYCURL_API_KEY: string;
      SCRAPIN_API_KEY: string;
    }
  }