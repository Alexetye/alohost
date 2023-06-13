# Epics

Before that setup the default client, or will inject your own client.

## Creating

```python
new_epic = { 'name': "Epic One", 
             'description': 'Epic description',
             'state': 'in progress'}
             
epic = await alo_host.epics.create(**new_epic)
```

## Updating

```python
id_epic = 112
updated_fields_epic = { 'description': 'Changed description','state': 'done'}
epic = await alo_host.epics.update(id_epic, **updated_fields_epic)
```

## Get by id

```python
id_epic = 112
epic = await alo_host.epics.get(id_epic)
#epic = await alo_host.epics(id_epic) alternative 
print(epic)
```

## Deleting by id

When None is returned this means it was successfull

```python
id_epic = 112
await alo_host.epics.delete(id_epic)
```

## Listing

Returns a list of all epics

```python
list_of_epics = await alo_host.epics()
```

## Create Epic Comment 

```python
id_epic = 113
id_author = '6028be51'
new_comm = {'author_id': id_author, 'text': 'new comment'}
comment = await alo_host.epics.create(id_epic, 'comments', **new_comm)
```

## Get Epic Comment 

```python
id_epic = 113
id_comment = 114
comment = await alo_host.epics.get(id_epic, 'comments', id_comment)
```

## Update Epic Comment

```python
id_epic = 113
id_comment = 114
updated_fields_comm = {'text': 'changed text'}
comment = await alo_host.epics.update(id_epic, 'comments', id_comment,
                                                    **updated_fields_comm)
```

## Create Epic Comment Comment

```python
id_epic = 113
id_comment = 114
new_comm = {'text': 'sub comment'}
comment = await alo_host.epics.create(id_epic, 'comments', id_comment, **new_comm)
```

## Delete Comment

```python
id_epic = 113
id_comment = 114
await alo_host.epics.delete(id_epic, id_comment)
```

## List Epic Comments

```python
list_comment_of_epic = await alo_host.epics(id_epic, 'comments')
```

## List Epic Stories

```python
list_stories_of_epic = await alo_host.epics(id_epic, 'stories')
```
