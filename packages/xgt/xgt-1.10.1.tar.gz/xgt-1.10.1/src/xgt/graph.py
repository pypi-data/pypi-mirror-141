# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2022 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

import ast
import json
import math
import os.path
import sys
import traceback

import grpc

try:
  from collections.abc import Iterable
except ImportError:
  from collections import Iterable

from . import DataService_pb2 as data_proto
from . import DataService_pb2_grpc as data_grpc
from . import GraphTypesService_pb2 as graph_proto
from . import SchemaMessages_pb2 as sch_proto
from .common import (_assert_isstring, _assert_noerrors,
                     _get_valid_property_types_for_return_only,
                     _get_valid_property_types_to_create,
                     _validated_property_name,
                     _validated_property_type,
                     XgtNotImplemented,
                     XgtIOError, XgtValueError, XgtInternalError, XgtTypeError,
                     MAX_PACKET_SIZE)
from .job import Job

class HeaderMode:
  NONE = 'none'
  IGNORE = 'ignore'
  NORMAL = 'normal'
  STRICT = 'strict'

  _all = [NONE,IGNORE,NORMAL,STRICT]

def _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns = None):
  if row_labels is not None and row_label_columns is not None:
    error = ("Only one of row_labels and "
             "row_label_columns must be passed."
            )
    raise ValueError(error)
  if row_labels is not None and \
     not isinstance(row_labels, (list, tuple)):
    raise TypeError('row_labels must be a list or tuple of string labels.')
  if row_label_columns is not None and \
     not isinstance(row_label_columns, (list, tuple)):
    raise TypeError('row_label_columns must be a list or tuple.')

def _validate_column_mapping_in_ingest(frame_to_file_column_mapping):
  if frame_to_file_column_mapping is not None:
    for frame_col, file_col in frame_to_file_column_mapping.items():
      if not isinstance(file_col, (str, int)):
        error_string = 'The data type of "frame_to_file_column_mapping" ' + \
                       'is incorrect. Expects a dictionary with string ' + \
                       'keys and string or integer values.'
        raise TypeError(error_string)

def _set_column_mapping_in_ingest_request(request, frame_to_file_column_mapping):
  if frame_to_file_column_mapping is not None:
    request.column_mapping.has_mapping = True
    for frame_col, file_col in frame_to_file_column_mapping.items():
      if isinstance(file_col, str):
        name_mapping = data_proto.FrameColumnToSourceName()
        name_mapping.frame_column_name = _validated_property_name(frame_col)
        name_mapping.file_column_name = file_col
        request.column_mapping.frame_column_to_source_name.extend([name_mapping])
      elif isinstance(file_col, int):
        idx_mapping = data_proto.FrameColumnToSourceIdx()
        idx_mapping.frame_column_name = _validated_property_name(frame_col)
        idx_mapping.file_column_idx = file_col
        request.column_mapping.frame_column_to_source_idx.extend([idx_mapping])
      else:
        error_string = 'The data type of "frame_to_file_column_mapping" ' + \
                       'is incorrect. Expects a dictionary with string ' + \
                       'keys and string or integer values.'
        raise TypeError(error_string)
  return request

def _get_processed_row_level_label_columns(row_label_columns,
                                           headerMode = HeaderMode.NONE):
  if row_label_columns is None:
    return None
  elif headerMode == HeaderMode.NONE or headerMode == HeaderMode.IGNORE:
    return [int(col) for col in row_label_columns]
  elif headerMode == HeaderMode.NORMAL or headerMode == HeaderMode.STRICT:
    for col in row_label_columns:
      _assert_isstring(col)
    return row_label_columns

def _row_level_labels_helper(request, row_labels, row_label_columns,
                             source_vertex_row_labels, target_vertex_row_labels,
                             headerMode):
  if row_labels is not None:
    if len(row_labels) == 0:
      row_labels.append("")
    for label in row_labels:
      request.row_labels.labels.extend([label])
  if source_vertex_row_labels is not None:
    for label in source_vertex_row_labels:
      request.row_labels.implicit_source_vertex_labels.extend([label])
  if target_vertex_row_labels is not None:
    for label in target_vertex_row_labels:
      request.row_labels.implicit_target_vertex_labels.extend([label])
  if row_label_columns is not None:
    if headerMode == HeaderMode.NONE or headerMode == HeaderMode.IGNORE:
      for col in row_label_columns:
        request.row_labels.label_column_indices.extend([col])
    elif headerMode == HeaderMode.NORMAL or headerMode == HeaderMode.STRICT:
      for col in row_label_columns:
        request.row_labels.label_column_names.extend([col])
  return request

# -----------------------------------------------------------------------------

class TableFrame(object):
  """
  TableFrame object represent a table held on the xGT server. It can be
  used to retrieve information about it and should not be instantiated directly
  by the user. Methods that return this object: `Connection.get_table_frame()`,
  `Connection.get_table_frames()` and `Connection.create_table_frame()`. A table
  may also be created by a MATCH query and may contain query results.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the frame, including the namespace.
  schema : list of pairs
    List of pairs associating property names with xGT data types.

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> ... run query and store results in Results
  >>> t = conn.get_table_frame('Results')
  >>> print(t.name)

  """
  def __init__(self, conn, name, schema):
    """
    Constructor for TableFrame. Called when TableFrame is created.
    """
    self._conn = conn
    self._name = name
    # Check the schema against the valid property types.
    valid_prop_types = _get_valid_property_types_to_create() + \
                       _get_valid_property_types_for_return_only()

    for col in schema:
      if col[1] not in valid_prop_types:
        raise XgtTypeError('Invalid property type "' + col[1] + '"')

    self._schema = schema

  @property
  def name(self):
    """str: Name of the frame."""
    return self._name

  @property
  def schema(self):
    """list of lists: Gets the property names and types of the frame."""
    return self._schema

  @property
  def connection(self):
    """Connection object: The connection used when constructing the frame."""
    return self._conn

  def load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
           row_labels = None, row_label_columns = None, delimiter = ',',
           frame_to_file_column_mapping = None):
    """
    Loads data from one or more files specified in the list of paths.
    These files may be CSV, Parquet, or compressed CSV.
    Some limitations exist for Parquet and compressed CSV.
    See docs.trovares.com for more details.
    Each path may have its own protocol as described below.

    Parameters
    ----------
    paths : list or string
      A single path or a list of paths to files.

      ==================== =====================================
                      Syntax for one file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to file>'
                           'xgt://<path to file>'
          xGT server:      'xgtd://<path to file>'
          AWS s3:          's3://<path to file>'
          https site:      'https://<path to file>'
          http site:       'http://<path to file>'
          ftps server:     'ftps://<path to file>'
          ftp server:      'ftp://<path to file>'
      ==================== =====================================

    headerMode : str
      Indicates how the file header should be processed:
        - HeaderMode.NONE:
          No header exists.
        - HeaderMode.IGNORE:
          Ignore the first line containing the header.
        - HeaderMode.NORMAL:
          Process the header in non-strict mode. If a schema column is missing,
          a null value is ingested for that schema column. Any file column whose
          name does not correspond to a schema column or a security label column
          is ignored.
        - HeaderMode.STRICT:
          Process the header in strict mode. The name of each header column
          should correspond to a schema column, a security label column, or be
          named IGNORE. Each schema column must appear in the file.

      Optional. Default=HeaderMode.NONE.
      Only applies to CSV files.

    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    row_labels : list
      A list of security labels to attach to each row inserted with the load.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of columns indicating which columns in the CSV file contain
      security labels to attach to the inserted row. If the header mode is
      NONE or IGNORE, this must be a list of integer column indices. If the
      header mode is NORMAL or STRICT, this must be a list of string column
      names. Note: Only one of row_labels and
      row_label_columns must be passed.
      (since version 1.5.0)

    delimiter : str
      Delimiter for CSV data.
      Only applies to CSV files.
      (since version 1.5.1)

    frame_to_file_column_mapping : dictionary
      Maps the frame column names to file columns for the ingest.
      The key of each element is frame's column name. The value is either the
      name of the file column (from the file header) or the file column index.
      If file column names are used, the headerMode must be NORMAL. If only
      file column indices are used, the headerMode can be NORMAL, NONE, or
      IGNORE.
      (Beta since version 1.10)

    Returns
    -------
    Job
      A Job object representing the job that has executed the load.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened or if there are errors inserting any
      lines in the file into the frame.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._load(paths, headerMode, record_history, row_labels,
                      row_label_columns, delimiter = delimiter,
                      frame_to_file_column_mapping = frame_to_file_column_mapping)

  def _load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
            row_labels = None, row_label_columns = None,
            source_vertex_row_labels = None, target_vertex_row_labels = None,
            delimiter = ',', frame_to_file_column_mapping = None, **kwargs):
    if not isinstance(delimiter, str) or len(delimiter) != 1:
      error = ("Delimiter must be a single character string.")
      raise ValueError(error)

    if headerMode is None:
      raise TypeError('the "headerMode" parameter is None')
    if headerMode not in HeaderMode._all:
      raise TypeError('Invalid header mode: "{0}"'.format(str(headerMode)))

    if headerMode == HeaderMode.STRICT and frame_to_file_column_mapping is not None:
      error = ("Passing frame_to_file_column_mapping with HeaderMode.STRICT "
               "is not supported.")
      raise XgtValueError(error)

    _validate_column_mapping_in_ingest(frame_to_file_column_mapping)
    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    _validate_row_level_labels_for_ingest(source_vertex_row_labels)
    _validate_row_level_labels_for_ingest(target_vertex_row_labels)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, headerMode)

    if paths is None:
      raise TypeError('the "paths" parameter is None')
    if not isinstance(paths, (list, tuple, str)):
      raise TypeError('one or more file paths are expected; the data type of the "paths" parameter is "{0}"'.format(type(paths)))
    client_paths, server_paths, url_paths = _group_paths(paths, True)
    if len(client_paths) == 0 and len(server_paths) == 0 and len(url_paths) == 0:
      raise XgtIOError('no valid paths found: ' + str(paths))
    if len(client_paths) > 0:
      return self._insert_from_csv(client_paths, headerMode, row_labels,
                                   row_label_columns, source_vertex_row_labels,
                                   target_vertex_row_labels, delimiter,
                                   frame_to_file_column_mapping)
    if len(server_paths) > 0:
      return self._ingest(server_paths, headerMode, row_labels,
                          row_label_columns, source_vertex_row_labels,
                          target_vertex_row_labels,
                          delimiter, frame_to_file_column_mapping,
                          record_history = record_history, **kwargs)
    if len(url_paths) > 0:
      return self._ingest(url_paths, headerMode, row_labels, row_label_columns,
                          source_vertex_row_labels, target_vertex_row_labels,
                          delimiter, frame_to_file_column_mapping,
                          record_history = record_history, **kwargs)

  def save(self, path, offset = 0, length = None, headers = False,
           record_history = True, include_row_labels = False,
           row_label_column_header = None, preserve_order = False,
           number_of_files = 1):
    """
    Writes the rows from the frame to a file in the location indicated
    by the path parameter.

    Parameters
    ----------
    path : str
      Path to the CSV file.

      ==================== =====================================
                      Syntax for one file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to file>'
                           'xgt://<path to file>'
          xGT server:      'xgtd://<path to file>'
      ==================== =====================================

    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved.
      Optional. Default=None.
    headers : boolean
      Indicates if headers should be added.
      Optional. Default=False.
    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)
    row_label_column_header : str
      The header column name to use for all row labels
      if include_row_labels is true and headers is true.
      (since version 1.5.0)
    preserve_order : boolean
      Indicates if the output should keep the order the
      frame is stored in.
      Optional. Default=False.
      (since version 1.5.1)
    number_of_files : int
      Number of files to save. Only works with the xgtd:// protocol.
      Optional. Default=1.
      (since version 1.10.0)

    Returns
    -------
    Job
      A Job object representing the job that has executed the save.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._save(path, offset, length, headers, record_history,
                      include_row_labels,
                      row_label_column_header, preserve_order, number_of_files)

  def _save(self, path, offset = 0, length = None, headers = False,
            record_history = True, include_row_labels = False,
            row_label_column_header = None, preserve_order = False,
            number_of_files = 1, **kwargs):
    if path is None:
      raise TypeError('the "paths" parameter is None')
    if not isinstance(path, str):
      msg = 'a file path is expected; the data type of the "path" ' \
            'parameter is "{0}"'.format(type(path))
      raise TypeError(msg)

    client_paths, server_paths, url_paths = _group_paths(path, False)
    if (len(client_paths) == 0 and len(server_paths) == 0 and
        len(url_paths) == 0):
      raise XgtIOError('no valid paths found: ' + str(path))
    if len(client_paths) > 0:
      return self._save_to_csv(client_paths[0], offset, length, headers,
                         include_row_labels = include_row_labels,
                         row_label_column_header = row_label_column_header,
                         preserve_order = preserve_order)
    if len(server_paths) > 0:
      return self._egest(server_paths[0], offset, length, headers,
                         record_history = record_history,
                         include_row_labels = include_row_labels,
                         row_label_column_header = row_label_column_header,
                         preserve_order = preserve_order,
                         number_of_files = number_of_files, **kwargs)

  def _create_insert_packet(self, frame_name, data, row_labels,
                            row_label_columns, source_vertex_row_labels,
                            target_vertex_row_labels):
    request = data_proto.UploadDataRequest()
    request.frame_name = self._name.encode('utf-8')
    request.content_type = data_proto.CSV
    request.header_mode = data_proto.NONE
    request.content = data.encode('utf-8')
    request.implicit_vertices = True
    request.delimiter = ','
    request.is_python_insert = True
    request = _row_level_labels_helper(request, row_labels,
                                       row_label_columns,
                                       source_vertex_row_labels,
                                       target_vertex_row_labels,
                                       HeaderMode.NONE)
    return request

  def _insert_packet_generator(self, data, is_pandas,
                               row_labels = None,
                               row_label_columns = None,
                               source_vertex_row_labels = None,
                               target_vertex_row_labels = None):
    nrow = len(data)
    buffer = ''
    schema_size = len(self.schema)
    col_type = [_[1] for _ in self.schema]

    try:
      if is_pandas:
        import pandas
        table = data.values
      else:
        table = data
      for row in table:
        row_str = [str(_) for _ in row]
        for j in range(len(row)):
          col = row[j]
          if isinstance(col, str):
            row_str[j] = '"' + row_str[j] + '"'
          elif col is None:
            row_str[j] = ""
          elif (j < schema_size):
            if (is_pandas and col_type[j] == 'int' and pandas.isna(col)):
              row_str[j] = ""
            elif (col_type[j] == 'list'):
              row_str[j] = '"' + row_str[j] + '"'
        buffer += ",".join(row_str) + '\n'
        if len(buffer) >= MAX_PACKET_SIZE:
          yield self._create_insert_packet(self._name, buffer,
                                           row_labels, row_label_columns,
                                           source_vertex_row_labels,
                                           target_vertex_row_labels)
          buffer = ''
      if len(buffer) > 0:
        yield self._create_insert_packet(self._name, buffer,
                                         row_labels, row_label_columns,
                                         source_vertex_row_labels,
                                         target_vertex_row_labels)
        buffer = ''
    except:
      #Print the error and don't throw since grpc will give an unknown error.
      traceback.print_exc(file=sys.stderr)
      sys.stderr.write("\n")
      pass

  def insert(self, data, row_labels = None,
             row_label_columns = None):
    """
    Inserts data rows. The properties of the new data must match the schema
    in both order and type.

    Parameters
    ----------
    data : list or Pandas dataframe
      Data represented by a list of lists of data items or by a
      Pandas Dataframe.

    row_labels : list
      A list of security labels to attach to each row inserted.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of integer column indices indicating which columns in the input
      data contain security labels to attach to the inserted row. Note: Only
      one of row_labels and row_label_columns must be passed.
      (since version 1.5.0)

    Returns
    -------
    Job
      A Job object representing the job that has executed the insert.

    Raises
    -------
    XgtIOError
      If there are errors in the data being inserted or some data could
      not be inserted into the frame.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    if data is None:
      return
    if len(data) == 0:
      return

    #---- if user passed in a pandas frame
    is_pandas = False
    try:
      import pandas
      if isinstance(data, pandas.DataFrame):
        is_pandas = True
    except:
      pass

    # Exceptions for iterators get eaten by grpc so we check outside
    # the generator function:
    if not is_pandas:
      if not isinstance(data, Iterable):
        raise TypeError('a list of lists or a Pandas DataFrame is expected')
      for i in range(len(data)):
          if not isinstance(data[i], Iterable):
              msg = 'Row #{0} is not a list. A list of lists ' \
                    'or a Pandas DataFrame is expected'.format(i)
              raise TypeError(msg)

    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, HeaderMode.NONE)

    data_iter = self._insert_packet_generator(data, is_pandas,
                                              row_labels,
                                              row_label_columns)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    job_data = job.get_data()
    if job_data is not None and len(job_data) > 0:
      raise XgtIOError(self._create_ingest_error_message(job), job = job)
    return job

  def _process_list_null_values(self, row):
    for i in range(0, len(row)):
      if row[i] == '':
        row[i] = None

      if type(row[i]) is list:
        self._process_list_null_values(row[i])

  def _process_get_data_null_values(self, jsn, num_labels = 0):
    # Empty string currently means null. Return as None.
    for row_idx, row in enumerate(jsn[1:]):
      for idx in range(0, len(row) - num_labels):
        if row[idx] == '':
          jsn[row_idx + 1][idx] = None
        if type(row[idx]) is list:
          self._process_list_null_values(row[idx])
    return jsn

  def get_data(self, offset = 0, length = None, include_row_labels = False):
    """
    Returns frame data starting at a given offset and spanning a given
    length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)

    Returns
    -------
    list of lists

    Raises
    -------
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    # Uses JSON conversion.  Results can get huge, which might result in the
    # client runnning out of memory.
    responses = self._get_data(offset=offset, length=length,
                               include_row_labels = include_row_labels,
                               row_label_column_header = None,
                               preserve_order = True)
    res = ''
    num_labels = 0
    num_labels_set = False
    for response in responses:
        _assert_noerrors(response)
        res += response.content.decode('utf-8')
        # The last message won't have data or the number of labels so set only
        # once.
        if not num_labels_set:
          num_labels = response.num_row_labels
          num_labels_set = True
    try:
      jsn = json.loads('['+res+']')
      jsn = self._process_get_data_null_values(jsn, num_labels)

    except ValueError as ex:
      raise XgtInternalError('Corrupted data packet received: '+ str(ex))
    return jsn[1:]

  def get_data_pandas(self, offset = 0, length = None, include_row_labels = False,
                      row_label_column_header = None):
    """
    Returns a Pandas DataFrame containing frame data starting at a given
    offset and spanning a given length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.
    include_row_labels : bool
      Indicates whether the security labels for each row
      should be egested along with the row.
      (since version 1.5.0)
    row_label_column_header : str
      The header column name to use for all row labels
      if include_row_labels is true and headers is true.
      (since version 1.5.0)

    Returns
    -------
    Pandas DataFrame

    Raises
    -------
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    import pandas

    # Throw an error if trying to return a list for pandas frames.
    for col in self._schema:
      if (_validated_property_type(col[1])) == "LIST":
        raise XgtTypeError('Cannot return list type to pandas frame')
    # Uses JSON conversion.  Results can get huge, which might result in the
    # client runnning out of memory.
    responses = self._get_data(offset = offset, length = length,
                               include_row_labels = include_row_labels,
                               row_label_column_header = row_label_column_header)
    res = ''
    num_labels = 0
    num_labels_set = False
    for response in responses:
        _assert_noerrors(response)
        res += response.content.decode('utf-8')
        # The last message won't have data or the number of labels so set only
        # once.
        if not num_labels_set:
          num_labels = response.num_row_labels
          num_labels_set = True
    try:
      jsn = json.loads('['+res+']')
      jsn = self._process_get_data_null_values(jsn, num_labels)
    except ValueError as ex:
      raise XgtInternalError('Corrupted data packet received: '+ str(ex))
    return pandas.DataFrame(columns=jsn[0:1][0], data=jsn[1:])

  @property
  def num_rows(self):
    """int: Gets the number of rows in the frame."""
    request = graph_proto.GetFrameSizeRequest()
    request.frame_name = self._name
    response = self._conn._call(request, self._conn._graph_svc.GetFrameSize)
    return response.size

  def _get_data(self, offset = 0, length = None, headers = True,
                content_type = data_proto.JSON, include_row_labels = False,
                row_label_column_header = None, preserve_order = False):
    if isinstance(offset, str):
      offset = int(offset)
    if isinstance(length, str):
      length = int(length)
    if isinstance(offset, int):
      if offset < 0:
        raise ValueError('offset is negative')
    if isinstance(length, int):
      if length < 0:
        raise ValueError('length is negative')

    request = data_proto.DownloadDataRequest()
    request.repository_name = self._name
    if offset is not None:
      request.offset.value = offset
    if length is not None:
      request.length.value = length
    request.with_headers = headers
    request.content_type = content_type
    request.preserve_order = preserve_order

    request.row_labels.egest_labels = include_row_labels
    if row_label_column_header is not None:
      request.row_labels.label_header_name = row_label_column_header
    else:
      request.row_labels.label_header_name = "ROWLABEL"

    responses = self._conn._call(request, self._conn._data_svc.DownloadData)
    return responses

  def _create_csv_packet (self, frame_name, data, headerMode, row_labels,
                          row_label_columns, source_vertex_row_labels,
                          target_vertex_row_labels, delimiter, file_path,
                          frame_to_file_column_mapping):
    request = data_proto.UploadDataRequest()
    request.frame_name = frame_name.encode('utf-8')
    request.content = data.encode('utf-8')
    request.content_type = data_proto.CSV
    request.is_python_insert = False
    request.file_path = file_path

    request = _row_level_labels_helper(request, row_labels,
                                                row_label_columns,
                                                source_vertex_row_labels,
                                                target_vertex_row_labels,
                                                headerMode)

    request.delimiter = delimiter;

    if headerMode == HeaderMode.IGNORE:
      request.header_mode = data_proto.IGNORE_HEADERS
    elif headerMode == HeaderMode.NORMAL:
      request.header_mode = data_proto.NORMAL
    elif headerMode == HeaderMode.STRICT:
      request.header_mode = data_proto.STRICT
    else:
      request.header_mode = data_proto.NONE
    request.implicit_vertices = True

    # Set the mapping of frame column to file source.
    if frame_to_file_column_mapping is not None:
      request = _set_column_mapping_in_ingest_request(request, frame_to_file_column_mapping)

    return request

  def _insert_csv_packet_generator(self, paths, headerMode, row_labels,
                                   row_label_columns, source_vertex_row_labels,
                                   target_vertex_row_labels, delimiter,
                                   frame_to_file_column_mapping):
    for fpath in paths:
        try:
          header = ''
          data = ''
          dsize = 0
          with open(fpath, 'rb') as f:
            line = f.readline()
            while line:
              line = line.decode('utf-8')
              lsize = len(line)
              if (dsize + lsize) < MAX_PACKET_SIZE:
                data += line
                dsize += lsize
              else:
                yield self._create_csv_packet(self._name, data, headerMode,
                                              row_labels, row_label_columns,
                                              source_vertex_row_labels,
                                              target_vertex_row_labels,
                                              delimiter, fpath,
                                              frame_to_file_column_mapping)
                data = line
                dsize = len(data)
              line = f.readline()
            yield self._create_csv_packet(self._name, data, headerMode,
                                          row_labels, row_label_columns,
                                          source_vertex_row_labels,
                                          target_vertex_row_labels, delimiter,
                                          fpath, frame_to_file_column_mapping)
        except:
          #Print the error and don't throw since grpc will give an unknown error.
          sys.stderr.write("Error in " + fpath + ": ")
          traceback.print_exc(file=sys.stderr)
          sys.stderr.write("\n")
          pass

  def _insert_from_csv(self, paths, headerMode=HeaderMode.NONE,
                       row_labels = None, row_label_columns = None,
                       source_vertex_row_labels = None,
                       target_vertex_row_labels = None, delimiter = ',',
                       frame_to_file_column_mapping = None):
    data_iter = self._insert_csv_packet_generator(paths, headerMode, row_labels,
                                                  row_label_columns,
                                                  source_vertex_row_labels,
                                                  target_vertex_row_labels,
                                                  delimiter,
                                                  frame_to_file_column_mapping)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    job_data = job.get_data()
    if job_data is not None and len(job_data) > 0:
      raise XgtIOError(self._create_ingest_error_message(job), job = job)
    return job

  def _ingest(self, paths, headerMode = HeaderMode.NONE,
              row_labels = None, row_label_columns = None,
              source_vertex_row_labels = None,
              target_vertex_row_labels = None, delimiter = ',',
              frame_to_file_column_mapping = None, **kwargs):
    request = data_proto.IngestUriRequest()
    request.frame_name = self._name
    request = _row_level_labels_helper(request, row_labels,
                                                row_label_columns,
                                                source_vertex_row_labels,
                                                target_vertex_row_labels,
                                                headerMode)

    if isinstance(paths, (list, tuple)):
      request.content_uri.extend(paths)
    else:
      request.content_uri.extend([paths])

    if headerMode == HeaderMode.IGNORE:
      request.header_mode = data_proto.IGNORE_HEADERS
    elif headerMode == HeaderMode.NORMAL:
      request.header_mode = data_proto.NORMAL
    elif headerMode == HeaderMode.STRICT:
      request.header_mode = data_proto.STRICT
    else:
      request.header_mode = data_proto.NONE

    # Set the mapping of frame column to file source.
    if frame_to_file_column_mapping is not None:
      request = _set_column_mapping_in_ingest_request(request, frame_to_file_column_mapping)

    if (len(self._conn.aws_access_key_id) > 0 and \
        len(self._conn.aws_secret_access_key) > 0):
      request.authorization = self._conn.aws_access_key_id + ':' + \
                              self._conn.aws_secret_access_key

    request.implicit_vertices = True
    request.delimiter = delimiter;

    for k,v in kwargs.items():
      if isinstance(v, bool):
        request.kwargs[k].bool_value = v
      elif isinstance(v, int):
        request.kwargs[k].int_value = v
      elif isinstance(v, float):
        request.kwargs[k].float_value = v
      elif isinstance(v, str):
        request.kwargs[k].string_value = v

    response = self._conn._call(request, self._conn._data_svc.IngestUri)
    job = Job(self._conn, response.job_status)
    job_data = job.get_data()
    if job_data is not None and len(job_data) > 0:
      raise XgtIOError(self._create_ingest_error_message(job), job = job)
    return job

  def _save_to_csv(self, path, offset = 0, length = None, headers = False,
                   include_row_labels = False, row_label_column_header = None,
                   preserve_order = False):
    # This will stream the bytes directly which is > 10X faster than using json.
    responses = self._get_data(offset=offset, length=length, headers=headers,
                               content_type=data_proto.CSV,
                               include_row_labels = include_row_labels,
                               row_label_column_header = row_label_column_header,
                               preserve_order = preserve_order)
    job_status = None
    with open(path, 'wb') as fobject:
      # Each packet can be directly written to the file since we have the
      # raw data. This avoids extra conversion issues and extra memory from
      # json.
      for response in responses:
          _assert_noerrors(response)
          fobject.write(response.content)
          if (response.HasField("job_status")):
            if (job_status is None):
              job_status = response.job_status
            else:
              raise XgtInternalError('Job status already set in packet stream')
    fobject.close()
    return job_status

  def _egest(self, path, offset = 0, length = None, headers = False,
             include_row_labels = False, row_label_column_header = None,
             preserve_order = False, number_of_files = 1, **kwargs):
    if isinstance(offset, str):
      offset = int(offset)
    if isinstance(length, str):
      length = int(length)
    if isinstance(offset, int):
      if offset < 0:
        raise ValueError('offset is negative')
    if isinstance(length, int):
      if length < 0:
        raise ValueError('length is negative')

    request = data_proto.EgestUriRequest()
    request.frame_name = self._name
    request.file_name = path
    request.with_headers = headers
    request.preserve_order = preserve_order
    request.number_of_files = number_of_files
    request.offset.value = offset
    if length is not None:
      request.length.value = length

    request.row_labels.egest_labels = include_row_labels
    if row_label_column_header is not None:
      request.row_labels.label_header_name = row_label_column_header
    else:
      request.row_labels.label_header_name = "ROWLABEL"

    for k,v in kwargs.items():
      if isinstance(v, bool):
        request.kwargs[k].bool_value = v
      elif isinstance(v, int):
        request.kwargs[k].int_value = v
      elif isinstance(v, float):
        request.kwargs[k].float_value = v
      elif isinstance(v, str):
        request.kwargs[k].string_value = v

    response = self._conn._call(request, self._conn._data_svc.EgestUri)
    return Job(self._conn, response.job_status)

  def __str__(self):
    print_frame = "{'name': '" + self.name + "'" + \
                  ", 'schema': " + str(self.schema) + "}"
    return print_frame

  @property
  def row_label_universe(self):
    """list of strings: Gets the universe of row security labels that can be
       attached to rows of this frame. Only labels that are also in the
       authenticated user's label set are returned."""
    request = graph_proto.GetRowLabelUniverseRequest()
    request.frame_name = self.name
    response = self._conn._call(request, self._conn._graph_svc.GetRowLabelUniverse)
    return response.row_labels.label

  def _create_ingest_error_message(self, job):
    num_errors = job.total_rows
    num_rows = self.num_rows

    error_string = 'Errors occurred when inserting data into frame ' + \
                   self._name + '.\n'

    error_string += '  ' + str(num_errors) + ' line'
    if num_errors > 1:
      error_string += 's'

    error_string += ' had insertion errors.\n' + \
                    '  Lines without errors were inserted into the frame.\n' + \
                    '  To see the number of rows in the frame, run "' + \
                    self._name + '.num_rows".\n' + \
                    '  To see the data in the frame, run "' + \
                    self._name + '.get_data()".\n'

    extra_text = ''
    if num_errors > 10:
      extra_text = ' first 10'

    error_string += 'Errors associated with the' + extra_text + ' lines ' + \
                    'that could not be inserted are shown below:'

    # Only print the first 10 messages.
    for error in job.get_data(0, 10):
      filename = os.path.basename(error[1])
      lineNumber = error[2]
      if lineNumber == -1:
        error_string += '\n '+ str(error[0])
      else:
        error_string += '\n  File: ' + filename + ': Line: ' + str(lineNumber) + \
                        ': ' + str(error[0])

    return error_string

# -----------------------------------------------------------------------------

class VertexFrame(TableFrame):
  """
  VertexFrame object represents a collection of vertices held on the xGT
  server; it can be used to retrieve information about them and should not be
  instantiated directly by the user. Methods that return this object:
  `Connection.get_vertex_frame()`, `Connection.get_vertex_frames()` and
  `Connection.create_vertex_frame()`.

  Each vertex in a VertexFrame shares the same properties,
  described in `VertexFrame.schema`. Each vertex in a VertexFrame
  is uniquely identified by the property listed in `VertexFrame.key`.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the vertex frame, including the namespace.
  schema : list of pairs
    List of pairs associating property names with xGT data types.
    Each vertex in the VertexFrame will have these properties.
  key : str
    The property name used to uniquely identify vertices in the graph.
    This is the name of one of the properties from the schema and
    must be unique for each vertex in the frame.

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> v1 = conn.create_vertex_frame(
  ...        name = 'People',
  ...        schema = [['id', xgt.INT],
  ...                  ['name', xgt.TEXT]],
  ...        key = 'id')
  >>> v2 = conn.get_vertex_frame('Companies') # An existing vertex frame
  >>> print(v1.name, v2.name)

  """
  def __init__(self, conn, name, schema, key):
    """
    Constructor for VertexFrame. Called when VertexFrame is created.
    """
    super(VertexFrame, self).__init__(conn, name, schema)
    self._key = key

  @property
  def key(self):
    """str: Gets the property name that uniquely identifies vertices of this type."""
    return self._key

  @property
  def num_vertices(self):
    """int: Gets the number of vertices in the VertexFrame."""
    return self.num_rows

  def __str__(self):
    print_frame = ("{'name': '" + self.name + "'" +
                   ", 'schema': " + str(self.schema) +
                   ", 'key': '" + self.key + "'}")
    return print_frame

# -----------------------------------------------------------------------------

class EdgeFrame(TableFrame):
  """
  EdgeFrame object represents a collection of edges held on the xGT server;
  it can be used to retrieve information about them and should not be
  instantiated directly by the user. Methods that return this object:
  `Connection.get_edge_frame()`, `Connection.get_edge_frames()` and
  `Connection.create_edge_frame()`. Each edge in an EdgeFrame shares the same
  properties, described in `EdgeFrame.schema`.

  The source vertex of each edge in an EdgeFrame must belong to the same
  VertexFrame. This name of this VertexFrame is given by `EdgeFrame.source_name`.
  The targe vertex of each edge in an EdgeFrame must belong to the same
  VertexFrame. This name of this VertexFrame is given by `EdgeFrame.target_name`.

  For each edge in the EdgeFrame, its source vertex is identified by
  the edge property name given by `EdgeFrame.source_key`, which is
  one of the properties listed in the schema. The edge target vertex
  is identified by the property name given by `EdgeFrame.target_key`.

  Parameters
  ----------
  conn : Connection
    An open connection to an xGT server.
  name : str
    Fully qualified name of the edge frame, including the namespace.
  schema : list of pairs
    List of pairs associating property names with xGT data types.
    Each edge in the EdgeFrame will have these properties.
  source : str or VertexFrame
    The name of a VertexFrame or a VertexFrame object.
    The source vertex of each edge in this EdgeFrame will belong
    to this VertexFrame.
  target : str or VertexFrame
    The name of a VertexFrame or a VertexFrame object.
    The target vertex of each edge in this EdgeFrame will belong
    to this VertexFrame.
  source_key : str
    The edge property name that identifies the source vertex of an edge.
    This is one of the properties from the schema.
  target_key : str
    The edge property name that identifies the target vertex of an edge.
    This is one of the properties from the schema.

  Examples
  --------
  >>> import xgt
  >>> conn = xgt.Connection()
  >>> e1 = conn.create_edge_frame(
  ...        name = 'WorksFor',
  ...        schema = [['srcid', xgt.INT],
  ...                  ['role', xgt.TEXT],
  ...                  ['trgid', xgt.INT]],
  ...        source = 'People',
  ...        target = 'Companies',
  ...        source_key = 'srcid',
  ...        target_key = 'trgid')
  >>> e2 = conn.get_edge_frame('RelatedTo') # An existing edge frame
  >>> print(e1.name, e2.name)

  """
  def __init__(self, conn, name, schema, source, target, source_key, target_key):
    """
    Constructor for EdgeFrame. Called when EdgeFrame is created.
    """
    super(EdgeFrame, self).__init__(conn, name, schema)
    self._source_name = source
    self._target_name = target
    self._source_key = source_key
    self._target_key = target_key

  @property
  def source_name(self):
    """str: Gets the name of the source vertex frame."""
    return self._source_name

  @property
  def target_name(self):
    """str: Gets the name of the target vertex frame."""
    return self._target_name

  @property
  def source_key(self):
    """str: The edge property name that identifies the source vertex of an edge."""
    return self._source_key

  @property
  def target_key(self):
    """str: The edge property name that identifies the target vertex of an edge."""
    return self._target_key

  @property
  def num_edges(self):
    """int: Gets the number of edges in the EdgeFrame."""
    return self.num_rows

  def __str__(self):
    print_frame = ("{'name': '" + self.name + "'" +
                   ", 'source': '" + self.source_name + "'" +
                   ", 'target': '" + self.target_name + "'" +
                   ", 'schema': " + str(self.schema) +
                   ", 'source_key': '" + self.source_key + "'" +
                   ", 'target_key': '" + self.target_key + "'}")
    return print_frame

  def load(self, paths, headerMode = HeaderMode.NONE, record_history = True,
           row_labels = None, row_label_columns = None,
           source_vertex_row_labels = None, target_vertex_row_labels = None,
           delimiter = ',', frame_to_file_column_mapping = None):
    """
    Loads data from one or more files specified in the list of paths.
    These files may be CSV, Parquet, or compressed CSV.
    Some limitations exist for Parquet and compressed CSV.
    See docs.trovares.com for more details.
    Each path may have its own protocol as described below.

    Parameters
    ----------
    paths : list or string
      A single path or a list of paths to files.

      ==================== =====================================
                      Syntax for one file path
      ----------------------------------------------------------
          Resource type                 Path syntax
      ==================== =====================================
          local to Python: '<path to file>'
                           'xgt://<path to file>'
          xGT server:      'xgtd://<path to file>'
          AWS s3:          's3://<path to file>'
          https site:      'https://<path to file>'
          http site:       'http://<path to file>'
          ftps server:     'ftps://<path to file>'
          ftp server:      'ftp://<path to file>'
      ==================== =====================================

    headerMode : str
      Indicates if the CSV files contain headers:
        - HeaderMode.NONE
        - HeaderMode.IGNORE
        - HeaderMode.NORMAL
        - HeaderMode.STRICT

      Optional. Default=HeaderMode.NONE.
      Only applies to CSV files.

    record_history : bool
      If true, records the history of the job.
      (since version 1.4.0)

    row_labels : list
      A list of security labels to attach to each row inserted with the load.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of columns indicating which columns in the CSV file contain
      security labels to attach to the inserted row. If the header mode is
      NONE or IGNORE, this must be a list of integer column indices. If the
      header mode is NORMAL or STRICT, this must be a list of string column
      names. Note: Only one of row_labels and
      row_label_columns must be passed.
      (since version 1.5.0)

    source_vertex_row_labels : list
      A list of security labels to attach to each source vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    target_vertex_row_labels : list
      A list of security labels to attach to each target vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    delimiter : str
      Delimiter for CSV data.
      Only applies to CSV files.
      (since version 1.5.1)

    frame_to_file_column_mapping : dictionary
      Maps the frame column names to file columns for the ingest.
      The key of each element is frame's column name. The value is either the
      name of the file column (from the file header) or the file column index.
      If file column names are used, the headerMode must be NORMAL. If only
      file column indices are used, the headerMode can be NORMAL, NONE, or
      IGNORE.
      (Beta since version 1.10)

    Returns
    -------
    Job
      A Job object representing the job that has executed the load.

    Raises
    -------
    XgtIOError
      If a file specified cannot be opened or if there are errors inserting any
      lines in the file into the frame.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    return self._load(paths, headerMode, record_history, row_labels,
                      row_label_columns, source_vertex_row_labels,
                      target_vertex_row_labels, delimiter,
                      frame_to_file_column_mapping = frame_to_file_column_mapping)

  def insert(self, data, row_labels = None,
             row_label_columns = None,
             source_vertex_row_labels = None,
             target_vertex_row_labels = None):
    """
    Inserts data rows. The properties of the new data must match the schema
    in both order and type.

    Parameters
    ----------
    data : list or Pandas dataframe
      Data represented by a list of lists of data items or by a
      Pandas Dataframe.

    row_labels : list
      A list of security labels to attach to each row inserted.
      Each label must have been passed in to the row_label_universe
      parameter when creating the frame. Note: Only one of row_labels
      and row_label_columns must be passed.
      (since version 1.5.0)

    row_label_columns: list
      A list of integer column indices indicating which columns in the input
      data contain security labels to attach to the inserted row. Note: Only
      one of row_labels and row_label_columns must be passed.
      (since version 1.5.0)

    source_vertex_row_labels : list
      A list of security labels to attach to each source vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    target_vertex_row_labels : list
      A list of security labels to attach to each target vertex that is
      implicitly inserted. Each label must have been passed in to the
      row_label_universe parameter when creating the frame.
      (since version 1.5.0)

    Returns
    -------
    Job
      A Job object representing the job that has executed the insert.

    Raises
    -------
    XgtIOError
      If there are errors in the data being inserted or some data could
      not be inserted into the frame.
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.

    """
    if data is None:
      return
    if len(data) == 0:
      return

    #---- if user passed in a pandas frame
    is_pandas = False
    try:
      import pandas
      if isinstance(data, pandas.DataFrame):
        is_pandas = True
    except:
      pass

    # Exceptions for iterators get eaten by grpc so we check outside
    # the generator function:
    if not is_pandas:
      if not isinstance(data, Iterable):
        raise TypeError('a list of lists or a Pandas DataFrame is expected')
      for i in range(len(data)):
          if not isinstance(data[i], Iterable):
              msg = 'Row #{0} is not a list. A list of lists ' \
                    'or a Pandas DataFrame is expected'.format(i)
              raise TypeError(msg)

    _validate_row_level_labels_for_ingest(row_labels,
                                          row_label_columns)
    _validate_row_level_labels_for_ingest(source_vertex_row_labels)
    _validate_row_level_labels_for_ingest(target_vertex_row_labels)
    row_label_columns = _get_processed_row_level_label_columns(
        row_label_columns, HeaderMode.NONE)

    data_iter = self._insert_packet_generator(data, is_pandas,
                                              row_labels,
                                              row_label_columns,
                                              source_vertex_row_labels,
                                              target_vertex_row_labels)
    response = self._conn._call(data_iter, self._conn._data_svc.UploadData)
    job = Job(self._conn, response.job_status)
    job_data = job.get_data()
    if job_data is not None and len(job_data) > 0:
      raise XgtIOError(self._create_ingest_error_message(job), job = job)
    return job

# -----------------------------------------------------------------------------

def _group_paths(paths, for_ingest):
  client_prefix = 'xgt://'
  server_prefix = 'xgtd://'
  url_prefixes = ['s3://', 'https://', 'http://', 'ftps://', 'ftp://']
  client_paths = []
  server_paths = []
  url_paths = []
  if isinstance(paths, str):
    paths = [paths]
  elif not isinstance(paths, (list, tuple)):
    return client_paths, server_paths, url_paths
  for one_path in paths:
    if one_path == "":
      raise ValueError('one or more "paths" are empty')
    if one_path.startswith(client_prefix):
      _validate_client_path(one_path)
      client_paths.append(one_path[len(client_prefix):])
    elif one_path.startswith(server_prefix):
      server_paths.append(one_path[len(server_prefix):])
    elif any(map(lambda p: one_path.startswith(p), url_prefixes)):
      for url_prefix in url_prefixes:
        if for_ingest == False:
          msg = 'Url paths are invalid for data writing ' \
                '"{0}".'.format(one_path)
          raise XgtNotImplemented(msg)
        if one_path.startswith(url_prefix):
          url_paths.append(one_path)
          break
    else:
      if '://' in one_path:
        msg = 'Unsupported url protocol in path "{0}".'.format(one_path)
        raise XgtNotImplemented(msg)
      _validate_client_path(one_path)
      client_paths.append(one_path)
  return client_paths, server_paths, url_paths

def _validate_client_path(one_path):
  if one_path.endswith('.gz') or one_path.endswith('.bz2'):
    msg = 'Loading/Saving compressed files from a local filesystem is ' \
          'not supported: {0}'.format(one_path)
    raise XgtNotImplemented(msg)
  elif one_path.endswith('.parquet'):
    msg = 'Loading/Saving parquet files from a local filesystem is ' \
          'not supported: {0}'.format(one_path)
    raise XgtNotImplemented(msg)
