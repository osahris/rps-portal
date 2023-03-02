<template>
  <ais-panel
        :class-names="{
          'ais-Panel': 'section ',
        }">
      <template v-slot:header><p class="subtitle">{{header_text}}</p></template>

      <template v-slot:default>
        <ais-refinement-list
            :attribute="search_attribute"
            searchable
            show-more
            :searchablePlaceholder="placeholder"
            :class-names="{
              'ais-RefinementList-checkbox': 'checkbox ',
              'ais-RefinementList-count': 'tag is-info is-light',
              'ais-RefinementList-submit':'button',
              'ais-RefinementList-showMore':'button',
            }"/>
      </template>
  </ais-panel>
</template>

<script>
import { AisPanel, AisRefinementList } from 'vue-instantsearch/vue3/es';

export default {
  name: 'SearchRefinement',
  components : {
    AisPanel,
    AisRefinementList
  },
  props: {
    header_text: String,
    search_attribute: String,
    placeholder: String,
  }
}
</script>