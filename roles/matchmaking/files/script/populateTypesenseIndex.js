
const yaml = require('js-yaml');
const fs = require('fs');
require("dotenv").config();

const CONFIG = yaml.load(fs.readFileSync('./config.yaml', 'utf8'));
const Typesense = require("typesense");

function resolve(path, obj) {
  return path.split('.').reduce(function(prev, curr) {
      return prev ? prev[curr] : null
  }, obj || self)
}

module.exports = (async () => {
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

  console.log("Config: ", TYPESENSE_CONFIG);

    // create Typesense client
  const typesense = new Typesense.Client(TYPESENSE_CONFIG);

  const schema = {
    name: CONFIG.index_name,
    num_documents: 0,
    fields: CONFIG.fields,
  };

  const records = require(CONFIG.import_file_path)

  try {
    const collection = await typesense.collections(CONFIG.index_name).retrieve();
    console.log("Found existing collection of records");
    console.log(JSON.stringify(collection, null, 2));

    if (collection.num_documents !== records.length) {
      console.log("Collection has different number of documents than data");
      console.log("Deleting collection");
      await typesense.collections(CONFIG.index_name).delete();
    }
  } catch (err) {
    console.error(err);
  }

  console.log("Creating schema...");
  console.log(JSON.stringify(schema, null, 2));

  await typesense.collections().create(schema);

  console.log("Populating collection...");

  mapped_records = records.map(record => {

    try {

      let mapped = {}
      let has_error = false

      CONFIG.fields.forEach(field => {
        let value = resolve(field.data_name, record)
        
        // if field is required and but not defined => record has an error
        if (field.is_required && value === undefined) {
          has_error = true
          console.log(`${field.name} is missing for ${record.id}`)
          return
        }

        default_value = field.type == "string[]" 
          ? [field.default_value] 
          : field.default_value  

        mapped[field.name] = value || default_value        

      });

      if(has_error) {
        throw Exception("missing first required data");
      }

      return mapped;
    } 
    catch (ex) {
        console.log(`Cannot import following record: ${record.id}`);
    }

  })
  .filter(x => x!==undefined);

  try {
    const returnData = await typesense
        .collections(CONFIG.index_name)
        .documents()
        .import(mapped_records);

    console.log("Return data: ", returnData);
    } catch (err) {
    console.error(err);
    console.error(err.importResults)
    }
})();