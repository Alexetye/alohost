# Labels

Before that setup the default client, or will inject your own client.

## Creating

```python
new_label = {'name': 'first label'}
label = await alo_host.labels.create(**new_label)
```

## Updating

```python
id_label = 116
updated_fields_label= { 'name': 'Label updated now'}
label = await alo_host.labels.update(id_label, **updated_fields_label)
```

## Get by id

```python
id_label = 116
label = await alo_host.labels.get(id_label)
#epic = await alo_host.labels(id_epic) alternative 
print(label)
```

## Deleting by id

When None is returned this means it was successfull

```python
id_label = 116
await alo_host.labels.delete(id_label)
```

## Listing

Returns a list of all labels

```python
list_labels = await alo_host.labels()
```

## List Label Epics

```python
id_label = 14
epics = await alo_host.labels.get(id_label, 'epics')
#epics = await alo_host.labels(id_label, 'epics')
```

## List Label Stories

```python
id_label = 14
stories = await alo_host.labels(id_label, 'stories')
#stories = await alo_host.labels.get(id_label, 'stories')
```
