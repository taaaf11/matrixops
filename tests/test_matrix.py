import unittest

from matop.exceptions import InconsistentOrder
from matop.matrix import BracketsType, Matrix, MatrixOrder  # type: ignore
from matop.row import Row  # type: ignore


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix1 = Matrix(
            Row(1, 2, 3),
            Row(7, 8, 9),
            Row(3, 5, 7),
        )
        
    def test_order_property(self):
        self.assertEqual(self.matrix1.order, MatrixOrder(rows=3, columns=3))
    
    def test_rows_property(self):
        self.assertEqual(
            self.matrix1.rows,
            [
                Row(1, 2, 3),
                Row(7, 8, 9),
                Row(3, 5, 7),
            ]
        )
    
    def test_columns_property(self):
        self.assertEqual(
            self.matrix1.columns,
            [
                [1, 7, 3],
                [2, 8, 5],
                [3, 9, 7],
            ]
        )
        
    def test_add_rows_without_scalar(self):
        self.matrix1.add_rows(0, 1)
        self.assertEqual(
            self.matrix1.rows[0].nums,
            [8, 10, 12]
        )
        
    def test_add_rows_with_scalar(self):
        self.matrix1.add_rows(0, 1, 5)
        self.assertEqual(
            self.matrix1.rows[0].nums,
            [36, 42, 48]
        )
        
    def test_interchange_rows(self):
        row_0_before = self.matrix1.rows[0]
        row_1_before = self.matrix1.rows[1]
        
        self.matrix1.interchange_rows(0, 1)
        
        row_0_after = self.matrix1.rows[0]
        row_1_after = self.matrix1.rows[1]
        
        self.assertTrue(
            row_0_before == row_1_after and
            row_1_before == row_0_after
        )
    
    def test_scalar_multiply(self):
        self.matrix1.scalar_multiply(2)
        self.assertEqual(
            self.matrix1,
            Matrix(
                Row(2, 4, 6),
                Row(14, 16, 18),
                Row(6, 10, 14),
            )
        )
    
    def test_scalar_multiply_row(self):
        self.matrix1.scalar_multiply_row(0, 2)
        self.assertEqual(
            self.matrix1,
            Matrix(
                Row(2, 4, 6),
                Row(7, 8, 9),
                Row(3, 5, 7),
            )
        )
    
    def test_dot_multiply(self):
        # matrix adopted from: https://www.mathsisfun.com/algebra/matrix-multiplying.html
        
        mat1 = Matrix(
            Row(1, 2, 3),
            Row(4, 5, 6)
        )
        mat2 = Matrix(
            Row(7, 8),
            Row(9, 10),
            Row(11, 12),
        )
        
        mat1.dot_multiply(mat2)
        
        self.assertEqual(
            mat1,
            Matrix(
                Row(58, 64),
                Row(139, 154),
            )
        )
        
        mat3 = Matrix(
            Row(1),
            Row(3)
        )
        mat4 = Matrix(
            Row(2, 1),
            Row(3, 5)
        )
        
        self.assertRaises(InconsistentOrder, mat3.dot_multiply, mat4)
        
    # test for private method: Matrix._add_row
    def test__add_row(self):
        self.matrix1._add_row(
            Row(12, 13, 14)
        )
        self.assertEqual(
            self.matrix1.rows,
            [
                Row(1, 2, 3),
                Row(7, 8, 9),
                Row(3, 5, 7),
                Row(12, 13, 14)
            ]
        )
    
    # should not be considered complete
    @unittest.skip("The test code is incomplete")
    def test_as_latex(self):
        rows_latex: str = "\n".join([row.as_latex() for row in self.matrix1.rows])
        
        def add_bracket_type(brackets: BracketsType):
            return f"\\begin{{{brackets.value}matrix}}\n" + \
                    rows_latex + \
                    f"\n\\end{{{brackets.value}matrix}}"
            
        for bracket_type in BracketsType:
            add_bracket_type(bracket_type)
        # latex = self.matrix1.as_latex()