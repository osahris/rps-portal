---
layout: docs
title: "Docs for Users"
---
# Manual for users

Dear users,

in this area you will find information that hopefully will ease your working with our infrastructure.
Please study the page concerning your use case carefully. If you happen to find any information lacking or missing completely, we would appreciate a quick feedback. (Should you feel that a point falls into your area of expertise, you are of course invited to extend the page yourself.)

A regular user, provided that they were given sufficient rights, may enjoy using the stack of services that is briefly described below. Here we intentionally avoid mentioning any technical peculiarities that can instead be found in manuals for [**Admins**](./admin) and  [**Developers**](./developer).


## Keycloak
**Identity and access management.**  
This so-called single-sign-on (SSO) service provides access to the other tools in the suite. In the RPS Keycloak is the entry point, the first what the users will see when they arrive to your portal. If the user is granted additional rights, they may also manage the scopes for others. For the rest it will seem to be just a friendly "please login" window.  
More info: [official docs - managing users](https://www.keycloak.org/docs/latest/server_admin/index.html#assembly-managing-users_server_administration_guide)


## Groups Interface
**Manage access to services and their parts.**  
The user with sufficient right may use this service to view, create, edit the groups for other users. Keeping in mind the relatively complex structure of [Keycloak](./#keycloak), we introduce this home-made service to provide the user with a handy and intuitive interface to edit the access rights to others.  
More info: [admin's manual](./admin/#groups-interface)


<!-- ## RocketChat
**Communication platform.**  
Highly customizable chatting tool that requires no rocket-science knowledge to start using it. With RocketChat it is easy to organize a convenient structure of the chat rooms to keep in touch with your colleagues spreding the discussions into multiple chats.  
More info: [official docs](https://docs.rocket.chat/) -->


## Element web
**Chat platform.**  
Highly customizable chatting tool that can be run straight from the browser, but alternatively can be used with a desktop or mobile app. With Element Web it is easy to organize a convenient structure of the chat rooms to keep in touch with your colleagues spreding the discussions into multiple chats.
More info: [official docs](https://web-docs.element.dev/Element%20Web/index.html)


## Discourse
**Discussion forum platform.**  
Sometimes a chat is not enough. For such cases we include the Discourse service to the RPS which allows for a broader list of means of communication in a form closer to a forum.  
More info: [official docs](https://docs.discourse.org/)


## Nextcloud
**Documents storing, sharing and co-editing platform.**  
Now that we're talking via [RocketChat](./#rocketchat) and [Discourse](./#discourse), time to have a handy tool to store, share and co-edit the documents in the cloud.  
More info: [official docs](https://nextcloud.com/support/)


## Wiki-Bookstack
**Information systematization tool.**  
For a bigger working group sooner or later comes the question of centralizing and structuring the core internal information. Having your own encyclopedia is a reasonable choice, especially if it is such a light-weight and easy-to-use one as Wiki-Bookstack in the RPS.  
More info: [official docs](https://www.bookstackapp.com/docs/)


## Budibase
**Low-code database framework.**  
For building forms quickly and pleasant working structured data. 

A simple example of its application could be a construction of a form to collect participants data for some event or project. With Budibase this can be done in a few minutes! (All right, first time it will take you longer...)  
More info: [official promo in YouTube](https://www.youtube.com/watch?v=xoljVpty_Kw)


<!-- ## OpenProject
**Short and very general description**  
A bit more detailed description and maybe reasoning to add it to RPS. This text in smaller size

Comments on additional features and configurations that are added when this service is integrated to the RPS.  
More info: [official docs](https://www.openproject.org/docs/) -->

## Other available topics

 * [Using the email system](email)
 * [Usage of the mailing lists](mailinglists)
 * [The main wiki](wiki)

