# Files

Before that setup the default client, or will inject your own client.

## Upload Files

Upload one or more Files, which can then be associated to a Story Description, Story Comment, or Epic Comment.

```python
new_file = {'file' : 'D:/112.py'}
file = await alo_host.files.upload(**new_file)
```

## Updating

```python
id_file = 117
update_fields = {'name': 'New file name', .files.get(id_file)
```

## Deleting by id

When None is returned this means it was successfull

```python
id_file = 117
await alo_host.files.delete(id_file)
```'description': 'new desc'}
file = await alo_host.files.update(id_file, **update_fields)
```

## Get by id

```python
id_file = 117
file = await alo_host

## Listing

Returns a list of all files

```python
files = await alo_host.files()
```
