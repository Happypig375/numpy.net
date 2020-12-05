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
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using static NumpyLib.numpyinternal;
#if NPY_INTP_64
using npy_intp = System.Int64;
#else
using npy_intp = System.Int32;
#endif

namespace NumpyLib
{
    internal partial class numpyinternal
    {
        #region NumericOP
        internal static NpyUFuncObject NpyArray_GetNumericOp(UFuncOperation op)
        {
            NpyUFuncObject loc = get_op_loc(op);
            return (null != loc) ? loc : null;
        }

        internal static NpyUFuncObject NpyArray_SetNumericOp(UFuncOperation op, NpyUFuncObject func)
        {
            throw new NotImplementedException();
        }

        private static npy_intp AdjustNegativeIndex<T>(VoidPtr data, npy_intp index)
        {
            if (index < 0)
            {
                T[] dp = data.datap as T[];
                index = dp.Length - Math.Abs(index);
            }
            return index;
        }

        static NpyUFuncObject get_op_loc(UFuncOperation op)
        {
            NpyUFuncObject loc = null;

            switch (op)
            {
                case UFuncOperation.add:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.maximum:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.minimum:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.multiply:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.logical_or:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.logical_and:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.subtract:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.divide:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.remainder:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.fmod:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.power:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.square:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.reciprocal:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.ones_like:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.sqrt:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.negative:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.absolute:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.invert:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.left_shift:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.right_shift:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.bitwise_and:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.bitwise_xor:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.bitwise_or:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.less:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.less_equal:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.equal:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.not_equal:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.greater:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.greater_equal:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.floor_divide:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.true_divide:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.floor:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.ceil:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.rint:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.conjugate:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.isnan:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.fmax:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.fmin:
                    return DefaultOpControl(op, UFuncCommon);
                case UFuncOperation.heaviside:
                    return DefaultOpControl(op, UFuncCommon);
                default:
                    loc = null;
                    break;
            }
            return loc;
        }

        private static NpyUFuncObject DefaultOpControl(UFuncOperation ops, NpyUFuncGenericFunction UFunc)
        {
            var loc = new NpyUFuncObject(UFunc)
            {
                ops = ops,
                name = "add",
                identity = NpyUFuncIdentity.NpyUFunc_Zero,
                nin = 1,
                nargs = 1,
                types = new NPY_TYPES[] {NPY_TYPES.NPY_BYTE, NPY_TYPES.NPY_UBYTE,
                                         NPY_TYPES.NPY_INT16, NPY_TYPES.NPY_UINT16,
                                         NPY_TYPES.NPY_INT32, NPY_TYPES.NPY_UINT32,
                                         NPY_TYPES.NPY_INT64, NPY_TYPES.NPY_UINT64,
                                         NPY_TYPES.NPY_FLOAT, NPY_TYPES.NPY_DOUBLE,
                                         NPY_TYPES.NPY_DECIMAL, NPY_TYPES.NPY_COMPLEX,
                                         NPY_TYPES.NPY_BIGINT, NPY_TYPES.NPY_OBJECT, NPY_TYPES.NPY_STRING},

            };

            return loc;
        }
        #endregion

        #region UFUNC Handlers

        private static IUFUNC_Operations GetUFuncHandler(NPY_TYPES npy_type)
        {
            switch (npy_type)
            {
                case NPY_TYPES.NPY_BOOL:
                    return new UFUNC_Bool();

                case NPY_TYPES.NPY_BYTE:
                    return new UFUNC_SByte();

                case NPY_TYPES.NPY_UBYTE:
                    return new UFUNC_UByte();

                case NPY_TYPES.NPY_INT16:
                    return new UFUNC_Int16();

                case NPY_TYPES.NPY_UINT16:
                    return new UFUNC_UInt16();

                case NPY_TYPES.NPY_INT32:
                    return new UFUNC_Int32();

                case NPY_TYPES.NPY_UINT32:
                    return new UFUNC_UInt32();

                case NPY_TYPES.NPY_INT64:
                    return new UFUNC_Int64();

                case NPY_TYPES.NPY_UINT64:
                    return new UFUNC_UInt64();

                case NPY_TYPES.NPY_FLOAT:
                    return new UFUNC_Float();

                case NPY_TYPES.NPY_DOUBLE:
                    return new UFUNC_Double();

                case NPY_TYPES.NPY_DECIMAL:
                    return new UFUNC_Decimal();

                case NPY_TYPES.NPY_COMPLEX:
                    return new UFUNC_Complex();

                case NPY_TYPES.NPY_BIGINT:
                    return new UFUNC_BigInt();

                case NPY_TYPES.NPY_OBJECT:
                    return new UFUNC_Object();

                default:
                    return null;
            }
        }


        internal static void UFuncCommon(GenericReductionOp op, VoidPtr[] bufPtr, npy_intp N, npy_intp[] steps, UFuncOperation Ops)
        {
            VoidPtr Result = bufPtr[2];

            if (Result.type_num == bufPtr[0].type_num && Result.type_num == bufPtr[0].type_num)
            {
                IUFUNC_Operations UFunc = GetUFuncHandler(Result.type_num);
                if (UFunc != null)
                {
                    if (op == GenericReductionOp.NPY_UFUNC_REDUCE)
                    {
                        UFunc.PerformReduceOpArrayIter(bufPtr, steps, Ops, N);
                        return;
                    }
                    if (op == GenericReductionOp.NPY_UFUNC_ACCUMULATE)
                    {
                        UFunc.PerformAccumulateOpArrayIter(bufPtr, steps, Ops, N);
                        return;
                    }
                    if (op == GenericReductionOp.NPY_UFUNC_REDUCEAT)
                    {
                        UFunc.PerformReduceAtOpArrayIter(bufPtr, steps, Ops, N);
                        return;
                    }
                }
            }


            switch (Result.type_num)
            {
                case NPY_TYPES.NPY_BOOL:
                    UFuncCommon_R<bool>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BYTE:
                    UFuncCommon_R<sbyte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UBYTE:
                    UFuncCommon_R<byte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT16:
                    UFuncCommon_R<Int16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT16:
                    UFuncCommon_R<UInt16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT32:
                    UFuncCommon_R<Int32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT32:
                    UFuncCommon_R<UInt32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT64:
                    UFuncCommon_R<Int64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT64:
                    UFuncCommon_R<UInt64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_FLOAT:
                    UFuncCommon_R<float>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DOUBLE:
                    UFuncCommon_R<double>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DECIMAL:
                    UFuncCommon_R<decimal>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_COMPLEX:
                    UFuncCommon_R<System.Numerics.Complex>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BIGINT:
                    UFuncCommon_R<System.Numerics.BigInteger>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_OBJECT:
                    UFuncCommon_R<object>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_STRING:
                    UFuncCommon_R<string>(op, bufPtr, N, steps, Ops);
                    break;
            }

            return;
        }

        private static void UFuncCommon_R<R>(GenericReductionOp op, VoidPtr[] bufPtr, npy_intp N, npy_intp[] steps, UFuncOperation Ops)
        {
            VoidPtr Result = bufPtr[0];

            switch (Result.type_num)
            {
                case NPY_TYPES.NPY_BOOL:
                    UFuncCommon_RO<R, bool>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BYTE:
                    UFuncCommon_RO<R, sbyte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UBYTE:
                    UFuncCommon_RO<R, byte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT16:
                    UFuncCommon_RO<R, Int16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT16:
                    UFuncCommon_RO<R, UInt16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT32:
                    UFuncCommon_RO<R, Int32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT32:
                    UFuncCommon_RO<R, UInt32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT64:
                    UFuncCommon_RO<R, Int64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT64:
                    UFuncCommon_RO<R, UInt64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_FLOAT:
                    UFuncCommon_RO<R, float>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DOUBLE:
                    UFuncCommon_RO<R, double>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DECIMAL:
                    UFuncCommon_RO<R, decimal>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_COMPLEX:
                    UFuncCommon_RO<R, System.Numerics.Complex>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BIGINT:
                    UFuncCommon_RO<R, System.Numerics.BigInteger>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_OBJECT:
                    UFuncCommon_RO<R, object>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_STRING:
                    UFuncCommon_RO<R, string>(op, bufPtr, N, steps, Ops);
                    break;
            }

            return;
        }

        private static void UFuncCommon_RO<R, O1>(GenericReductionOp op, VoidPtr[] bufPtr, npy_intp N, npy_intp[] steps, UFuncOperation Ops)
        {
            VoidPtr Result = bufPtr[1];

            switch (Result.type_num)
            {
                case NPY_TYPES.NPY_BOOL:
                    UFuncCommon_ROO<R, O1, bool>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BYTE:
                    UFuncCommon_ROO<R, O1, sbyte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UBYTE:
                    UFuncCommon_ROO<R, O1, byte>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT16:
                    UFuncCommon_ROO<R, O1, Int16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT16:
                    UFuncCommon_ROO<R, O1, UInt16>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT32:
                    UFuncCommon_ROO<R, O1, Int32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT32:
                    UFuncCommon_ROO<R, O1, UInt32>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_INT64:
                    UFuncCommon_ROO<R, O1, Int64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_UINT64:
                    UFuncCommon_ROO<R, O1, UInt64>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_FLOAT:
                    UFuncCommon_ROO<R, O1, float>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DOUBLE:
                    UFuncCommon_ROO<R, O1, double>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_DECIMAL:
                    UFuncCommon_ROO<R, O1, decimal>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_COMPLEX:
                    UFuncCommon_ROO<R, O1, System.Numerics.Complex>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_BIGINT:
                    UFuncCommon_ROO<R, O1, System.Numerics.BigInteger>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_OBJECT:
                    UFuncCommon_ROO<R, O1, object>(op, bufPtr, N, steps, Ops);
                    break;
                case NPY_TYPES.NPY_STRING:
                    UFuncCommon_ROO<R, O1, string>(op, bufPtr, N, steps, Ops);
                    break;
            }
        }

        private static void UFuncCommon_ROO<R, O1, O2>(GenericReductionOp op, VoidPtr[] bufPtr, npy_intp N, npy_intp[] steps, UFuncOperation ops)
        {
            if (op == GenericReductionOp.NPY_UFUNC_REDUCE)
            {
                UFuncCommon_REDUCE<R, O1, O2>(bufPtr, N, steps, ops);
                return;
            }

            if (op == GenericReductionOp.NPY_UFUNC_ACCUMULATE)
            {
                UFuncCommon_ACCUMULATE<R, O1, O2>(bufPtr, N, steps, ops);
                return;
            }

            if (op == GenericReductionOp.NPY_UFUNC_REDUCEAT)
            {
                UFuncCommon_REDUCEAT<R, O1, O2>(bufPtr, N, steps, ops);
                return;
            }

            if (op == GenericReductionOp.NPY_UFUNC_OUTER)
            {
                UFuncCommon_OUTER<R, O1, O2>(bufPtr, N, steps, ops);
                return;
            }

            throw new Exception("Unexpected UFUNC TYPE");

        }

        private static void UFuncCommon_REDUCE<R, O1, O2>(VoidPtr[] bufPtr, npy_intp N, npy_intp[] steps, UFuncOperation ops)
        {
            VoidPtr Operand1 = bufPtr[0];
            VoidPtr Operand2 = bufPtr[1];
            VoidPtr Result = bufPtr[2];

            npy_intp O1_Step = steps[0];
            npy_intp O2_Step = steps[1];
            npy_intp R_Step = steps[2];

            if (Operand2 == null)
            {
                Operand2 = Operand1;
                O2_Step = O1_Step;
            }
            if (Result == null)
            {
                Result = Operand1;
                R_Step = O1_Step;
            }



            NumericOperation Operation = GetOperation(Operand1, ops);
            var Operand1Handler = DefaultArrayHandlers.GetArrayHandler(Operand1.type_num);
            var Operand2Handler = DefaultArrayHandlers.GetArrayHandler(Operand2.type_num);
            var ResultHandler = DefaultArrayHandlers.GetArrayHandler(Result.type_num);

            npy_intp O1_sizeData = Operand1Handler.ItemSize;
            npy_intp O2_sizeData = Operand2Handler.ItemSize;
            npy_intp R_sizeData = ResultHandler.ItemSize;

            npy_intp O1_Offset = Operand1.data_offset;
            npy_intp O2_Offset = Operand2.data_offset;
            npy_intp R_Offset = Result.data_offset;

            npy_intp R_Index = AdjustNegativeIndex<R>(Result, R_Offset / R_sizeData);
            npy_intp O1_Index = AdjustNegativeIndex<O1>(Operand1, O1_Offset / O1_sizeData);

            R[] retArray = Result.datap as R[];
            O1[] Op1Array = Operand1.datap as O1[];
            O2[] Op2Array = Operand2.datap as O2[];

            npy_intp O2_CalculatedStep = (O2_Step / O2_sizeData);
            npy_intp O2_CalculatedOffset = (O2_Offset / O2_sizeData);

            bool ThrewException = false;


            for (int i = 0; i < N; i++)
            {

                try
                {
                    var O1Value = Op1Array[O1_Index];

                    npy_intp O2_Index = ((i * O2_CalculatedStep) + O2_CalculatedOffset);
                    var O2Value = Op2Array[O2_Index];                                            // get operand 2

                    retry:
                    if (ThrewException)
                    {
                        var RRValue = Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                        ResultHandler.SetIndex(Result, R_Index, RRValue);
                    }
                    else
                    {
                        try
                        {
                            R RValue = (R)Operation(O1Value, O2Value);    // calculate result
                            retArray[R_Index] = RValue;
                        }
                        catch
                        {
                            ThrewException = true;
                            goto retry;
                        }

                    }

                }
                catch (System.OverflowException oe)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_OverflowError, oe.Message);
                }
                catch (Exception ex)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                }
            }

            return;
        }

        private static void UFuncCommon_ACCUMULATE<R, O1, O2>(VoidPtr[] bufPtr, long N, long[] steps, UFuncOperation ops)
        {
            VoidPtr Operand1 = bufPtr[0];
            VoidPtr Operand2 = bufPtr[1];
            VoidPtr Result = bufPtr[2];

            npy_intp O1_Step = steps[0];
            npy_intp O2_Step = steps[1];
            npy_intp R_Step = steps[2];

            if (Operand2 == null)
            {
                Operand2 = Operand1;
                O2_Step = O1_Step;
            }
            if (Result == null)
            {
                Result = Operand1;
                R_Step = O1_Step;
            }

            NumericOperation Operation = GetOperation(Operand1, ops);
            var Operand1Handler = DefaultArrayHandlers.GetArrayHandler(Operand1.type_num);
            var Operand2Handler = DefaultArrayHandlers.GetArrayHandler(Operand2.type_num);
            var ResultHandler = DefaultArrayHandlers.GetArrayHandler(Result.type_num);

            npy_intp O1_sizeData = Operand1Handler.ItemSize;
            npy_intp O2_sizeData = Operand2Handler.ItemSize;
            npy_intp R_sizeData = ResultHandler.ItemSize;

            npy_intp O1_Offset = Operand1.data_offset;
            npy_intp O2_Offset = Operand2.data_offset;
            npy_intp R_Offset = Result.data_offset;


            R[] retArray = Result.datap as R[];
            O1[] Op1Array = Operand1.datap as O1[];
            O2[] Op2Array = Operand2.datap as O2[];

            npy_intp O1_CalculatedStep = (O1_Step / O1_sizeData);
            npy_intp O1_CalculatedOffset = (O1_Offset / O1_sizeData);

            npy_intp O2_CalculatedStep = (O2_Step / O2_sizeData);
            npy_intp O2_CalculatedOffset = (O2_Offset / O2_sizeData);

            npy_intp R_CalculatedStep = (R_Step / R_sizeData);
            npy_intp R_CalculatedOffset = (R_Offset / R_sizeData);

            bool ThrewException = false;

            for (int i = 0; i < N; i++)
            {
                npy_intp O1_Index = ((i * O1_CalculatedStep) + O1_CalculatedOffset);
                npy_intp O2_Index = ((i * O2_CalculatedStep) + O2_CalculatedOffset);
                npy_intp R_Index = ((i * R_CalculatedStep) + R_CalculatedOffset);

                var O1Value = Op1Array[O1_Index];                                            // get operand 1
                var O2Value = Op2Array[O2_Index];                                            // get operand 2

                try
                {
                    retry:
                    if (ThrewException)
                    {
                        var RRValue = Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                        ResultHandler.SetIndex(Result, R_Index, RRValue);
                    }
                    else
                    {
                        try
                        {
                            R RValue = (R)Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                            retArray[R_Index] = RValue;
                        }
                        catch
                        {
                            ThrewException = true;
                            goto retry;
                        }
                    }

                }
                catch (System.OverflowException oe)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_OverflowError, oe.Message);
                }
                catch (Exception ex)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                }
            }
        }

        private static void UFuncCommon_REDUCEAT<R, O1, O2>(VoidPtr[] bufPtr, long N, long[] steps, UFuncOperation ops)
        {
            VoidPtr Operand1 = bufPtr[0];
            VoidPtr Operand2 = bufPtr[1];
            VoidPtr Result = bufPtr[2];

            npy_intp O1_Step = steps[0];
            npy_intp O2_Step = steps[1];
            npy_intp R_Step = steps[2];

            if (Operand2 == null)
            {
                Operand2 = Operand1;
                O2_Step = O1_Step;
            }
            if (Result == null)
            {
                Result = Operand1;
                R_Step = O1_Step;
            }

            NumericOperation Operation = GetOperation(Operand1, ops);
            var Operand1Handler = DefaultArrayHandlers.GetArrayHandler(Operand1.type_num);
            var Operand2Handler = DefaultArrayHandlers.GetArrayHandler(Operand2.type_num);
            var ResultHandler = DefaultArrayHandlers.GetArrayHandler(Result.type_num);

            npy_intp O1_sizeData = Operand1Handler.ItemSize;
            npy_intp O2_sizeData = Operand2Handler.ItemSize;
            npy_intp R_sizeData = ResultHandler.ItemSize;

            npy_intp O1_Offset = Operand1.data_offset;
            npy_intp O2_Offset = Operand2.data_offset;
            npy_intp R_Offset = Result.data_offset;


            R[] retArray = Result.datap as R[];
            O1[] Op1Array = Operand1.datap as O1[];
            O2[] Op2Array = Operand2.datap as O2[];

            npy_intp O1_CalculatedStep = (O1_Step / O1_sizeData);
            npy_intp O1_CalculatedOffset = (O1_Offset / O1_sizeData);

            npy_intp O2_CalculatedStep = (O2_Step / O2_sizeData);
            npy_intp O2_CalculatedOffset = (O2_Offset / O2_sizeData);

            npy_intp R_CalculatedStep = (R_Step / R_sizeData);
            npy_intp R_CalculatedOffset = (R_Offset / R_sizeData);

            bool ThrewException = false;

            for (int i = 0; i < N; i++)
            {
                npy_intp O1_Index = ((i * O1_CalculatedStep) + O1_CalculatedOffset);
                npy_intp O2_Index = ((i * O2_CalculatedStep) + O2_CalculatedOffset);
                npy_intp R_Index = ((i * R_CalculatedStep) + R_CalculatedOffset);

                var O1Value = Op1Array[O1_Index];                                            // get operand 1
                var O2Value = Op2Array[O2_Index];                                            // get operand 2

                try
                {
                    retry:
                    if (ThrewException)
                    {
                        var RRValue = Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                        ResultHandler.SetIndex(Result, R_Index, RRValue);
                    }
                    else
                    {
                        try
                        {
                            R RValue = (R)Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                            retArray[R_Index] = RValue;
                        }
                        catch
                        {
                            ThrewException = true;
                            goto retry;
                        }
                    }

                }
                catch (System.OverflowException oe)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_OverflowError, oe.Message);
                }
                catch (Exception ex)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                }
            }
        }

        private static void UFuncCommon_OUTER<R, O1, O2>(VoidPtr[] bufPtr, long N, long[] steps, UFuncOperation ops)
        {
            VoidPtr Operand1 = bufPtr[0];
            VoidPtr Operand2 = bufPtr[1];
            VoidPtr Result = bufPtr[2];

            npy_intp O1_Step = steps[0];
            npy_intp O2_Step = steps[1];
            npy_intp R_Step = steps[2];

            if (Operand2 == null)
            {
                Operand2 = Operand1;
                O2_Step = O1_Step;
            }
            if (Result == null)
            {
                Result = Operand1;
                R_Step = O1_Step;
            }

            NumericOperation Operation = GetOperation(Operand1, ops);
            var Operand1Handler = DefaultArrayHandlers.GetArrayHandler(Operand1.type_num);
            var Operand2Handler = DefaultArrayHandlers.GetArrayHandler(Operand2.type_num);
            var ResultHandler = DefaultArrayHandlers.GetArrayHandler(Result.type_num);

            npy_intp O1_sizeData = Operand1Handler.ItemSize;
            npy_intp O2_sizeData = Operand2Handler.ItemSize;
            npy_intp R_sizeData = ResultHandler.ItemSize;

            npy_intp O1_Offset = Operand1.data_offset;
            npy_intp O2_Offset = Operand2.data_offset;
            npy_intp R_Offset = Result.data_offset;


            R[] retArray = Result.datap as R[];
            O1[] Op1Array = Operand1.datap as O1[];
            O2[] Op2Array = Operand2.datap as O2[];

            npy_intp O2_CalculatedStep = (O2_Step / O2_sizeData);
            npy_intp O2_CalculatedOffset = (O2_Offset / O2_sizeData);

            for (int i = 0; i < N; i++)
            {
                npy_intp O1_Index = ((i * O1_Step) + O1_Offset) / O1_sizeData;
                npy_intp O2_Index = ((i * O2_Step) + O2_Offset) / O2_sizeData;
                npy_intp R_Index = ((i * R_Step) + R_Offset) / R_sizeData;

                try
                {
                    var O1Value = Operand1Handler.GetIndex(Operand1, O1_Index);                  // get operand 1
                    var O2Value = Operand2Handler.GetIndex(Operand2, O2_Index);                  // get operand 2
                    var RValue = Operation(O1Value, Operand1Handler.MathOpConvertOperand(O1Value, O2Value));    // calculate result
                    ResultHandler.SetIndex(Result, R_Index, RValue);
                }
                catch (System.OverflowException oe)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_OverflowError, oe.Message);
                }
                catch (Exception ex)
                {
                    NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                }
            }
        }

        #endregion

        internal abstract class UFUNC_BASE<T>
        {
            public UFUNC_BASE(int sizeOfItem)
            {
                this.SizeOfItem = sizeOfItem;
            }
            protected int SizeOfItem;


            #region SCALAR CALCULATIONS
            public void PerformScalarOpArrayIter(NpyArray destArray, NpyArray srcArray, NpyArray operArray, UFuncOperation op)
            {
                var destSize = NpyArray_Size(destArray);

                var SrcIter = NpyArray_BroadcastToShape(srcArray, destArray.dimensions, destArray.nd);
                var DestIter = NpyArray_BroadcastToShape(destArray, destArray.dimensions, destArray.nd);
                var OperIter = NpyArray_BroadcastToShape(operArray, destArray.dimensions, destArray.nd);

                if (!SrcIter.requiresIteration && !DestIter.requiresIteration && !operArray.IsASlice)
                {
                    PerformNumericOpScalarIterContiguousNoIter(srcArray, destArray, operArray, op, SrcIter, DestIter, OperIter);
                    return;
                }

                

                if (Vector.IsHardwareAccelerated && destArray.ItemType == NPY_TYPES.NPY_DOUBLE && false)
                {
                    PerformNumericOpScalarSmallIterSIMD(srcArray, destArray, operArray, op, SrcIter, DestIter, OperIter, destSize);
                }
                else
                {
                    PerformNumericOpScalarSmallIter(srcArray, destArray, operArray, op, SrcIter, DestIter, OperIter, destSize);
                }

                return;

            }

  
            protected void PerformNumericOpScalarSmallIterNEW(NpyArray srcArray, NpyArray destArray, NpyArray operArray, UFuncOperation op, NpyArrayIterObject srcIter, NpyArrayIterObject destIter, NpyArrayIterObject operIter, npy_intp taskSize)
            {
                T[] src = srcArray.data.datap as T[];
                T[] dest = destArray.data.datap as T[];
                T[] oper = operArray.data.datap as T[];

                var UFuncOperation = GetUFuncOperation(op);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", op.ToString()));
                }

                List<Exception> caughtExceptions = new List<Exception>();

                var srcParallelIters = NpyArray_ITER_ParallelSplit(srcIter, numpyinternal.maxNumericOpParallelSize);
                var destParallelIters = NpyArray_ITER_ParallelSplit(destIter, numpyinternal.maxNumericOpParallelSize);
                var operParallelIters = NpyArray_ITER_ParallelSplit(operIter, numpyinternal.maxNumericOpParallelSize);

                Parallel.For(0, destParallelIters.Count(), index =>
                //for (int index = 0; index < destParallelIters.Count(); index++) // 
                {
                    var ldestIter = destParallelIters.ElementAt(index);
                    var lsrcIter = srcParallelIters.ElementAt(index);
                    var loperIter = operParallelIters.ElementAt(index);

                    npy_intp srcDataOffset = srcArray.data.data_offset;
                    npy_intp operDataOffset = operArray.data.data_offset;

                    while (ldestIter.index < ldestIter.size)
                    {
                        npy_intp cacheSize = ldestIter.size - ldestIter.index;
                        NpyArray_ITER_CACHE(ldestIter, cacheSize);
                        NpyArray_ITER_CACHE(lsrcIter, cacheSize);
                        NpyArray_ITER_CACHE(loperIter, cacheSize);

                        try
                        {
                            while (ldestIter.IsCacheEmpty == false)
                            {
                                var srcValue = src[AdjustedIndex_GetItemFunction(lsrcIter.GetNextCache() - srcDataOffset, srcArray, src.Length)];
                                var operand = oper[AdjustedIndex_GetItemFunction(loperIter.GetNextCache() - operDataOffset, operArray, oper.Length)];
                                var destIndex = AdjustedIndex_GetItemFunction(ldestIter.GetNextCache() - destArray.data.data_offset, destArray, dest.Length);

                                try
                                {
                                    dest[destIndex] = UFuncOperation(srcValue, operand);
                                }
                                catch
                                {
                                    dest[destIndex] = default(T);
                                }
                            }

                        }
                        catch (Exception ex)
                        {
                            caughtExceptions.Add(ex);
                        }

                    }
                });




                if (caughtExceptions.Count > 0)
                {
                    throw caughtExceptions[0];
                }
            }


            protected void PerformNumericOpScalarSmallIter(NpyArray srcArray, NpyArray destArray, NpyArray operArray, UFuncOperation op, NpyArrayIterObject srcIter, NpyArrayIterObject destIter, NpyArrayIterObject operIter, npy_intp taskSize)
            {
                T[] src = srcArray.data.datap as T[];
                T[] dest = destArray.data.datap as T[];
                T[] oper = operArray.data.datap as T[];

                var UFuncOperation = GetUFuncOperation(op);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", op.ToString()));
                }

                List<Exception> caughtExceptions = new List<Exception>();

                var srcParallelIters = NpyArray_ITER_ParallelSplit(srcIter, numpyinternal.maxNumericOpParallelSize);
                var destParallelIters = NpyArray_ITER_ParallelSplit(destIter, numpyinternal.maxNumericOpParallelSize);
                var operParallelIters = NpyArray_ITER_ParallelSplit(operIter, numpyinternal.maxNumericOpParallelSize);

                Parallel.For(0, destParallelIters.Count(), index =>
                //for (int index = 0; index < destParallelIters.Count(); index++) // 
                {
                    var ldestIter = destParallelIters.ElementAt(index);
                    var lsrcIter = srcParallelIters.ElementAt(index);
                    var loperIter = operParallelIters.ElementAt(index);

                    npy_intp srcDataOffset = srcArray.data.data_offset;
                    npy_intp operDataOffset = operArray.data.data_offset;

                    while (ldestIter.index < ldestIter.size)
                    {
                        try
                        {
                            var srcValue = src[AdjustedIndex_GetItemFunction(lsrcIter.dataptr.data_offset - srcDataOffset, srcArray, src.Length)];
                            var operand = oper[AdjustedIndex_GetItemFunction(loperIter.dataptr.data_offset - operDataOffset, operArray, oper.Length)];
                            npy_intp destIndex = AdjustedIndex_GetItemFunction(ldestIter.dataptr.data_offset - destArray.data.data_offset, destArray, dest.Length);

                            try
                            {
                                 dest[destIndex] = UFuncOperation(srcValue, operand);
                            }
                            catch
                            {
                                dest[destIndex] = default(T);
                            }

                            NpyArray_ITER_NEXT(ldestIter);
                            NpyArray_ITER_NEXT(lsrcIter);
                            NpyArray_ITER_NEXT(loperIter);

                        }
                        catch (Exception ex)
                        {
                            caughtExceptions.Add(ex);
                        }

                    }
                } );




                if (caughtExceptions.Count > 0)
                {
                    throw caughtExceptions[0];
                }
            }

            private void PerformNumericOpScalarSmallIterSIMD(NpyArray srcArray, NpyArray destArray, NpyArray operArray, UFuncOperation op, NpyArrayIterObject srcIter, NpyArrayIterObject destIter, NpyArrayIterObject operIter, long destSize)
            {
                double[] src = srcArray.data.datap as double[];
                double[] dest = destArray.data.datap as double[];
                double[] oper = operArray.data.datap as double[];

                List<Exception> caughtExceptions = new List<Exception>();

                var simdLength = Vector<double>.Count * 100;
                double[] srcItem = new double[simdLength];
                double[] operItem = new double[simdLength];

                var srcParallelIters = NpyArray_ITER_ParallelSplit(srcIter, numpyinternal.maxNumericOpParallelSize);
                var destParallelIters = NpyArray_ITER_ParallelSplit(destIter, numpyinternal.maxNumericOpParallelSize);
                var operParallelIters = NpyArray_ITER_ParallelSplit(operIter, numpyinternal.maxNumericOpParallelSize);

                //Parallel.For(0, destParallelIters.Count(), index =>
                for (int index = 0; index < destParallelIters.Count(); index++) // 
                {
                    var ldestIter = destParallelIters.ElementAt(index);
                    var lsrcIter = srcParallelIters.ElementAt(index);
                    var loperIter = operParallelIters.ElementAt(index);

                    npy_intp srcDataOffset = srcArray.data.data_offset;
                    npy_intp operDataOffset = operArray.data.data_offset;

                    while (ldestIter.index < ldestIter.size)
                    {
                        try
                        {
                            npy_intp simdIndex = 0;
                            npy_intp destIndex = 0;

                            long lsimdLength = Math.Min(simdLength, ldestIter.size - ldestIter.index);
                            while (simdIndex < lsimdLength)
                            {
                                srcItem[simdIndex] = src[AdjustedIndex_GetItemFunction(lsrcIter.dataptr.data_offset - srcDataOffset, srcArray, src.Length)];
                                operItem[simdIndex] = oper[AdjustedIndex_GetItemFunction(loperIter.dataptr.data_offset - operDataOffset, operArray, oper.Length)];
                                
                                if (simdIndex == 0)
                                    destIndex = AdjustedIndex_GetItemFunction(ldestIter.dataptr.data_offset - destArray.data.data_offset, destArray, dest.Length);

                                simdIndex++;

                                if (simdIndex == lsimdLength)
                                {
                                    try
                                    {
                                        if (op == NumpyLib.UFuncOperation.add)
                                            SIMDArrayAddition(srcItem, operItem, dest, (int)destIndex);
                                        else if (op == NumpyLib.UFuncOperation.divide)
                                            SIMDArrayDivide(srcItem, operItem, dest, (int)destIndex);
                                    }
                                    catch
                                    {
                                        dest[destIndex] = 0;
                                    }
                                }
           

                                NpyArray_ITER_NEXT(ldestIter);
                                NpyArray_ITER_NEXT(lsrcIter);
                                NpyArray_ITER_NEXT(loperIter);
                            }
            

                        }
                        catch (Exception ex)
                        {
                            caughtExceptions.Add(ex);
                        }

                    }
                } //);




                if (caughtExceptions.Count > 0)
                {
                    throw caughtExceptions[0];
                }
            }

            private static double[] SIMDArrayAddition(double[] lhs, double[] rhs, double [] result, int resultOffset)
            {
                var simdLength = Vector<double>.Count;
                var i = 0;
                for (i = 0; i <= lhs.Length - simdLength; i += simdLength)
                {
                    var va = new Vector<double>(lhs, i);
                    var vb = new Vector<double>(rhs, i);
                    (va + vb).CopyTo(result, resultOffset);
                }

                for (; i < lhs.Length; ++i)
                {
                    result[resultOffset + i] = (float)(lhs[i] + rhs[i]);
                }

                return result;
            }

            private static double[] SIMDArrayDivide(double[] lhs, double[] rhs, double[] result, int resultOffset)
            {
                var simdLength = Vector<double>.Count;
                var i = 0;
                for (i = 0; i <= lhs.Length - simdLength; i += simdLength)
                {
                    var va = new Vector<double>(lhs, i);
                    var vb = new Vector<double>(rhs, i);
                    (va / vb).CopyTo(result, resultOffset);
                }

                for (; i < lhs.Length; ++i)
                {
                    result[resultOffset + i] = lhs[i] / rhs[i];
                }

                return result;
            }


            protected void PerformNumericOpScalarIterContiguousNoIter(NpyArray srcArray, NpyArray destArray, NpyArray operArray, UFuncOperation op, NpyArrayIterObject srcIter, NpyArrayIterObject destIter, NpyArrayIterObject operIter)
            {
                T[] src = srcArray.data.datap as T[];
                T[] dest = destArray.data.datap as T[];
                T[] oper = operArray.data.datap as T[];


                int srcAdjustment = (int)srcArray.data.data_offset / srcArray.ItemSize;
                int destAdjustment = (int)destArray.data.data_offset / destArray.ItemSize;

                var exceptions = new ConcurrentQueue<Exception>();

                var loopCount = NpyArray_Size(destArray);

                var UFuncOperation = GetUFuncOperation(op);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", op.ToString()));
                }

                if (NpyArray_Size(operArray) == 1 && !operArray.IsASlice)
                {
                    T operand = oper[0];

                    Parallel.For(0, loopCount, index =>
                    //for (npy_intp index = 0; index < loopCount; index++)
                    {
                        try
                        {
                            T srcValue = src[index - srcAdjustment];
                            dest[index - destAdjustment] = UFuncOperation(srcValue, operand);
                        }
                        catch (System.OverflowException of)
                        {
                            dest[index - destAdjustment] = default(T);
                        }
                        catch (Exception ex)
                        {
                            exceptions.Enqueue(ex);
                        }

                    } );
                }
                else
                {
                    var ParallelIters = NpyArray_ITER_ParallelSplit(operIter, numpyinternal.maxNumericOpParallelSize);

                    Parallel.For(0, ParallelIters.Count(), index =>
                    {
                        var Iter = ParallelIters.ElementAt(index);

                        while (Iter.index < Iter.size)
                        {
                            try
                            {
                                T operand = oper[Iter.dataptr.data_offset / SizeOfItem];
                                T srcValue = src[Iter.index - srcAdjustment];

                                T retValue = retValue = UFuncOperation(srcValue, operand);
                                dest[Iter.index - destAdjustment] = retValue;
                            }
                            catch (System.OverflowException of)
                            {
                                dest[Iter.index - destAdjustment] = default(T);
                            }
                            catch (Exception ex)
                            {
                                exceptions.Enqueue(ex);
                            }

                            NpyArray_ITER_NEXT(Iter);
                        }

                    } );
                }

                if (exceptions.Count > 0)
                {
                    throw exceptions.ElementAt(0);
                }

            }

            #endregion

            #region UFUNC Outer
            public void PerformOuterOpArrayIter(NpyArray a, NpyArray b, NpyArray destArray, NumericOperations operations, UFuncOperation op)
            {
                var destSize = NpyArray_Size(destArray);
                var aSize = NpyArray_Size(a);
                var bSize = NpyArray_Size(b);

                if (bSize == 0 || aSize == 0)
                {
                    NpyArray_Resize(destArray, new NpyArray_Dims() { len = 0, ptr = new npy_intp[] { } }, false, NPY_ORDER.NPY_ANYORDER);
                    return;
                }

                var aIter = NpyArray_IterNew(a);
                var bIter = NpyArray_IterNew(b);
                var DestIter = NpyArray_IterNew(destArray);

                T[] aValues = new T[aSize];
                for (long i = 0; i < aSize; i++)
                {
                    aValues[i] = ConvertToTemplate(operations.srcGetItem(aIter.dataptr.data_offset - a.data.data_offset, a));
                    NpyArray_ITER_NEXT(aIter);
                }

                T[] bValues = new T[bSize];
                for (long i = 0; i < bSize; i++)
                {
                    bValues[i] = ConvertToTemplate(operations.operandGetItem(bIter.dataptr.data_offset - b.data.data_offset, b));
                    NpyArray_ITER_NEXT(bIter);
                }


                T[] dp = destArray.data.datap as T[];

                var UFuncOperation = GetUFuncOperation(op);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", op.ToString()));
                }
                
                if (DestIter.contiguous && destSize > UFUNC_PARALLEL_DEST_MINSIZE && aSize > UFUNC_PARALLEL_DEST_ASIZE)
                {
                    List<Exception> caughtExceptions = new List<Exception>();

                    Parallel.For(0, aSize, i =>
                    {
                        try
                        {
                            var aValue = aValues[i];

                            long destIndex = (destArray.data.data_offset / destArray.ItemSize) + i * bSize;

                            for (long j = 0; j < bSize; j++)
                            {
                                var bValue = bValues[j];
  
                                try
                                {
                                    dp[destIndex] = UFuncOperation(aValue, bValue);
                                }
                                catch
                                {
                                    operations.destSetItem(destIndex, 0, destArray);
                                }
                                destIndex++;
                            }
                        }
                        catch (Exception ex)
                        {
                            caughtExceptions.Add(ex);
                        }


                    });

                    if (caughtExceptions.Count > 0)
                    {
                        Exception ex = caughtExceptions[0];
                        if (ex is System.OverflowException)
                        {
                            NpyErr_SetString(npyexc_type.NpyExc_OverflowError, ex.Message);
                            return;
                        }

                        NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                        return;
                    }
                }
                else
                {
                    try
                    {
                        for (long i = 0; i < aSize; i++)
                        {
                            var aValue = aValues[i];

                            for (long j = 0; j < bSize; j++)
                            {
                                var bValue = bValues[j];

                                T destValue = UFuncOperation(aValue, bValue);
   
                                try
                                {
                                    long AdjustedIndex = AdjustedIndex_SetItemFunction(DestIter.dataptr.data_offset - destArray.data.data_offset, destArray, dp.Length);
                                    dp[AdjustedIndex] = destValue;
                                }
                                catch
                                {
                                    long AdjustedIndex = AdjustedIndex_SetItemFunction(DestIter.dataptr.data_offset - destArray.data.data_offset, destArray, dp.Length);
                                    operations.destSetItem(AdjustedIndex, 0, destArray);
                                }
                                NpyArray_ITER_NEXT(DestIter);
                            }

                        }
                    }
                    catch (System.OverflowException ex)
                    {
                        NpyErr_SetString(npyexc_type.NpyExc_OverflowError, ex.Message);
                        return;
                    }
                    catch (Exception ex)
                    {
                        NpyErr_SetString(npyexc_type.NpyExc_ValueError, ex.Message);
                        return;
                    }

                }


            }

            #endregion

            #region UFUNC Reduce

            public void PerformReduceOpArrayIter(VoidPtr[] bufPtr, npy_intp[] steps, UFuncOperation ops, npy_intp N)
            {
                VoidPtr Operand1 = bufPtr[0];
                VoidPtr Operand2 = bufPtr[1];
                VoidPtr Result = bufPtr[2];

                npy_intp O1_Step = steps[0];
                npy_intp O2_Step = steps[1];
                npy_intp R_Step = steps[2];

                npy_intp O1_Offset = Operand1.data_offset;
                npy_intp O2_Offset = Operand2.data_offset;
                npy_intp R_Offset = Result.data_offset;


                T[] retArray = Result.datap as T[];
                T[] Op1Array = Operand1.datap as T[];
                T[] Op2Array = Operand2.datap as T[];

                npy_intp R_Index = AdjustNegativeIndex(retArray, R_Offset / SizeOfItem);
                npy_intp O1_Index = AdjustNegativeIndex(Op1Array, O1_Offset / SizeOfItem);

                npy_intp O2_CalculatedStep = (O2_Step / SizeOfItem);
                npy_intp O2_CalculatedOffset = (O2_Offset / SizeOfItem);


                T retValue = retArray[R_Index];

                var UFuncOperation = GetUFuncOperation(ops);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", ops.ToString()));
                }

                // note: these can't be parrallized.
                for (int i = 0; i < N; i++)
                {
                    npy_intp O2_Index = ((i * O2_CalculatedStep) + O2_CalculatedOffset);

                    var Op1Value = retValue;
                    var Op2Value = Op2Array[O2_Index];

                    retValue = UFuncOperation(Op1Value, Op2Value);
                }

                retArray[R_Index] = retValue;
                return;
            }


            #endregion

            #region UFUNC Accumulate

            public void PerformAccumulateOpArrayIter(VoidPtr[] bufPtr, npy_intp[] steps, UFuncOperation ops, npy_intp N)
            {
                VoidPtr Operand1 = bufPtr[0];
                VoidPtr Operand2 = bufPtr[1];
                VoidPtr Result = bufPtr[2];

                npy_intp O1_Step = steps[0];
                npy_intp O2_Step = steps[1];
                npy_intp R_Step = steps[2];

                if (Operand2 == null)
                {
                    Operand2 = Operand1;
                    O2_Step = O1_Step;
                }
                if (Result == null)
                {
                    Result = Operand1;
                    R_Step = O1_Step;
                }

                npy_intp O1_Offset = Operand1.data_offset;
                npy_intp O2_Offset = Operand2.data_offset;
                npy_intp R_Offset = Result.data_offset;


                T[] retArray = Result.datap as T[];
                T[] Op1Array = Operand1.datap as T[];
                T[] Op2Array = Operand2.datap as T[];

                npy_intp O1_CalculatedStep = (O1_Step / SizeOfItem);
                npy_intp O1_CalculatedOffset = (O1_Offset / SizeOfItem);

                npy_intp O2_CalculatedStep = (O2_Step / SizeOfItem);
                npy_intp O2_CalculatedOffset = (O2_Offset / SizeOfItem);

                npy_intp R_CalculatedStep = (R_Step / SizeOfItem);
                npy_intp R_CalculatedOffset = (R_Offset / SizeOfItem);

                var UFuncOperation = GetUFuncOperation(ops);
                if (UFuncOperation == null)
                {
                    throw new Exception(string.Format("UFunc op:{0} is not implemented", ops.ToString()));
                }

                for (int i = 0; i < N; i++)
                {
                    npy_intp O1_Index = ((i * O1_CalculatedStep) + O1_CalculatedOffset);
                    npy_intp O2_Index = ((i * O2_CalculatedStep) + O2_CalculatedOffset);
                    npy_intp R_Index = ((i * R_CalculatedStep) + R_CalculatedOffset);

                    var O1Value = Op1Array[O1_Index];                                            // get operand 1
                    var O2Value = Op2Array[O2_Index];                                            // get operand 2
         
                    retArray[R_Index] = UFuncOperation(O1Value, O2Value);
                }


            }

            #endregion

            #region REDUCEAT

            public void PerformReduceAtOpArrayIter(VoidPtr[] bufPtr, npy_intp[] steps, UFuncOperation ops, npy_intp N)
            {
                PerformAccumulateOpArrayIter(bufPtr, steps, ops, N);
            }

            #endregion


            protected int CalculateIterationArraySize(NpyArray Array, NpyArray destArray)
            {
                var OperIter = NpyArray_BroadcastToShape(Array, destArray.dimensions, destArray.nd);
                return NpyArray_ITER_COUNT(OperIter);
            }

            protected npy_intp AdjustNegativeIndex(T[] data, npy_intp index)
            {
                if (index < 0)
                {
                    index = data.Length - Math.Abs(index);
                }
                return index;
            }

            protected opFunction GetUFuncOperation(UFuncOperation ops)
            {
                switch (ops)
                {
                    case UFuncOperation.add:
                        return Add;

                    case UFuncOperation.subtract:
                        return Subtract;

                    case UFuncOperation.multiply:
                        return Multiply;

                    case UFuncOperation.divide:
                        return Divide;

                    case UFuncOperation.remainder:
                        return Remainder;

                    case UFuncOperation.fmod:
                        return FMod;

                    case UFuncOperation.power:
                        return Power;

                    case UFuncOperation.square:
                        return Square;

                    case UFuncOperation.reciprocal:
                        return Reciprocal;

                    case UFuncOperation.ones_like:
                        return OnesLike;

                    case UFuncOperation.sqrt:
                        return Sqrt;

                    case UFuncOperation.negative:
                        return Negative;

                    case UFuncOperation.absolute:
                        return Absolute;

                    case UFuncOperation.invert:
                        return Invert;

                    case UFuncOperation.left_shift:
                        return LeftShift;

                    case UFuncOperation.right_shift:
                        return RightShift;

                    case UFuncOperation.bitwise_and:
                        return BitWiseAnd;

                    case UFuncOperation.bitwise_xor:
                        return BitWiseXor;

                    case UFuncOperation.bitwise_or:
                        return BitWiseOr;

                    case UFuncOperation.less:
                        return Less;

                    case UFuncOperation.less_equal:
                        return LessEqual;

                    case UFuncOperation.equal:
                        return Equal;

                    case UFuncOperation.not_equal:
                        return NotEqual;

                    case UFuncOperation.greater:
                        return Greater;

                    case UFuncOperation.greater_equal:
                        return GreaterEqual;

                    case UFuncOperation.floor_divide:
                        return FloorDivide;

                    case UFuncOperation.true_divide:
                        return TrueDivide;

                    case UFuncOperation.logical_or:
                        return LogicalOr;

                    case UFuncOperation.logical_and:
                        return LogicalAnd;

                    case UFuncOperation.floor:
                        return Floor;

                    case UFuncOperation.ceil:
                        return Ceiling;

                    case UFuncOperation.maximum:
                        return Maximum;

                    case UFuncOperation.minimum:
                        return Minimum;

                    case UFuncOperation.rint:
                        return Rint;

                    case UFuncOperation.conjugate:
                        return Conjugate;

                    case UFuncOperation.isnan:
                        return IsNAN;

                    case UFuncOperation.fmax:
                        return FMax;

                    case UFuncOperation.fmin:
                        return FMin;

                    case UFuncOperation.heaviside:
                        return Heaviside;

                }

                return null;
            }

            protected delegate T opFunction(T o1, T o2);

            protected abstract T Add(T o1, T o2);
            protected abstract T Subtract(T o1, T o2);
            protected abstract T Multiply(T o1, T o2);
            protected abstract T Divide(T o1, T o2);
            protected abstract T Power(T o1, T o2);
            protected abstract T Remainder(T o1, T o2);
            protected abstract T FMod(T o1, T o2);
            protected abstract T Square(T o1, T o2);
            protected abstract T Reciprocal(T o1, T o2);
            protected abstract T OnesLike(T o1, T o2);
            protected abstract T Sqrt(T o1, T o2);
            protected abstract T Negative(T o1, T o2);
            protected abstract T Absolute(T o1, T o2);
            protected abstract T Invert(T o1, T o2);
            protected abstract T LeftShift(T o1, T o2);
            protected abstract T RightShift(T o1, T o2);
            protected abstract T BitWiseAnd(T o1, T o2);
            protected abstract T BitWiseXor(T o1, T o2);
            protected abstract T BitWiseOr(T o1, T o2);
            protected abstract T Less(T o1, T o2);
            protected abstract T LessEqual(T o1, T o2);
            protected abstract T Equal(T o1, T o2);
            protected abstract T NotEqual(T o1, T o2);
            protected abstract T Greater(T o1, T o2);
            protected abstract T GreaterEqual(T o1, T o2);
            protected abstract T FloorDivide(T o1, T o2);
            protected abstract T TrueDivide(T o1, T o2);
            protected abstract T LogicalOr(T o1, T o2);
            protected abstract T LogicalAnd(T o1, T o2);
            protected abstract T Floor(T o1, T o2);
            protected abstract T Ceiling(T o1, T o2);
            protected abstract T Maximum(T o1, T o2);
            protected abstract T Minimum(T o1, T o2);
            protected abstract T Rint(T o1, T o2);
            protected abstract T Conjugate(T o1, T o2);
            protected abstract T IsNAN(T o1, T o2);
            protected abstract T FMax(T o1, T o2);
            protected abstract T FMin(T o1, T o2);
            protected abstract T Heaviside(T o1, T o2);

            protected abstract T PerformUFuncOperation(UFuncOperation op, T o1, T o2);

            protected abstract T ConvertToTemplate(object v);


        }




    }
}
