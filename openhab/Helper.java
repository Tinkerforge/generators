package com.tinkerforge;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;

public class Helper {


    public static short parseDisplayCommandLine(String cmd, Logger logger) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            logger.warn("Could not parse display command {}: Could not split into line, position and text. Format is [LINE],[POSITION],[TEXT].", cmd);
            return 0;
        }

        try {
            return Short.parseShort(splt[0]);
        } catch (NumberFormatException e) {
            logger.warn("Could not parse display command {}: Line {} could not be parsed as short", cmd, splt[0]);
        }
        return 0;
    }

    public static short parseDisplayCommandPosition(String cmd, Logger logger) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            // No need to log an error here, parseDisplayCommandLine will already have complained about this.
            return 0;
        }
        try {
            return Short.parseShort(splt[1]);
        } catch (NumberFormatException e) {
            logger.warn("Could not parse display command {}: Position {} could not be parsed as short", cmd, splt[1]);
        }
        return 0;
    }


    public static String parseDisplayCommandText(String cmd, Logger logger) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            // No need to log an error here, parseDisplayCommandLine will already have complained about this.
            return "";
        }
        cmd = splt[2];

        String copy = cmd;
        StringBuilder result = new StringBuilder();

        int backslash_idx = cmd.indexOf("\\");

        while(backslash_idx >= 0) {
            result.append(cmd.substring(0, backslash_idx));
            cmd = cmd.substring(backslash_idx + 1);

            if(cmd.isEmpty()) {
                logger.warn("Could not parse display command {}: Found \\ as last character.", copy);
                break;
            }

            switch(cmd.charAt(0)) {
                case 'x':
                    cmd = cmd.substring(1);
                    if(cmd.length() < 2) {
                        logger.warn("Could not parse display command {}: Found hex command \\x{} with character code of wrong length {} (expected: 2).", copy, cmd, cmd.length());
                        break;
                    }
                    String char_code = cmd.substring(0, 2);

                    cmd = cmd.substring(2);
                    try {
                        result.append(Character.toString((char)Integer.parseInt(char_code, 16)));
                    }
                    catch (NumberFormatException e) {
                        logger.warn("Could not parse display command {}: Found hex command that could not be parsed as hexadecimal number:{}", copy, e.getMessage());
                    }
                    break;
                default:
                    logger.warn("Could not parse display command {}: Found unknown command \\{}.", copy, cmd.charAt(0));
                    break;
            }

            backslash_idx = cmd.indexOf("\\");
        }
        result.append(cmd);

        return utf16ToKS0066U(result.toString());
    }

    public static String utf16ToKS0066U(String utf16)
    {
        String ks0066u = "";
        char c;

        for (int i = 0; i < utf16.length(); i++) {
            int codePoint = utf16.codePointAt(i);

            if (Character.isHighSurrogate(utf16.charAt(i))) {
                // Skip low surrogate
                i++;
            }

            // ASCII subset from JIS X 0201
            if (codePoint >= 0x0020 && codePoint <= 0x007e) {
                // The LCD charset doesn't include '\' and '~', use similar characters instead
                switch (codePoint) {
                case 0x005c: c = (char)0xa4; break; // REVERSE SOLIDUS maps to IDEOGRAPHIC COMMA
                case 0x007e: c = (char)0x2d; break; // TILDE maps to HYPHEN-MINUS
                default: c = (char)codePoint; break;
                }
            }
            // Katakana subset from JIS X 0201
            else if (codePoint >= 0xff61 && codePoint <= 0xff9f) {
                c = (char)(codePoint - 0xfec0);
            }
            // Special characters
            else {
                switch (codePoint) {
                case 0x00a5: c = (char)0x5c; break; // YEN SIGN
                case 0x2192: c = (char)0x7e; break; // RIGHTWARDS ARROW
                case 0x2190: c = (char)0x7f; break; // LEFTWARDS ARROW
                case 0x00b0: c = (char)0xdf; break; // DEGREE SIGN maps to KATAKANA SEMI-VOICED SOUND MARK
                case 0x03b1: c = (char)0xe0; break; // GREEK SMALL LETTER ALPHA
                case 0x00c4: c = (char)0xe1; break; // LATIN CAPITAL LETTER A WITH DIAERESIS
                case 0x00e4: c = (char)0xe1; break; // LATIN SMALL LETTER A WITH DIAERESIS
                case 0x00df: c = (char)0xe2; break; // LATIN SMALL LETTER SHARP S
                case 0x03b5: c = (char)0xe3; break; // GREEK SMALL LETTER EPSILON
                case 0x00b5: c = (char)0xe4; break; // MICRO SIGN
                case 0x03bc: c = (char)0xe4; break; // GREEK SMALL LETTER MU
                case 0x03c2: c = (char)0xe5; break; // GREEK SMALL LETTER FINAL SIGMA
                case 0x03c1: c = (char)0xe6; break; // GREEK SMALL LETTER RHO
                case 0x221a: c = (char)0xe8; break; // SQUARE ROOT
                case 0x00b9: c = (char)0xe9; break; // SUPERSCRIPT ONE maps to SUPERSCRIPT (minus) ONE
                case 0x00a4: c = (char)0xeb; break; // CURRENCY SIGN
                case 0x00a2: c = (char)0xec; break; // CENT SIGN
                case 0x2c60: c = (char)0xed; break; // LATIN CAPITAL LETTER L WITH DOUBLE BAR
                case 0x00f1: c = (char)0xee; break; // LATIN SMALL LETTER N WITH TILDE
                case 0x00d6: c = (char)0xef; break; // LATIN CAPITAL LETTER O WITH DIAERESIS
                case 0x00f6: c = (char)0xef; break; // LATIN SMALL LETTER O WITH DIAERESIS
                case 0x03f4: c = (char)0xf2; break; // GREEK CAPITAL THETA SYMBOL
                case 0x221e: c = (char)0xf3; break; // INFINITY
                case 0x03a9: c = (char)0xf4; break; // GREEK CAPITAL LETTER OMEGA
                case 0x00dc: c = (char)0xf5; break; // LATIN CAPITAL LETTER U WITH DIAERESIS
                case 0x00fc: c = (char)0xf5; break; // LATIN SMALL LETTER U WITH DIAERESIS
                case 0x03a3: c = (char)0xf6; break; // GREEK CAPITAL LETTER SIGMA
                case 0x03c0: c = (char)0xf7; break; // GREEK SMALL LETTER PI
                case 0x0304: c = (char)0xf8; break; // COMBINING MACRON
                case 0x00f7: c = (char)0xfd; break; // DIVISION SIGN

                case 0x0008: c = (char)0x08; break; // CUSTOM CHARACTER 1
                case 0x0009: c = (char)0x09; break; // CUSTOM CHARACTER 2
                case 0x000A: c = (char)0x0A; break; // CUSTOM CHARACTER 3
                case 0x000B: c = (char)0x0B; break; // CUSTOM CHARACTER 4
                case 0x000C: c = (char)0x0C; break; // CUSTOM CHARACTER 5
                case 0x000D: c = (char)0x0D; break; // CUSTOM CHARACTER 6
                case 0x000E: c = (char)0x0E; break; // CUSTOM CHARACTER 7
                case 0x000F: c = (char)0x0F; break; // CUSTOM CHARACTER 8

                default:
                case 0x25a0: c = codePoint > 0xff ? (char)0xff : (char)codePoint; break; // BLACK SQUARE
                }
            }

            // Special handling for 'x' followed by COMBINING MACRON
            if (c == (char)0xf8) {
                if (!ks0066u.endsWith("x")) {
                    c = (char)0xff; // BLACK SQUARE
                }

                if (ks0066u.length() > 0) {
                    ks0066u = ks0066u.substring(0, ks0066u.length() - 1);
                }
            }

            ks0066u += c;
        }

        return ks0066u;
    }

	public static int parseLEDValueIndex(String string, Logger logger) {
		try {
            return Integer.valueOf(string.split(",")[0]);
        } catch (Exception e) {
            logger.warn("Could not parse LED Value command: {}", e.getMessage());
            return 0;
        }
	}

	public static int[] parseLEDValues(String string, Logger logger) {
		try {
            return Arrays.stream(string.split(",")).skip(1).mapToInt(Integer::valueOf).toArray();
        } catch (Exception e) {
            logger.warn("Could not parse LED Value command: {}", e.getMessage());
            return new int[]{};
        }
	}

    public static short parseLED1ValueLength(String string, boolean usesFourChannels, Logger logger) {
        int elements = (int)string.chars().filter(c -> c == ',').count(); // there should be a + 1 here, but the first element is the index, which must not be counted.
        int result = elements / (usesFourChannels ? 4 : 3);

        short maxControllableLEDs = (short) (usesFourChannels ? 12 : 16);
        if(result > maxControllableLEDs) {
            logger.warn("Could not parse LED Value command: A maximum of {} LEDs can be set with one command, but got {}.", maxControllableLEDs, result);
            return 0;
        }

        return (short)result;
    }

    public static short[] parseLED1Values(String string, int channel, boolean usesFourChannels, Logger logger)
    {
        try {
            String[] splt = string.split(",");
            short[] result = new short[usesFourChannels ? 12 : 16];
            int nextInsert = 0;

            for (int i = 1 + channel; i < splt.length; i += (usesFourChannels ? 4 : 3)) {
                result[nextInsert] = Short.valueOf(splt[i]);
            }
            return result;
        } catch (Exception e) {
            logger.warn("Could not parse LED Value command: {}", e.getMessage());
            return new short[]{};
        }
    }

    public static ZonedDateTime parseGPSDateTime(long date, long time) {
        int year = 2000 + (int)date % 100;
        date /= 100;
        int month = (int)date % 100;
        date /= 100;
        int day = (int)date;

        int millisecond = (int)time % 1000;
        time /= 1000;
        int second = (int)time % 100;
        time /= 100;
        int minute = (int)time % 100;
        time /= 100;
        int hour = (int)time;
        try {
            return ZonedDateTime.of(year, month, day, hour, minute, second, millisecond * 1000 * 1000, ZoneId.of("UTC"));
        }
        catch(Exception e) {
            return ZonedDateTime.now();
        }
    }

    public static boolean[] shortToBits(short s) {
        boolean[] result = new boolean[8];
        for (int i = 0; i < 8; ++i) {
            result[i] = (s & (1 << (i))) != 0;
        }
        return result;
    }

    private static short translateCharacter(char c) {
        short[] digits = {
            0x3f,0x06,0x5b,0x4f,0x66, //0-4
            0x6d,0x7d,0x07,0x7f,0x6f  //5-9
        };
        short[] capitals = {
            0x77,0x7f,0x39,0x3f,0x79,0x71, //A-F
            0x7d,0x76,0x30,0x0E,0x76,0x38, //G-L
            0x15,0x15,0x3F,0x73,0x67,0x77, //M-R
            0x6d,0x31,0x3e,0x3e,0x2a,0x76, //S-X
            0x66,0x5b,                     //Y-Z
        };
        short[] minuscules = {
            0x5c,0x7c,0x58,0x5e,0x7B,0x71, //a-f
            0x6f,0x74,0x10,0x0C,0x76,0x18, //g-l
            0x15,0x54,0x63,0x73,0x67,0x50, //m-r
            0x6d,0x78,0x1c,0x62,0x2a,0x76, //s-x
            0x6E,0x5b,                     //y-z
        };
        Map<Character, Short> special_characters = new HashMap<>();
        special_characters.put((char)'"', (short)0x22);
        special_characters.put((char)'(', (short)0x39);
        special_characters.put((char)')', (short)0x0F);
        special_characters.put((char)'+', (short)0x70);
        special_characters.put((char)'-', (short)0x40);
        special_characters.put((char)'=', (short)0x09);
        special_characters.put((char)'[', (short)0x39);
        special_characters.put((char)']', (short)0x0F);
        special_characters.put((char)'^', (short)0x23);
        special_characters.put((char)'_', (short)0x08);
        special_characters.put((char)'|', (short)0x06);

        short digit = 0;
        if (c >= 48 && c <= 57) {
            digit = digits[c - 48];
        } else if (c >= 65 && c <= 90) {
            digit = capitals[c - 65];
        } else if (c >= 97 && c <= 122) {
            digit = minuscules[c - 97];
        } else {
            digit = special_characters.getOrDefault(c, (short)0);
        }

        return digit;
    }

    public static long bitsToLong(boolean[] bits) {
        long result = 0;
        for(int i = 0; i < bits.length; ++i) {
            if (bits[i]) {
                result |= (1 << i);
            }
        }
        return result;
    }

    public static boolean[] parseSegmentDisplay2TextDigit(String string, int digit) {
        boolean[][] result = new boolean[4][8];

        int seenDigits = 0;

        for (int i = 0; i < string.length(); ++i) {
            char c = string.charAt(i);
            short s = translateCharacter(c);
            if (s != 0 && seenDigits < 4) {
                result[seenDigits] = shortToBits(s);
                ++seenDigits;
            }
            if(seenDigits > 0 && c == '.') {
                result[seenDigits - 1][7] = true;
            }
        }

        return result[digit];
    }

    public static short[] parseSegmentDisplayText(String string) {
        String copy = string.replace(":", "");
        short[] result = new short[4];
        for (int i = 0; i < Math.min(copy.length(), 4); ++i) {
            result[i] = translateCharacter(copy.charAt(i));
        }
        return result;
    }
}
