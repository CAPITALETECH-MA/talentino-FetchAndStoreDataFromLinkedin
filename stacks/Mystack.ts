import { StackContext, Api, Function} from "sst/constructs";

export function API({ stack }: StackContext) {
  const linkedinScrapperFunction = new Function(stack, "LinkedinScrapper", {
    handler: "functions/linkedin_scrapper.handler",
    runtime: "python3.9",
    environment: {
      SUPABASE_URL: process.env.SUPABASE_URL || "",
      SUPABASE_KEY: process.env.SUPABASE_KEY || "",
      PROXYCURL_API_KEY: process.env.PROXYCURL_API_KEY || "",
      SCRAPIN_API_KEY: process.env.SCRAPIN_API_KEY || "",
    },
  });

  const api = new Api(stack, "api", {
    routes: {
      "POST /scrape-linkedin-profile": linkedinScrapperFunction,
    },
  });
  stack.addOutputs({
    ApiEndpoint: api.url,
  });
}