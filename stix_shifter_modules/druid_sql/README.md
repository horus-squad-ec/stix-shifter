# Apache Druid Connector

This is a STIX shifter transmission module for querying a Druid database using its SQL endpoint.

## Testing

If you don't have an Apache Druid for testing, follow this [tutorial](https://druid.apache.org/docs/latest/tutorials/index.html) to create one.

The tests omit user/password authentication and use the `wikipedia` dataset that comes with Apache Druid.

### Tranmission ping

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' ping
```

### Tranmission is\_async

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' is_async
```

### Transmission query

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' query 'SELECT * FROM wikipedia'
```

### Transmission status

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' status 0
```

### Transmission results

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' results 'SELECT * FROM wikipedia' 1 1
```

### Transmission delete

```
python main.py transmit druid_sql '{"host":"<host address>", "port":8082}' '{"auth": {}}' delete 0
```
