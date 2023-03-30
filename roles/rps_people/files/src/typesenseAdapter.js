import jQuery from "jquery";
window.$ = jQuery; // workaround for https://github.com/parcel-bundler/parcel/issues/333

import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";

const host = process.env.VUE_APP_TYPESENSE_HOST || window.location.host;
const protocol = process.env.VUE_APP_TYPESENSE_PROTOCOL || window.location.protocol.slice(0,-1);
let port = process.env.VUE_APP_TYPESENSE_PORT || window.location.port;
if (port == "") {
  if (protocol == "http" ) {
    port = 80;
  } else {
    port = 443;
  }
}
const TYPESENSE_SERVER_CONFIG = {
  apiKey: process.env.VUE_APP_TYPESENSE_SEARCH_ONLY_API_KEY, // Be sure to use an API key that only allows searches, in production
  nodes: [
    {
      host,
      port,
      protocol,
      path: process.env.VUE_APP_TYPESENSE_PATH || "/"
    },
  ],
  numRetries: 8,
  useServerSideSearchCache: true,
};

let INDEX_NAME = process.env.VUE_APP_COLLECTION_NAME;

console.log(`${INDEX_NAME} - index name`);
console.log(process.env);
console.log(TYPESENSE_SERVER_CONFIG);


export default function (authorization) {
  return new TypesenseInstantSearchAdapter({
    server: {
      ...TYPESENSE_SERVER_CONFIG,
      additionalHeaders: {
        Authorization: authorization,
      },
    },
    // The following parameters are directly passed to Typesense's search API endpoint.
    //  So you can pass any parameters supported by the search endpoint below.
    //  queryBy is required.
    additionalSearchParameters: {
      query_by: "location,num_projects,department,job,last_name",
      query_by_weights: "2,2,1,1,1",
      sort_by: "_text_match(buckets: 10):desc",
      num_typos: 3,
      typo_tokens_threshold: 1,
    },
    
  });
}
// export const search = instantsearch({
//   searchClient,
//   indexName: INDEX_NAME,
//   routing: true,
//   // searchFunction(helper) {
//   //   if (helper.state.query === '') {
//   //     $('#results-section').addClass('d-none');
//   //   } else {
//   //     $('#results-section').removeClass('d-none');
//   //     helper.search();
//   //   }
//   // },
// });
