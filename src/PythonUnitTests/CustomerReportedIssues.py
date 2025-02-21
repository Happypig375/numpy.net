import unittest
import numpy as np
from nptest import nptest

class Test_CustomerReportedIssues(unittest.TestCase):

    
    def test_tensordot_asiamartini_bugreport(self):  
        
        alpha_0 = np.array([ 1.0, 1.0, 1.0 ]);
        temp = np.array([ [ [ 0.0, 0.0, 0.0, 0.0 ], [ 0.0, 0.0, 0.0, 0.0 ], [ 0.0, 0.0, 0.0, 0.0 ], [ 0.0, 0.0, 0.0, 0.0 ] ], 
                         [ [ -18.0, 12.0, 12.0, -10.0 ], [ 12.0, 10.0, 18.0, 12.0 ], [ 12.0, 18.0, -10.0, -12.0 ], [ -10.0, 12.0, -12.0, 18.0 ] ], 
                         [ [ -3.5, 21.5, 5.5, -2.5 ], [ 21.5, 2.5, 5.5, 3.5 ], [ 5.5, 5.5, -20.5, -5.5 ], [ -2.5, 3.5, -5.5, 21.5 ] ] ])


        matrix = nptest.tensordot(alpha_0, temp, axes=([0],[0]))
        print(matrix)
        return


    def test_matmul_asiamartini_bugreport(self):

        rq = np.array([0.5,0.5,0.5,0.5]);
        am = np.array([[-21.5, 33.5, 17.5, -12.5], [33.5, 12.5, 23.5, 15.5], [17.5,23.5,-30.5,-17.5], [-12.5, 15.5, -17.5, 39.5] ]);
   
        temp1 = np.matmul(rq.T, am);
        print(temp1)


    def test_goodgood_test(self):

        img = np.fromfile('test.dat',sep=',')
        img = img.reshape(10,10,3)
        print(img)
        output = img.copy()

        valid = np.all(img == [ 255, 255, 240], axis = -1)
        rs, cs = valid.nonzero()
        output[rs, cs, :] = [255, 255, 255]
        print(output)

    def test_goodgood_test_2(self):

        imgnd = np.arange(1,301).reshape(10,10,3)
        R = imgnd[:, :, 0]
        G = imgnd[:, :, 1]
        B = imgnd[:, :, 2]
        print(R.shape,G.shape,B.shape)
        print(R)
        print(G)
        print(B)

    def test_append_msever_1(self):

        arr = np.array([[1,2,3],[4,5,6]])
        row = np.array([7,8,9])
        arr = np.append(arr,[row],axis= 0)
        print(arr)

    def test_tuple_msever_2(self):

        a = np.array((1,2,3))
        print(a)
        b = np.array((2,3,4))
        print(b)
          
        c = np.column_stack((a,b))
        print(c)

    def test_slice_msever_1(self):

        a=np.array([[1,3,0],[0,0,5]])

        col1 = a[:,0] 
        col2 = a[:,1]
        col3 = a[:,2]

        print(col1)
        print(col2)
        print(col3)

    def test_hsplit_msever_1(self):

        a=np.array([[1,3,0],[0,0,5]])

        row, col = np.hsplit(np.argwhere(a),2)

        print(row)
        print(col)


    def test_take_msever_1(self):

        testVector = np.array([ 1.011163, 1.01644999999999, 1.01220500000001, 1.01843699999999, 1.00985100000001, 1.018964, 1.005825, 1.016707, 8.11556899999999, 1.010744, 1.01700600000001, 1.01323099999999, 1.010389, 1.015216, 1.015418, 1.01704600000001, 1.01191, 1.01164299999999, 1.01062400000001, 1.014199, 1.012952, 1.017645, 1.01591999999999, 1.018655, 1.00942400000001, 1.012852, 1.010543, 1.02000700000001, 1.008196, 1.01396099999999 ]);
        testVector2 = testVector.reshape(15, 2);
        testDataMode1 = np.array([ 1, 2, 2, 3, 4, 7, 9 ]);

        print(testVector2);
        print(testDataMode1);

        print("np.take()");
        testTake = np.take(testVector2, testDataMode1.astype(np.intp), axis=0);
        print(testTake);

        testVector3 = np.arange(0.0, 30000.0, 0.5, dtype= np.float64);
        testVector4 = testVector3.reshape(30000, 2);
        testIndex = np.arange(0, 30000, 100, dtype= np.intp);

        print("test BIG np.take()");
        # testBigTake = np.take(testVector4, testIndex, axis: 0);
        testBigTake = np.zeros((300, 2), dtype= np.float64);
        testBigTake = np.take(testVector4, testIndex, axis= 0);
        print(testIndex);
        print(testBigTake);
        print(np.diff(testIndex));
        print(np.diff(testBigTake, axis= 0));
   
    def test_HadrianTang_1(self):

       x = np.array_equal([], [])
       print(x)

       x = np.array_equiv([], [])
       print(x)



    def test_HadrianTang_2(self):

       x = np.all([])
       print(x)
       x = np.any([])
       print(x)

    def test_HadrianTang_3(self):

       x = np.sum([])
       print(x)
       x = np.prod([])
       print(x)

    def test_HadrianTang_4(self):

       x = np.logical_and([],[])
       print(x)
       x = np.logical_or([], [])
       print(x)


    def test_HadrianTang_5(self):

        x = np.not_equal([], [])
        print(x)

    def test_HadrianTang_6(self):

        x = np.concatenate([[], []])
        print(x)

        x = np.stack(([],[]))
        print(x)

    def test_HadrianTang_7(self):

        x = np.array([])
        x = x * 5
        print(x)
        x = x + 5
        print(x)


    def test_HadrianTang_8(self):

        x = np.array([["0","1"],["0","0"]]).astype(np.float);
     
        print(x)
    

    def test_HadrianTang_9(self):

        x = np.delete(np.array([["0", "1", "@"],["1", "0", "@"]]), 1, 1);
     
        print(x)
    
    def test_HadrianTang_10(self):

        x = np.logical_and(np.array([0, 1, 2]), np.array([1, 0, 2]))
        print(x)

        x = np.logical_or(np.array([1, 0, 2]), np.array([1, 0, 0]))
        print(x)

    def test_HadrianTang_11(self):

        a = np.argmax(np.arange(5))
        print(a)
        b = np.arange(7)[a]
        print(b)

    def test_HadrianTang_12(self):

        print(np.array(4).shape)
        print(np.arange(7)[np.array(4)])

    def test_HadrianTang_13(self):

       objecta = 9.234
       objectb = 33

       a = np.min(objecta)
       b = np.max(objectb)
       #c =  ndarray.this[objectb]

       print(a)
       print(b)
       #print(c)

    def test_HadrianTang_14(self):

        a = np.array(2);
        b = np.array(2, np.int32);

        print(a.ndim)
        print(b.ndim)

 
      
if __name__ == '__main__':
    unittest.main()
