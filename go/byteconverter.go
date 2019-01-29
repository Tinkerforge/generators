package internal

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

func Min(left, right int64) int64 {
	if left < right {
		return left
	}
	return right
}

func MinU(left, right uint64) uint64 {
	if left < right {
		return left
	}
	return right
}

func BoolSliceToByteSlice(b []bool) []byte {
	result := make([]byte, len(b)/8)
	for i := range result {
		for bit := 0; bit < 8; bit++ {
			if b[i*8+bit] {
				result[i] |= 1 << uint(bit)
			}
		}
	}
	return result
}

func ByteSliceToBoolSlice(b []byte) []bool {
	result := make([]bool, len(b)*8)
	for i := range result {
		result[i] = b[i/8]&(1<<uint(i%8)) != 0
	}
	return result
}

func FixedSliceToByteSlice(slice []interface{}) []byte {
	var buf bytes.Buffer
	for _, item := range slice {
		binary.Write(&buf, binary.LittleEndian, item)
	}
	return buf.Bytes()
}

func ByteSliceToInt8Slice(slice []byte) []int8 {
	buf := bytes.NewBuffer(slice)
	result := make([]int8, len(slice))
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToUint8Slice(slice []byte) []uint8 {
	buf := bytes.NewBuffer(slice)
	result := make([]uint8, len(slice))
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func Uint8SliceToByteSlice(slice []uint8) []byte {
	var buf bytes.Buffer
	binary.Write(&buf, binary.LittleEndian, slice)
	return buf.Bytes()
}

func Uint64SliceToByteSlice(slice []uint64) []byte {
	var buf bytes.Buffer
	binary.Write(&buf, binary.LittleEndian, slice)
	return buf.Bytes()
}

func Uint16SliceToByteSlice(slice []uint16) []byte {
	var buf bytes.Buffer
	binary.Write(&buf, binary.LittleEndian, slice)
	return buf.Bytes()
}

func Int8SliceToByteSlice(slice []int8) []byte {
	var buf bytes.Buffer
	binary.Write(&buf, binary.LittleEndian, slice)
	return buf.Bytes()
}

func ByteSliceToInt16Slice(slice []byte) []int16 {
	buf := bytes.NewBuffer(slice)
	result := make([]int16, len(slice)/2)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToUint16Slice(slice []byte) []uint16 {
	buf := bytes.NewBuffer(slice)
	result := make([]uint16, len(slice)/2)
	err := binary.Read(buf, binary.LittleEndian, result)
	if err != nil {
		panic(err)
	}
	return result
}

func ByteSliceToInt32Slice(slice []byte) []int32 {
	buf := bytes.NewBuffer(slice)
	result := make([]int32, len(slice)/4)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToUint32Slice(slice []byte) []uint32 {
	buf := bytes.NewBuffer(slice)
	result := make([]uint32, len(slice)/4)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToInt64Slice(slice []byte) []int64 {
	buf := bytes.NewBuffer(slice)
	result := make([]int64, len(slice)/8)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToUint64Slice(slice []byte) []uint64 {
	buf := bytes.NewBuffer(slice)
	result := make([]uint64, len(slice)/8)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToFloat32Slice(slice []byte) []float32 {
	buf := bytes.NewBuffer(slice)
	result := make([]float32, len(slice)/4)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToFloat64Slice(slice []byte) []float64 {
	buf := bytes.NewBuffer(slice)
	result := make([]float64, len(slice)/8)
	binary.Read(buf, binary.LittleEndian, result[:])
	return result
}

func ByteSliceToRuneSlice(slice []byte) []rune {
	result := make([]rune, len(slice))
	for idx, b := range slice {
		result[idx] = rune(b)
	}
	return result
}

func RuneSliceToByteSlice(slice []rune) []byte {
	result := make([]byte, len(slice))
	for idx, b := range slice {
		result[idx] = byte(b)
	}
	return result
}

func ByteSliceToString(slice []byte) string {
	result := make([]rune, len(slice))

	last := 0
	for i, b := range slice {
		if b == 0 {
			continue
		}
		last = i
		result[i] = rune(b)
	}

	return string(result[:last])
}

func StringToByteSlice(str string, maxLen uint64) ([]byte, error) {
	runes := []rune(str)
	bytes := make([]byte, maxLen, maxLen)

	if uint64(len(runes)) > maxLen {
		return nil, fmt.Errorf("invalid parameter: string was %d runes long, but only %d are allowed", len(runes), maxLen)
	}

	for i, r := range runes {
		if int32(r) > 255 {
			return nil, fmt.Errorf("Invalid parameter: rune %c can not be encoded, as it is longer than one byte", r)
		}

		bytes[i] = byte(r)
	}
	return bytes, nil
}
