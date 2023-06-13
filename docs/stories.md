# Stories

Before that setup the default client, or will inject your own client.

## Creating

```python
new_story = { 'comments':[ {'text': 'A comment to start the story'} ],
                'deadline': '2016-12-31T12:30:00Z',
                'estimate': 8,
                'labels': [ {'name': 'High'}, {'name': 'bug' } ],
                'name': "Can't login and get 503",
                'project_id': 4,
                'story_type': 'bug',
                'tasks': [ {'description': 'Monitor server load' } ]}
story = await alo_host.stories.create(**new_story)
```

## Create Multiple Stories

```python
many_stories = { "stories": [
    {'name': "Login",
     'project_id': 4,
     'story_type': 'bug'}, 
    {
     'name': "Log Out",
     'project_id': 4,
     'story_type': 'feature'}]}
stories = await alo_host.stories.create('bulk',**many_stories)
```

## Updating

```python
id_story = 120
updates = { 
            'name': "Can't login and get 503",
            'project_id': 4,
            'story_type': 'feature'}
story = await alo_host.stories.update(id_story, **updates)
```

## Update Multiple Stories

```python
many_stories = { 'story_ids': [125,126], 'project_id': 4,'story_type': 'bug'} 
stories = await alo_host.stories.update('bulk',**many_stories)
```

## Get by id

```python
id_story = 120
linked_file = await alo_host.stories.get(id_story)
```

## Deleting by id

When None is returned this means it was successfull

```python
id_story = 120
await alo_host.stories.delete(id_story)
```

## Delete Multiple Stories

```python
many_stories = { 'story_ids': [125,126]} 
await alo_host.stories.delete('bulk', **many_stories)
```

## Listing

Returns a list of all labels

```python
all_linked_files = await alo_host.stories()
```

## Story History

```python
id_story = 120
story = await alo_host.stories.history(id_story)
```

