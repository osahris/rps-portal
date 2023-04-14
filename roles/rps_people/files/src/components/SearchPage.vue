<template>
  <div class="main ">  
    <ais-instant-search :search-client="searchClient" :index-name="config.index_name"
                        :search-function="searchFunction">
      <div class="hero is-primary is-medium"> 
        <h1 class="title">Wen suchen Sie?</h1>
        <p class="subtitle">Geben Sie gerne Schlagworte, Fachrichtungen, Institutionen unten in die Suchleiste ein und klicken Sie auf “Los!”</p>
        <div class="container">
        <ais-search-box id="searchbox"
                        placeholder="Search for users..." 
                        submit-title="Go"
                        :show-loading-indicator="true"
                        :class-names="{
            'ais-SearchBox-input':'input longer',
            'ais-SearchBox-submit':'button',
            'ais-SearchBox-form':'flex',
            'ais-SearchBox-reset':'d-none',
          }">
          <template v-slot:submit-icon>🔎</template>
        </ais-search-box>
        
          <ais-stats id="search-stats" class="d-none" data-layout="mobile">
            <template v-slot="{ nbHits }">
              <span class="ais-Stats-text subtitle">
                <strong>{{ nbHits }}</strong> <span v-if="nbHits == 1">Ergebnis</span><span v-else>Ergebnisse</span>
              </span>
            </template>
          </ais-stats>
        </div>
      </div>
  
      <!-- regular Vue InstantSearch app inside -->
      <div id="main-search" class="d-none">
        <div class="column is-one-third">
          <h2 class="subtitle">Filters</h2>
          <ais-clear-refinements data-layout="desktop"
              :class-names="{
                  'ais-ClearRefinements-button': 'button',
                  'ais-ClearRefinements-button--disabled': 'button disabled',
                }">
            <template v-slot:resetLabel>
              <div class="clear-filters">              
                Clear filters
              </div>
            </template>
          </ais-clear-refinements>    
  
          <SearchRefinement v-for="refinement in facetFields" :key="refinement.name"
              :header_text="refinement.display_name" 
              :search_attribute="refinement.name" 
              :placeholder="'Suche nach ' + refinement.display_name" />
                 
        </div>
        <div class="column container is-two-third">
          <ais-hits id="hits">
            <template v-slot="{ items }">
              <ul>
                <li v-for="item in items" :key="item.last_name" class="box">
                  <div v-for="field in config.fields" :key="field.name">
                    <div v-if="field.type == 'string[]' && item[field.name][0] && item[field.name][0] != field.default_value">
                      <p>{{field.display_name}}:</p>
                      <ul>
                        <li v-for="subItem in item[field.name]" :key="subItem">
                          {{ subItem }}
                          <ais-highlight :attribute="field.name" :hit="item" />
                        </li>
                      </ul>
                    </div>
                    <div v-else-if="item[field.name] && item[field.name] != field.default_value">
                      {{field.display_name}}:
                      <ais-highlight :attribute="field.name" :hit="item" />
                    </div>
                  </div>
  
                </li>
                <li v-for="item in items" :key="item.last_name" class="box">
                  <h1 class="subtitle" v-if="item.title != 'none'">{{ item.title }} {{ item.first_name }} {{ item.last_name }} </h1>            
                  <h1 class="subtitle" v-else>{{ item.first_name }} {{ item.last_name }} </h1>            
                  <div>
                    from 
                    <a role="button" class="clickable-search-term">
                      <ais-highlight attribute="location" :hit="item" />
                    </a><br>
                    <a role="button" class="clickable-search-term">
                      <ais-highlight attribute="department" :hit="item" />
                    </a>
                  </div>            
                  <div v-if="item.num_projects && item.num_projects[0] != 'None'">
                    working in 
                      <span v-for="project in item.num_projects" :key="project">
                        {{project}}
                      </span>
                  </div>
  
                  <div v-if="item.job && item.job != 'none'">
                    Functions: {{ item.job }}
                  </div>
                </li>
              </ul>
            </template>
          </ais-hits>
        </div> 
      </div>
    </ais-instant-search>
  </div>
  </template>
  
  <script>
  import config from '../../config.yaml'
  import jQuery from 'jquery';
  window.$ = jQuery;
  import createSearchClient from '../typesenseAdapter.js'
  import { AisInstantSearch, AisSearchBox, AisStats,  AisHits, AisHighlight, AisClearRefinements } from 'vue-instantsearch/vue3/es';
  
  import SearchRefinement from './SearchRefinement.vue'
  
  console.log(config)
  
  export default {
    name: 'SearchPage',
    props: {
      'authorization': Object,
    },
    components: {
      AisInstantSearch, 
      AisSearchBox,
      AisHits,
      AisHighlight,
      AisClearRefinements,
      AisStats,
      // eslint-disable-next-line
      jQuery,
      SearchRefinement,
    },
    setup(props) {
      return {
        searchClient: createSearchClient(props.authorization).searchClient,
      }
    },
    data () {
      return {
        firstQuery: true,
        config : config
      }
    },
    methods: {
      searchFunction(helper) {
        if (helper.state.query === '' && this.firstQuery) {
          $('#main-search').addClass('d-none');
          $('#search-stats').addClass('d-none');
          this.firstQuery = false;
        } else {
          $('#main-search').removeClass('d-none');
          $('#search-stats').removeClass('d-none');
        }
        helper.search();
      },
    },
    computed : {
      facetFields() {
        console.log(this.config.fields)
        let fields = this.config.fields.filter(field => field.facet)
        return fields
      },
      imgField() {
        return "svg"
  
      }
    }
  }
  
  </script>
  