# Projects

Before that setup the default client, or will inject your own client.

## Creating

```python
new_project = {'name': 'Project One',
                   'description': 'Project desc',
                   'team_id' : 5,
                   'color': '#222'}
project = await alo_host.projects.create(**new_project)
```

## Updating

```python
id_project = 119
updated_fields= {'description': 'foo'}
project = await alo_host.projects.update(id_project, **updated_fields)
```

## Get by id

```python
id_project = 119
linked_file = await alo_host.projects.get(id_project)
```

## Deleting by id

When None is returned this means it was successfull

```python
id_project = 119
await alo_host.projects.delete(id_project)
```

## Listing

Returns a list of all labels

```python
all_linked_files = await alo_host.projects()
```

## Listing all stories for a project

```python
id_project = 119
member = await alo_host.member()
project_stories = await alo_host.projects(id_project, 'stories')
```
