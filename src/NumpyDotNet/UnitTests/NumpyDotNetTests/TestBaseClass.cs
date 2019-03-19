﻿/*
 * BSD 3-Clause License
 *
 * Copyright (c) 2018-2019
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using NumpyDotNet;

namespace NumpyDotNetTests
{
    public class TestBaseClass
    {
        [ClassInitialize]
        public static void CommonInit(TestContext t)
        {
          //  numpy.InitializeNumpyLibrary();
        }

        [TestInitialize]
        public void FunctionInit()
        {
            numpy.NumpyErrors.Clear();
        }

        protected void print(object obj)
        {
            if (obj == null)
            {
                Console.WriteLine("<null>");
                return;
            }
            if (obj is Array)
            {
                foreach (var o in (Array)obj)
                {
                    Console.WriteLine(o.ToString());
                }
            }
            else
            {
                Console.WriteLine(obj.ToString());
            }
        }
        protected void print(string label, object obj)
        {
            Console.WriteLine(label + obj.ToString());
        }
        protected void print<T>(string label, T[] array)
        {
            Console.WriteLine(label + ArrayToString(array));
        }

        protected string ArrayToString<T>(T[] array)
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("[");

            foreach (T t in array)
            {
                sb.Append(t.ToString());
                sb.Append(",");
            }

            sb.Append("]");

            return sb.ToString();
        }


        #region Asserts


        internal void AssertStrides(ndarray a, int s0)
        {
            Assert.AreEqual(a.strides.Length, 1);
            Assert.AreEqual(a.strides[0], s0);
        }
        internal void AssertStrides(ndarray a, int s0, int s1)
        {
            Assert.AreEqual(a.strides.Length, 2);
            Assert.AreEqual(a.strides[0], s0);
            Assert.AreEqual(a.strides[1], s1);
        }
        internal void AssertStrides(ndarray a, int s0, int s1, int s2)
        {
            Assert.AreEqual(a.strides.Length, 3);
            Assert.AreEqual(a.strides[0], s0);
            Assert.AreEqual(a.strides[1], s1);
            Assert.AreEqual(a.strides[2], s2);
        }
        internal void AssertStrides(ndarray a, int s0, int s1, int s2, int s3)
        {
            Assert.AreEqual(a.strides.Length, 4);
            Assert.AreEqual(a.strides[0], s0);
            Assert.AreEqual(a.strides[1], s1);
            Assert.AreEqual(a.strides[2], s2);
            Assert.AreEqual(a.strides[3], s3);
        }

        internal void AssertShape(ndarray a, int s0)
        {
            AssertShape(a.shape, s0);
        }
        internal void AssertShape(shape s, int s0)
        {
            Assert.AreEqual(s.iDims.Length, 1);
            Assert.AreEqual(s.iDims[0], s0);
        }

        internal void AssertShape(ndarray a, int s0, int s1)
        {
            AssertShape(a.shape, s0, s1);
        }
        internal void AssertShape(shape s, int s0, int s1)
        {
            Assert.AreEqual(s.iDims.Length, 2);
            Assert.AreEqual(s.iDims[0], s0);
            Assert.AreEqual(s.iDims[1], s1);
        }

        internal void AssertShape(ndarray a, int s0, int s1, int s2)
        {
            AssertShape(a.shape, s0, s1, s2);
        }
        internal void AssertShape(shape s, int s0, int s1, int s2)
        {
            Assert.AreEqual(s.iDims.Length, 3);
            Assert.AreEqual(s.iDims[0], s0);
            Assert.AreEqual(s.iDims[1], s1);
            Assert.AreEqual(s.iDims[2], s2);
        }

        internal void AssertShape(ndarray a, int s0, int s1, int s2, int s3)
        {
            AssertShape(a.shape, s0, s1, s2, s3);
        }
        internal void AssertShape(shape s, int s0, int s1, int s2, int s3)
        {
            Assert.AreEqual(s.iDims.Length, 4);
            Assert.AreEqual(s.iDims[0], s0);
            Assert.AreEqual(s.iDims[1], s1);
            Assert.AreEqual(s.iDims[2], s2);
            Assert.AreEqual(s.iDims[3], s3);
        }
        internal void AssertShape(shape s, int s0, int s1, int s2, int s3, int s4, int s5)
        {
            Assert.AreEqual(s.iDims.Length, 6);
            Assert.AreEqual(s.iDims[0], s0);
            Assert.AreEqual(s.iDims[1], s1);
            Assert.AreEqual(s.iDims[2], s2);
            Assert.AreEqual(s.iDims[3], s3);
            Assert.AreEqual(s.iDims[4], s4);
            Assert.AreEqual(s.iDims[5], s5);
        }

        internal void AssertArrayNAN<T>(ndarray arrayData, T[] expectedData)
        {
            int length = expectedData.Length;
            AssertShape(arrayData, length);

            for (int i = 0; i < length; i++)
            {
                Assert.AreEqual(expectedData[i], arrayData[i]);
            }
        }

        internal void AssertArray<T>(ndarray arrayData, T[] expectedData)
        {
            int length = expectedData.Length;
            AssertShape(arrayData, length);

            for (int i = 0; i < length; i++)
            {
                double E1 = Convert.ToDouble(expectedData[i]);
                double A1 = Convert.ToDouble(arrayData[i]);

                if (double.IsNaN(E1) && double.IsNaN(A1))
                    continue;
                if (double.IsInfinity(E1) && double.IsInfinity(A1))
                    continue;

                Assert.AreEqual(E1, A1, 0.00000001);
            }
        }

        internal void AssertArray<T>(ndarray arrayData, T[,] expectedData)
        {
            int lengthd0 = expectedData.GetLength(0);
            int lengthd1 = expectedData.GetLength(1);
            AssertShape(arrayData, lengthd0, lengthd1);

            for (int i = 0; i < lengthd0; i++)
            {
                ndarray rowData = arrayData[i] as ndarray;
                for (int j = 0; j < lengthd1; j++)
                {
                    double E1 = Convert.ToDouble(expectedData[i, j]);
                    double A1 = Convert.ToDouble(rowData[j]);

                    if (double.IsNaN(E1) && double.IsNaN(A1))
                        continue;
                    if (double.IsInfinity(E1) && double.IsInfinity(A1))
                        continue;

                    Assert.AreEqual(E1, A1, 0.00000001);
                }
            }
        }

        internal void AssertArray<T>(ndarray arrayData, T[,,] expectedData)
        {
            int lengthd0 = expectedData.GetLength(0);
            int lengthd1 = expectedData.GetLength(1);
            int lengthd2 = expectedData.GetLength(2);
            AssertShape(arrayData, lengthd0, lengthd1, lengthd2);

            for (int i = 0; i < lengthd0; i++)
            {
                ndarray dim1Data = arrayData[i] as ndarray;
                for (int j = 0; j < lengthd1; j++)
                {
                    ndarray dim2Data = dim1Data[j] as ndarray;
                    for (int k = 0; k < lengthd2; k++)
                    {
                        double E1 = Convert.ToDouble(expectedData[i, j, k]);
                        double A1 = Convert.ToDouble(dim2Data[k]);

                        if (double.IsNaN(E1) && double.IsNaN(A1))
                            continue;
                        if (double.IsInfinity(E1) && double.IsInfinity(A1))
                            continue;

                        Assert.AreEqual(E1, A1, 0.00000001);
                    }
                }
            }
        }

        internal void AssertArray<T>(ndarray arrayData, T[,,,] expectedData)
        {
            int lengthd0 = expectedData.GetLength(0);
            int lengthd1 = expectedData.GetLength(1);
            int lengthd2 = expectedData.GetLength(2);
            int lengthd3 = expectedData.GetLength(3);
            AssertShape(arrayData, lengthd0, lengthd1, lengthd2, lengthd3);

            for (int i = 0; i < lengthd0; i++)
            {
                ndarray dim1Data = arrayData[i] as ndarray;
                for (int j = 0; j < lengthd1; j++)
                {
                    ndarray dim2Data = dim1Data[j] as ndarray;
                    for (int k = 0; k < lengthd2; k++)
                    {
                        ndarray dim3Data = dim2Data[k] as ndarray;
                        for (int l = 0; l < lengthd3; l++)
                        {
                            double E1 = Convert.ToDouble(expectedData[i, j, k, l]);
                            double A1 = Convert.ToDouble(dim3Data[l]);

                            if (double.IsNaN(E1) && double.IsNaN(A1))
                                continue;
                            if (double.IsInfinity(E1) && double.IsInfinity(A1))
                                continue;

                            Assert.AreEqual(E1, A1, 0.00000001);
                        }
                    }
                }
            }
        }

        #endregion

    }
}
