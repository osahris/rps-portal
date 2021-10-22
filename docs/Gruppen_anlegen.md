# Gruppen anlegen in der RPS

## Gruppenkonfiguration

Die Gruppen müssen aktuell in einer Konfigurationsdatei mit dem Namen groups.yaml im jeweiligen Konfigurationsrepository des Projektes mit dem Pfad inventory/group_vars/all/groups.yaml eingetragen werden. Diese Datei ist in der [YAML-Sprache](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) verfasst.

Die Gruppen werden unter dem Schlüssel `global_groups` angelegt. Beispiel:

```
global_groups:
  - name: new_registered_users
    membership_source: accounts
  - name: approved_users
    membership_source: accounts
  - name: hello
    title: Hello!
    description: bla
    mailinglist:
      type: incoming
  - name: news
    title: News and Announcements
    description: News and Announcements
    mailinglist:
      type: newsletter
```

Erklärung der einzelnen Attribute einer Gruppe:
- `name`: Name der Mailingliste. Dies ist ein URL-Pfad, dieser darf keine Leerzeichen oder Sonderzeichen wie äöüß enthalten. - und _ sind zulässig. Dies ist die maschinenlesbare ID der Gruppe.
- `title` _(optional)_: Hier wird der Name der Gruppe in einem Format für die Anzeige in Übersichtslisten und im Titel auf der Gruppenübersichtsseite eingetragen.
- `description` _(optional)_: Eine Erklärung was es mit dieser Gruppe auf sich hat und wer in die Gruppe einbezogen werden soll.
- `membership_source` _(optional)_: Hier wird angegeben aus welchem Dienst die Gruppe bei der Gruppensynchronisation die Mitgliedschaften als Quelle beziehen soll. Bei allen anderen Diensten werden die Gruppenmitgliedschaften überschrieben. Wenn es nicht angegeben ist, wird als Quelle `group_sync_default_membership_source` verwendet.
- `mailinglist` _(optional)_: Wenn Dieses Attribut vorhanden ist wird eine Mailingliste für die Gruppe angelegt. Die Unterattribute hier sind wie folgt:
  - `type`: Mailinglistentyp, hier wird definiert was für eine Art von Mailingliste es ist. Die möglichen Einträge sind:
    - `newsletter`: nur Mailadressen die in `groups_global_mailinglist_editors` aufgeführt sind können an diese Mailingliste schreiben.
    - `incoming`: Jede beliebige Mailadresse, also auch Externe, können an diese Mailingliste schreiben.
    - `internal`: Die Mitglieder der Gruppe und Personen die in `groups_global_mailinglist_editors` aufgeführt sind können an diese Gruppe schreiben.

Für Änderungen an der Gruppendefinition sollte dann ein Merge Request angelegt werden, der von den verantwortlichen Administrator:innen dann im Anschluss deployed wird.

## Gruppenhierachisierung

Um eine Gruppenhierachisierung vorzunehmen können Einträge im `group_hierarchy`-Schlüssel in der o.g. groups.yaml-Datei vorgenommen werden. Die Gruppenhierachisierung sorgt dafür dass Personen aus den höheren Gruppen automatisch in die niegrigeren Gruppen in dem Baum eingefügt werden. Die höheren Gruppen sind im `children`-Element in der jeweiligen Gruppe aufgeführt. Beispiel:

```
group_hierarchy:
  - name: maingroup
    children:
      - name: subgroup
        children:
          - name: subsubgroup
```


Es sind auch Querschnittsgruppen möglich, dabei werden die Personen nur in die tiefere Gruppe hinzugefügt, wenn Personen in beiden Gruppen sind. Beispiel:

```
group_hierarchy:
  - name: tr-2-uk-koeln
    type: intersection
    children:
      - name: tr-2
      - name: uk-koeln
```

Erklärung der einzelnen Attribute einer Gruppenhierachisierung:

- `name`: Gruppen-ID, sollte gleich sein wie der `name` in `global_groups`.
- `type` _(optional)_: Bei `union` (Standard) wird eine [Vereinigungsmenge](https://en.wikipedia.org/wiki/Union_(set_theory%29), bei `intersection` eine [Schnittmenge](https://en.wikipedia.org/wiki/Intersection_(set_theory%29) der höheren Gruppen gebildet.
- `children` _(optional)_: Hier werden die höheren Gruppen aufgeführt. Eine rekursive Verschachtelung ist möglich.


## Deployment

Das Deployment durch die verantwortliche Administrator:in erfolgt nachdem das lokale git-Repository synchronisiert wurde wie folgt:

`ansible-playbook -i example-suite/inventory/ rps/groups-update.yaml`
