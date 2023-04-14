<template>
  <SearchPage v-if="authorization" :authorization="authorization" />
</template>

<script>
class Authorization {
  constructor(keycloak) {
    this.keycloak = keycloak;
  }
  toString() {
    return "Bearer " + this.keycloak.token;
  }
}

import SearchPage from "./components/SearchPage.vue";
import Keycloak from "keycloak-js";

export default {
  name: "App",
  components: {
    SearchPage,
  },
  data() {
    return {
      authorization: null,
    };
  },
  mounted() {
    const keycloak = new Keycloak({
      url: process.env.VUE_APP_KEYCLOAK_URL,
      realm: process.env.VUE_APP_KEYCLOAK_REALM,
      clientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,
    });
    keycloak.onTokenExpired = () => {
      console.log("token expired", keycloak.token);
      keycloak
        .updateToken(30)
        .then(() => {
          console.log("successfully get a new token", keycloak.token);
        })
        .catch((e) => {
          console.log(e);
        });
    };
    keycloak
      .init({
        onLoad: "login-required",
        checkLoginIframe: false,
      })
      .then(async (authenticated) => {
        if (!authenticated) {
          alert("failed to authenticate");
          return;
        }
        console.log("keycloak auth successful");
        this.authorization = new Authorization(keycloak);
      });
  },
};
</script>
