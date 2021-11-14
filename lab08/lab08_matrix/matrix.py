class Matrix:
  def __init__(self, m, n):
    """
    Initialises a matrix of dimensions m by n.
    """
    self.matrix = [[0 for j in range(n)] for i in range(m)]
    self.row = m
    self.column = n
    self.shape = m * n

  def __getitem__(self, key):
    """
    Returns the (i,j)th entry of the matrix, where key is the tuple (i,j).
    i or j may be Ellipsis (...) indicating that the entire i-th row
    or j-th column should be selected. In this case, this method returns a
    list of the i-th row or j-th column.
    Used as follows: x = matrix[0,0] || x = matrix[...,1] || x = matrix[0,...]
     * raises IndexError if (i,j) is out of bounds
     * raises TypeError if (i,j) are both Ellipsis
    """
    if key[0] != ...:
      if (key[0] >= self.row) or (key[0] < 0):
        raise IndexError
    if key[1] != ...:
      if (key[1] >= self.column) or (key[1] < 0):
        print(key[1])
        raise IndexError
    if key == (...,...):
      raise TypeError
      
    if key[0] == ...:
      result = []
      for row in range(self.row):
        result.append(self.matrix[row][key[1]])
      return result
    elif key[1] == ...:
      result = []
      for col in range(self.column):
        result.append(self.matrix[key[0]][col])
      return result
    else:
      return self.matrix[key[0]][key[1]]


  def __setitem__(self, key, data):
    """
    Sets the (i,j)th entry of the matrix, where key is the tuple (i,j)
    and data is the number being added.
    One of i or j may be Ellipsis (...) indicating that the entire i-th row
    or j-th column should be replaced. In this case, data should be a list
    or a tuple of integers of the same dimensions as the equivalent matrix
    row or column. This method then replaces the i-th row or j-th column
    with the contents of the list or tuple
    Used as follows: matrix[0,0] = 1 || matrix[...,1] = [4,5,6] || matrix[0,...] = (1,2)
     * raises IndexError if (i,j) is out of bounds
     * raises TypeError if (i,j) are both Ellipsis
     * if i and j are integral, raises TypeError if data is not an integer
     * if i or j are Ellipsis, raises TypeError if data is not a list or tuple of integers
     * if i or j are Ellipsis, raises ValueError if data is not the correct size
    """
    if key == (...,...):
      raise TypeError
    if (key[0] != ...) & (key[1] != ...) & (type(data) != int):
      raise TypeError
    if (key[0] == ...) | (key[1] == ...):
      if (type(data) != list) and (type(data) != tuple):
        raise TypeError
    if key[0] == ...:
      if len(data) != self.row:
        raise ValueError
    if key[1] == ...:
      if len(data) != self.column:
        raise ValueError
    if type(data) != int:
      for i in data:
        if type(i) != int:
          raise TypeError
    if key[0] != ...:
      if (key[0] >= self.row) or (key[0] < 0):
        raise IndexError
    if key[1] != ...:
      if (key[1] >= self.column) or (key[1] < 0):
        raise IndexError

    if key[0] == ...:
      for row in range(self.row):
        self.matrix[row][key[1]] = data[row]
    elif key[1] == ...:
      for col in range(self.column):
        self.matrix[key[0]][col] = data[col]
    else:
      self.matrix[key[0]][key[1]] = data


  def __iadd__(self, other):
    """
    Adds other to this matrix, modifying this matrix object and returning self
    Used as follows: m1 += m2 ||  m1 += 3
     * raises TypeError if other is not a Matrix object or an integer
     * raises ValueError if adding another Matrix and it does not have the same dimensions as this matrix
    """
    if (type(self) != type(other)) and (not isinstance(other, int)):
      raise TypeError
    if other.shape != self.shape:
      raise ValueError
    for r in range(self.row):
      for c in range(self.column):
        self[r, c] = self[r, c] + other[r, c]
    return self


  def __add__(self, other):
    """
    Adds this matrix to other, returning a new matrix object.
    This method should not modify the current matrix or other.
    Used as follows: m1 + m2 ||  m1 + 3
     * raises TypeError if other is not a Matrix object or an integer
     * raises ValueError if adding another Matrix and it does not have the same dimensions as this matrix
    """
    if (type(self) != type(other)) and (not isinstance(other, int)):
      raise TypeError
    if (type(self) == type(other)) and (other.shape != self.shape):
      raise ValueError
    New = Matrix(self.row, self.column)
    if isinstance(other, int) or isinstance(other,float):
      for r in range(self.row):
        for c in range(self.column):
          New[r, c] = self[r, c] + other
    else:
      for r in range(self.row):
        for c in range(self.column):
          New[r, c] = self[r, c] + other[r, c]
    return New

  def __mul__(self, other):
    """Multiplies self with another Matrix or integer, returning a new Matrix.

    This method should not modify the current matrix or other.
    Used as follows: m1*m2 => m1.__mul__(m2) (matrix multiplication, not point-wise)
    or: m1*3 => m1.__mul__(3)
    * raises TypeError if the other is not a Matrix object or an integer
    * raises ValueError if the other Matrix has incorrect dimensions
    """
    if (type(self) != type(other)) and (not isinstance(other, int)):
      raise TypeError
    if isinstance(other, int) or isinstance(other,float):
      M = Matrix(self.row, self.column)
      for r in range(self.row):
        for c in range(self.column):
          M[r, c] = self[r, c] * other
    else:
      if other.row != self.column:
        raise ValueError
      M = Matrix(self.row, other.column)
      for r in range(self.row):
        for c in range(other.column):
          sum = 0
          for k in range(self.column):
            sum += self[r, k] * other[k, c]
          M[r, c] = sum
    return M

  def get_dimensions(self):
      return self.shape

  def __str__(self):
    """
    Returns a string representation of this matrix in the form:
      a b c
      d e f
      g h i
    Used as follows: s = str(m1)
    """
    s = ''
    for r in range(self.row):
      s += ('\n' + str(self[r,0]) )
      for c in range(1,self.column):    
        s += ' '
        s += str(self[r,c])  
    return s[1:]

  def transpose(self):
    """
    Returns a new matrix that is the transpose of this Matrix object
    This method should not modify the current matrix.
    """
    M = Matrix(self.column, self.row)
    for r in range(self.column):
      for c in range(self.row):
        M[r, c] = self[c, r]
    return M

  def copy(self):
    """
    Returns a new Matrix that is an exact and independent copy of this one
    This method should not modify the current matrix.
    """
    M = Matrix(self.row, self.column)
    for c in range(self.column):
      for r in range(self.row):
        M[r, c] = self[r, c]
    return M
