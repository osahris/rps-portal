<template>
    <div class="user-hit-div">
        <h3 class="text-primary font-weight-light font-letter-spacing-loose mb-0">
            {{ user?.title }} {{ user.first_name }} {{ user.last_name }}
        </h3>
        <div>
            from
            <a role="button" class="clickable-search-term">{{#helpers.highlight}}{ "attribute": "location" }{{/helpers.highlight}}</a>
            <a role="button" class="clickable-search-term">{{#helpers.highlight}}{ "attribute": "department" }{{/helpers.highlight}}</a>
        </div>
        <div v-if="num_projects && num_projects[0] != 'none'" class="mt-3">
            working in <a v-for="project in num_projects">{{project}}</a>
        </div>
        <div v-if="job" class="text-muted small mb-2">
            Functions: {{ job }}
        </div>
    </div>
</template>

<script>
export default {
  name: 'UserHits',
  props: {
    user: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
