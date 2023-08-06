from typing import Union


class Table:
    """Hopara Table type.
    Table support all the following types for its columns:
     - ``STRING``, ``INTEGER``, ``DECIMAL``, ``BOOLEAN``
     - ``DATETIME``: python datetime format
     - ``AUTO_INCREMENT``: auto-increment integer
     - ``MONEY``: currency values
     - ``JSON``: json column, can be used for regular Json or a (GeoJson)(https://geojson.org/)
     - ``STRING_ARRAY``: string array column: ``['value1', 'value2']``
     - ``POLYGON``: a string representing a Polygon ``POLYGON ((40 40, 20 45, 45 30, 40 40))`` in [WKT format](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
     - ``MULTIPOINT``: a string representing a MultiPoint ``MULTIPOINT ((10 40), (40 30), (20 20), (30 10))`` in WKT format
     - ``IMAGE``: a string that representing an image ``data:[<mediatype>][;base64],<data>`` in [Data URIs format](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
    """
    def __init__(self, name: str):
        """Initialize a table with a name.
        :param name: name of the table.
        :type name: str
        """
        self.name = name
        self.__table = {'createStats': False}
        self.__columns = {}

    def get_payload(self) -> dict:
        self.__table['columns'] = [dict(properties, **{'name': name}) for name, properties in self.__columns.items()]
        return self.__table

    def set_create_stats(self, create_stats: bool):
        self.__table['createStats'] = create_stats

    def add_column(self, column_name: str, column_type: str):
        """Add a new columns to the table.
        :param column_name: name of the column
        :type column_name: str
        :param column_type: type of the column. See more details about the types on the class description above.
        :type column_type: str
        """
        self.__columns[column_name] = {}
        if column_type:
            self.__columns[column_name]['type'] = column_type
        if column_name.startswith('_'):
            self.__columns[column_name]['label'] = column_name.lstrip('_')

    def __update_column_properties(self, column_name: Union[str, list], properties: dict):
        if isinstance(column_name, str):
            self.__columns[column_name].update(properties)
        else:
            for col_name in column_name:
                self.__columns[col_name].update(properties)

    def set_columns_type(self, column_name: Union[str, list], column_type: str):
        """Change a previously set or missing column type.
        :param column_name: column or list of column to have the type changed
        :type column_name: str | list
        :param column_type: type of the columns. See more details about these types at this class description above.
        :type column_type: str
        """
        self.__update_column_properties(column_name, {'type': column_type})

    def set_unique_key_columns(self, column_name: Union[str, list]):
        """Set a column as unique, same value will update the same row instead of add a new one.
        :param column_name: column or list of column that must have unique values
        :type column_name: str | list
        """
        self.__update_column_properties(column_name, {'uniqueKey': True})

    def set_primary_key_column(self, column_name: Union[str, list]):
        """Set a column as primary key
        :param column_name: column or list of column that must be primary key
        :type column_name: str | list
        """
        self.__update_column_properties(column_name, {'primaryKey': True})

    def set_searchable_columns(self, column_name: Union[str, list]):
        """Set a column as searchable, which means an index will be created to speed up the queries
         :param column_name: column or list of column that must have an index created
         :type column_name: str | list
         """
        self.__update_column_properties(column_name, {'searchable': True})

    def disable_update_on_upsert(self, column_name: Union[str, list]):
        """When you need continually update the same row in a table, you can lose the information in the columns that you don't send on the new data.
        To avoid it, you can lock some columns and update the other without losing information.
        :param column_name: column or list of column that must have update disabled on upsert
        :type column_name: str | list
        """
        self.__update_column_properties(column_name, {'updateOnUpsert': False})
