import { Opal } from "../dist/index";

const client = new Opal({
  apiKey: 'your-api-key',
  baseUrl: 'https://jsonplaceholder.typicode.com',
});

client.events
  .create_opal_event(undefined)
  .then((p) => {
    console.log(`Created new post with id ${p.status}`);
  });
