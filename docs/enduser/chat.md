The chat app Element Web is used to arrange discussions between the users and keep them well-organized and separated by topics into relevant chat rooms.

The chat is reachable at address https://chat.<domain_name> .

## Activating push notifications

Many modern applications support push notifications. In contrast to desktop apps where this feature is natively on, the web-based applications often get their push notifications blocked by default by the browser. To fix this for a particular instance of an Element Web chat, do the following steps:
- Login to your account
- Go to Settings, then choose Notifications, then try to activate the trigger "Enable desktop notifications for this session". If you get a warning that the feature is blocked, pay attention to the relevant button that will now appear in your browser (probably near the URL block) asking if you wish to let this website get persmission to send push notifications
- Grant the permission to the website and press the trigger in the Element Web Settings again
- If this did not work, check whether you have put the chat address to the block list in your browser settings
- Additionally check whether the browser setting "block all new push notification activation requests" is on or off

## Storing the encrypting keys safely

Element Web provides encryption for your messages keeping your conversations safe. All the content is stored on the Matrix server but the keys to decrypt it are only stored on the end-user side. If you clear the cache in your browser, you will likely see "Unable to decrypt message" warnings. The content of the messages can only be decrypted if at least one member of the converstion still has the decryption key. To be on the safe side, we recommend you to make a backup of your decryption keys. In order to do so, do the following steps:
- Login to your account
- Go to Settings, then choose Security & Privacy, and configure the storage of the backup keys.
- Save them in a proper place of your choice. Never share them with anyone 

## Accessing the API

Besides the generic usage of the chat through your browser, you may enreaching your experience with the Element Web by getting direct access to the Matrix server via API. For this purpose you will need to add your token to all your requests. To generate or find it, do the following steps:

- Login to your account
- Go to Settings, then choose Help & About, then scroll down to Advanced and find the token. Never share it with anyone
- Add the following header to your requests: "Authorization: Bearer <token>"
