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
	if len(str) == 0 {
		return 0, fmt.Errorf("UID was empty.")
	}

	var result_u64 uint64

	radix := uint64(len(alphabet))
	var digit = uint64(0)
	for idx := range strings.TrimLeft(str, "1") {
		r := rune(str[len(str)-idx-1])
		i := strings.IndexRune(alphabet, r)
		if i == -1 {
			return uint32(result_u64), fmt.Errorf("UID %s contained an invalid character at position: %d", str, idx)
		}

		pow_overflows := digit > 0 && pow(radix, digit-1) > (math.MaxUint64/radix)
		mult_overflows := math.MaxUint64/pow(radix, digit) < uint64(i)
		add_overflows := math.MaxUint64-pow(radix, digit)*uint64(i) < result_u64

		if pow_overflows || mult_overflows || add_overflows {
			return uint32(result_u64), fmt.Errorf("UID %s was too big to fit into an uint64.", str)
		}
		result_u64 += pow(radix, digit) * uint64(i)
		digit++
	}

	var result uint32
	if result_u64 > math.MaxUint32 {
		value1 := uint32(result_u64 & 0xFFFFFFFF)
		value2 := uint32((result_u64 >> 32) & 0xFFFFFFFF)
		result = (value1 & 0x00000FFF) |
			(value1&0x0F000000)>>12 |
			(value2&0x0000003F)<<16 |
			(value2&0x000F0000)<<6 |
			(value2&0x3F000000)<<2
	} else {
		result = uint32(result_u64)
	}

	if result == 0 {
		return result, fmt.Errorf("UID was empty or mapped to zero.")
	}

	return result, nil
}
