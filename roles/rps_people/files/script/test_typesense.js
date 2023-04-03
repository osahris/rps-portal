const Typesense = require("typesense");
require("dotenv").config();

const TYPESENSE_CONFIG = {
    nodes: [
        {
        host: process.env.TYPESENSE_HOST,
        port: process.env.TYPESENSE_PORT,
        protocol: process.env.TYPESENSE_PROTOCOL,
        },
    ],
    apiKey: process.env.TYPESENSE_ADMIN_API_KEY,
};

// console.log("Config: ", TYPESENSE_CONFIG);


// create Typesense client
const typesense = new Typesense.Client(TYPESENSE_CONFIG);

module.exports = (async () => {
    let collections = await typesense.collections().retrieve()
    // console.log("collections")
    // console.log(collections)

    let searchParameters = {
        'q': 'Christan',
        'query_by': 'first_name',
        'filer_by': 'job:!= none'
        }
    let x = await typesense.collections("test").documents().search(searchParameters)
    console.log(x.hits[0])
})();
