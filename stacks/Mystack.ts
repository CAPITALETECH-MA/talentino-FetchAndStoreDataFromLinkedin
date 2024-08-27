import { StackContext, Api } from "sst/constructs";

export function API({ stack }: StackContext) {
  const api = new Api(stack, "api", {
    defaults: {
      function: {
        runtime: "python3.9",
        environment: {
          SUPABASE_URL: process.env.SUPABASE_URL || "",
          SUPABASE_KEY: process.env.SUPABASE_KEY || "",
          PROXYCURL_API_KEY: process.env.PROXYCURL_API_KEY || "",
          SCRAPIN_API_KEY: process.env.SCRAPIN_API_KEY || "",
        },
      },
    },
    routes: {
      "POST /scrape-linkedin-profile": "linkedin_scrapper.handler",
    },
  });

  stack.addOutputs({
    ApiEndpoint: api.url,
  });
}