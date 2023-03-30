import instantsearch from 'instantsearch.js/es';
import { searchClient } from './typesenseAdapter.js'
import {
  searchBox,
  stats,
  sortBy,
  configure,
  infiniteHits,
  refinementList,
} from 'instantsearch.js/es/widgets';
import jQuery from 'jquery';
window.$ = jQuery;

export function initializeSearch() {
    console.log("init");
    console.log(this.search);
    $('#searchbox').addClass('test-class');
    search.addWidgets([
        searchBox({
        container: '#searchbox',
        showSubmit: false,
        showReset: false,
        placeholder: 'Type in a song, artist or album name',
        autofocus: true,
        cssClasses: {
            input: 'form-control',
        }
        }),
        stats({
        container: '#stats',
        templates: {
            text: ({ nbHits, hasNoResults, hasOneResult, processingTimeMS }) => {
            let statsText = '';
            if (hasNoResults) {
                statsText = 'No results';
            } else if (hasOneResult) {
                statsText = '1 result';
            } else {
                statsText = `${nbHits.toLocaleString()} results`;
            }
            return `${statsText} found in ${processingTimeMS}ms.`;
            },
        },
        }),
        configure({
        hitsPerPage: 15,
        }),
        sortBy({
            container: '#sort-by',
            items: [
                { label: 'Recent first', value: `${INDEX_NAME}` },
                { label: 'Oldest first', value: `${INDEX_NAME}/sort/release_date:asc` },
            ],
            cssClasses: {
                select: 'custom-select custom-select-sm',
            },
        }),
        infiniteHits({
            container: '#hits',
            cssClasses: {
                list: 'list-unstyled grid-container',
                item: 'd-flex flex-column search-result-card bg-light-2 p-3',
                loadMore: 'btn btn-primary mx-auto d-block mt-4',
            },
            templates: {
                item(hit) {
                let hit_html = '<h3 class="text-primary font-weight-light font-letter-spacing-loose mb-0">'

                if (hit.title && hit.title != "none") {
                    hit_html += `${hit.title} `
                }
                hit_html += `${ hit.first_name } ${ hit.last_name }
                    </h3>
                    <div>
                        from 
                        <a role="button" class="clickable-search-term">${instantsearch.highlight({ "attribute": "location", hit})}</a>
                        <a role="button" class="clickable-search-term">${instantsearch.highlight({ "attribute": "department", hit})}</a>
                    </div>
                    `
                if (hit.num_projects && hit.num_projects[0] != "None" && hit.num_projects[0] != "none") {
                    hit_html += `<div>working in `;
                    for (let i = 0;i < hit.num_projects.length;i++) {
                        let projects = hit.num_projects;
                        hit_html += `<a role="button" class="clickable-search-term">${projects[i]}</a>`
                    }
                    hit_html += "</div>"
                }
                if (hit.job && hit.job != "none") {
                    hit_html += `
                    <div >
                        Functions: ${ hit.job }
                    </div>`;
                }
                return hit_html;
                },
                empty: 'No songs found for <q>{{ query }}</q>. Try another search term.',
                showMoreText: 'Show more',
            }
        }),
        refinementList({
            container: '#projects-refinement-list',
            attribute: 'num_projects',
            searchable: true,
            searchablePlaceholder: 'Search projects',
            showMore: true,
            cssClasses: {
              searchableInput: 'form-control form-control-sm mb-2 border-light-2',
              searchableSubmit: 'd-none',
              searchableReset: 'd-none',
              showMore: 'btn btn-secondary btn-sm align-content-center',
              list: 'list-unstyled',
              count: 'badge badge-light bg-light-2 ml-2',
              label: 'd-flex align-items-center',
              checkbox: 'mr-2',
            },
          }),
          refinementList({
            container: '#department-refinement-list',
            attribute: 'department',
            searchable: true,
            searchablePlaceholder: 'Search department',
            showMore: true,
            cssClasses: {
              searchableInput: 'form-control form-control-sm mb-2 border-light-2',
              searchableSubmit: 'd-none',
              searchableReset: 'd-none',
              showMore: 'btn btn-secondary btn-sm',
              list: 'list-unstyled',
              count: 'badge badge-light bg-light-2 ml-2',
              label: 'd-flex align-items-center',
              checkbox: 'mr-2',
            },
          }),
          refinementList({
            container: '#job-refinement-list',
            attribute: 'job',
            searchable: true,
            searchablePlaceholder: 'Search job',
            showMore: true,
            cssClasses: {
              searchableInput: 'form-control form-control-sm mb-2 border-light-2',
              searchableSubmit: 'd-none',
              searchableReset: 'd-none',
              showMore: 'btn btn-secondary btn-sm',
              list: 'list-unstyled',
              count: 'badge badge-light bg-light-2 ml-2',
              label: 'd-flex align-items-center',
              checkbox: 'mr-2',
            },
          }),
          refinementList({
            container: '#location-refinement-list',
            attribute: 'location',
            searchable: true,
            searchablePlaceholder: 'Search location',
            showMore: true,
            cssClasses: {
              searchableInput: 'form-control form-control-sm mb-2 border-light-2',
              searchableSubmit: 'd-none',
              searchableReset: 'd-none',
              showMore: 'btn btn-secondary btn-sm',
              list: 'list-unstyled',
              count: 'badge badge-light bg-light-2 ml-2',
              label: 'd-flex align-items-center',
              checkbox: 'mr-2',
            },
          }),
    ])
    function handleSearchTermClick(event) {
        const $searchBox = $('#searchbox input[type=search]');
        search.helper.clearRefinements();
        $searchBox.val(event.currentTarget.textContent);
        search.helper.setQuery($searchBox.val()).search();
    }

    search.on('render', function() {
        // Make artist names clickable
        $('#hits .clickable-search-term').on('click', handleSearchTermClick);
    });

    search.start();

    $(function() {
        const $searchBox = $('#searchbox input[type=search]');
        // Set initial search term
        // if ($searchBox.val().trim() === '') {
        //   $searchBox.val('Song');
        //   search.helper.setQuery($searchBox.val()).search();
        // }

        // Handle example search terms
        $('.clickable-search-term').on('click', handleSearchTermClick);

        // Clear refinements, when searching
        $searchBox.on('keydown', event => {
        search.helper.clearRefinements();
        console.log(event);
        });

        if (!matchMedia('(min-width: 768px)').matches) {
        $searchBox.on('focus, keydown', () => {
            $('html, body').animate(
            {
                scrollTop: $('#searchbox-container').offset().top,
            },
            500
            );
        });
        }
    });
    console.log(this.search);
}

export const INDEX_NAME = process.env.VUE_APP_COLLECTION_NAME;
export const search = instantsearch({
      searchClient,
      indexName: INDEX_NAME,
      routing: true,
      searchFunction(helper) {
        if (helper.state.query === '') {
          $('#results-section').addClass('d-none');
        } else {
          $('#results-section').removeClass('d-none');
          helper.search();
        }
      },
    });