# NUM Matchmaking Prototype


## Description
for information look [here] (https://gitlab.com/idcohorts/NUM/num-matchmaking-prototype).

More Info Material:

- [Typesense API Documentation](https://typesense.org/docs/0.23.1/api/search.html)
- [Best YouTube Tutorial for full-development](https://www.youtube.com/watch?v=iO0d_Ncjc7U&ab_channel=CoderOne)
- [Vue + TypeSense examples in pretty github repo](https://github.com/algolia/vue-instantsearch/tree/master/examples)
- [Typesense documentation](https://typesense.org/docs/guide/installing-a-client.html)
- [Algolia Vue documentation](https://www.algolia.com/doc/api-reference/widgets/vue/)

## Badg
## Installation
1. Following has to be installed:
- Docker
- yarn
- npm

2. Then users.json needs to be placed inside num-matchmaking-prototype/script/data.

3. Install all dependencies:

``` sh
yarn
```

4. Start typesense server:

``` sh
yarn start-typesense-server
```

5. Populate typesense server:

``` sh
yarn populate-typesense-server
```

6. Load dev server and initialize client:

``` sh
yarn serve
```

## Usage


## Support


## Roadmap
Todos:
Funcionality:
- [ ] create synonym [list] (https://typesense.org/docs/0.23.0/api/synonyms.html)
- [ ] add Keycloak authentification

Database:
- [ ] fill information by Orcid
- [ ] sync script with keycloak
- [ ] data cleaning scripts & quality assurance

Design:
- [ ] custom CSS
- [ ] add small animations
- [ ] user site

## Contributing


## Authors and acknowledgment


## License


## Project status
