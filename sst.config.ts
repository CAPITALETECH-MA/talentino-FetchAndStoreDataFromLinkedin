import { SSTConfig } from "sst";
import {API} from "./stacks/Mystack";

export default {
  config(_input) {
    return {
      name: "linkedin_scrapper-app",
      region: "eu-west-3",
    };
  },
  stacks(app) {
    app.stack(API);
  }
} satisfies SSTConfig ;