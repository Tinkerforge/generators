package internal

import (
	"fmt"
	"math"
	"strings"
)

const alphabet = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

func pow(base, exp uint64) uint64 {
	result := uint64(1)
	for i := uint64(0); i < exp; i++ {
		result *= base
	}
	return result
}

func Base58ToU32(str string) (uint32, error) {
	var result uint64

	radix := uint64(len(alphabet))
	var digit = uint64(0)
	for idx := range str {
		r := rune(str[len(str)-idx-1])
		i := strings.IndexRune(alphabet, r)
		if i == -1 {
			return uint32(result), fmt.Errorf("UID contained an invalid character at position: %d", idx)
		}
		//TODO: overflow check
		result += pow(radix, digit) * uint64(i)
		digit++
	}

	if result > math.MaxUint32 {
		value1 := uint32(result & 0xFFFFFFFF)
		value2 := uint32((result >> 32) & 0xFFFFFFFF)
		return (value1 & 0x00000FFF) |
			(value1&0x0F000000)>>12 |
			(value2&0x0000003F)<<16 |
			(value2&0x000F0000)<<6 |
			(value2&0x3F000000)<<2, nil
	}

	return uint32(result), nil
}
