package com.tinkerforge;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;

import org.slf4j.Logger;

public class Helper {


    public static int parseDisplayCommandLine(String cmd, Logger logger) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            logger.warn("Could not parse display command {}: Could not split into line, position and text. Format is [LINE],[POSITION],[TEXT].", cmd);
            return 0;
        }

        try {
            return Integer.parseInt(splt[0]);
        } catch (NumberFormatException e) {
            logger.warn("Could not parse display command {}: Line {} could not be parsed as int", cmd, splt[0]);
        }
        return 0;
    }

    public static int parseDisplayCommandPosition(String cmd, Logger logger) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            // No need to log an error here, parseDisplayCommandLine will already have complained about this.
            return 0;
        }
        try {
            return Integer.parseInt(splt[1]);
        } catch (NumberFormatException e) {
            logger.warn("Could not parse display command {}: Position {} could not be parsed as int", cmd, splt[1]);
        }
        return 0;
    }


    public static String parseDisplayCommandText(String cmd, Logger logger, boolean oldCharset) {
        String[] splt = cmd.toString().split(",", 3);
        if(splt.length != 3) {
            // No need to log an error here, parseDisplayCommandLine will already have complained about this.
            return "";
        }
        cmd = splt[2];

        String copy = cmd;

        if (oldCharset) {
            cmd = utf16ToKS0066U(cmd);
        } else {
            cmd = utf16ToCP437(cmd);
        }

        StringBuilder result = new StringBuilder();
        String backslash_pattern = oldCharset ? Character.toString((char)0xa4) : "\\";
        int backslash_idx = cmd.indexOf(backslash_pattern);

        while(backslash_idx >= 0) {
            result.append(cmd.substring(0, backslash_idx));
            cmd = cmd.substring(backslash_idx + 1);

            if(cmd.isEmpty()) {
                logger.warn("Could not parse display command {}: Found \\ as last character.", copy);
                break;
            }

            if (cmd.charAt(0) == 'x') {
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
            }
            else if (cmd.charAt(0) == backslash_pattern.charAt(0)) {
                cmd = cmd.substring(1);
                result.append(backslash_pattern.charAt(0));
            }
            else {
                logger.warn("Could not parse display command {}: Found unknown command \\{}.", copy, cmd.charAt(0));
            }

            backslash_idx = cmd.indexOf(backslash_pattern);
        }
        result.append(cmd);

        return result.toString();
    }

    static final List<Integer> cp437 = Arrays.asList(
        0x0000, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022,
        0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C,
        0x25BA, 0x25C4, 0x2195, 0x203C, 0x00B6, 0x00A7, 0x25AC, 0x21A8,
        0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC,
        0x0020, 0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027,
        0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F,
        0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
        0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F,
        0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047,
        0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F,
        0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057,
        0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x005F,
        0x0060, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067,
        0x0068, 0x0069, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F,
        0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077,
        0x0078, 0x0079, 0x007A, 0x007B, 0x007C, 0x007D, 0x007E, 0x2302,
        0x00C7, 0x00FC, 0x00E9, 0x00E2, 0x00E4, 0x00E0, 0x00E5, 0x00E7,
        0x00EA, 0x00EB, 0x00E8, 0x00EF, 0x00EE, 0x00EC, 0x00C4, 0x00C5,
        0x00C9, 0x00E6, 0x00C6, 0x00F4, 0x00F6, 0x00F2, 0x00FB, 0x00F9,
        0x00FF, 0x00D6, 0x00DC, 0x00A2, 0x00A3, 0x00A5, 0x20A7, 0x0192,
        0x00E1, 0x00ED, 0x00F3, 0x00FA, 0x00F1, 0x00D1, 0x00AA, 0x00BA,
        0x00BF, 0x2310, 0x00AC, 0x00BD, 0x00BC, 0x00A1, 0x00AB, 0x00BB,
        0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556,
        0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510,
        0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F,
        0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567,
        0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B,
        0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580,
        0x03B1, 0x00DF, 0x0393, 0x03C0, 0x03A3, 0x03C3, 0x00B5, 0x03C4,
        0x03A6, 0x0398, 0x03A9, 0x03B4, 0x221E, 0x03C6, 0x03B5, 0x2229,
        0x2261, 0x00B1, 0x2265, 0x2264, 0x2320, 0x2321, 0x00F7, 0x2248,
        0x00B0, 0x2219, 0x00B7, 0x221A, 0x207F, 0x00B2, 0x25A0, 0x00A0
    );

    public static String utf16ToCP437(String utf16) {
        StringBuilder result = new StringBuilder();
        utf16.codePoints().map(c -> cp437.indexOf(c)).map(i -> i == -1 ? 0xDB : i).forEach(c -> result.append((char)c));
        return result.toString();
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

    public static int parseLED1ValueLength(String string, boolean usesFourChannels, Logger logger) {
        int elements = (int)string.chars().filter(c -> c == ',').count(); // there should be a + 1 here, but the first element is the index, which must not be counted.
        int result = elements / (usesFourChannels ? 4 : 3);

        int maxControllableLEDs = (usesFourChannels ? 12 : 16);
        if(result > maxControllableLEDs) {
            logger.warn("Could not parse LED Value command: A maximum of {} LEDs can be set with one command, but got {}.", maxControllableLEDs, result);
            return 0;
        }

        return result;
    }

    public static int[] parseLED1Values(String string, int channel, boolean usesFourChannels, Logger logger)
    {
        try {
            String[] splt = string.split(",");
            int[] result = new int[usesFourChannels ? 12 : 16];
            int nextInsert = 0;

            for (int i = 1 + channel; i < splt.length; i += (usesFourChannels ? 4 : 3)) {
                result[nextInsert] = Integer.valueOf(splt[i]);
            }
            return result;
        } catch (Exception e) {
            logger.warn("Could not parse LED Value command: {}", e.getMessage());
            return new int[]{};
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

    public static boolean[] intToBits(int i) {
        boolean[] result = new boolean[8];
        for (int bit = 0; bit < 8; ++bit) {
            result[bit] = (i & (1 << (bit))) != 0;
        }
        return result;
    }

    private static int translateCharacter(char c) {
        int[] digits = {
            0x3f,0x06,0x5b,0x4f,0x66, //0-4
            0x6d,0x7d,0x07,0x7f,0x6f  //5-9
        };
        int[] capitals = {
            0x77,0x7f,0x39,0x3f,0x79,0x71, //A-F
            0x7d,0x76,0x30,0x0E,0x76,0x38, //G-L
            0x15,0x15,0x3F,0x73,0x67,0x77, //M-R
            0x6d,0x31,0x3e,0x3e,0x2a,0x76, //S-X
            0x66,0x5b,                     //Y-Z
        };
        int[] minuscules = {
            0x5c,0x7c,0x58,0x5e,0x7B,0x71, //a-f
            0x6f,0x74,0x10,0x0C,0x76,0x18, //g-l
            0x15,0x54,0x63,0x73,0x67,0x50, //m-r
            0x6d,0x78,0x1c,0x62,0x2a,0x76, //s-x
            0x6E,0x5b,                     //y-z
        };
        Map<Character, Integer> special_characters = new HashMap<>();
        special_characters.put((char)'"', 0x22);
        special_characters.put((char)'(', 0x39);
        special_characters.put((char)')', 0x0F);
        special_characters.put((char)'+', 0x70);
        special_characters.put((char)'-', 0x40);
        special_characters.put((char)'=', 0x09);
        special_characters.put((char)'[', 0x39);
        special_characters.put((char)']', 0x0F);
        special_characters.put((char)'^', 0x23);
        special_characters.put((char)'_', 0x08);
        special_characters.put((char)'|', 0x06);

        int digit = 0;
        if (c >= 48 && c <= 57) {
            digit = digits[c - 48];
        } else if (c >= 65 && c <= 90) {
            digit = capitals[c - 65];
        } else if (c >= 97 && c <= 122) {
            digit = minuscules[c - 97];
        } else {
            digit = special_characters.getOrDefault(c, 0);
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
            int s = translateCharacter(c);
            if (s != 0 && seenDigits < 4) {
                result[seenDigits] = intToBits(s);
                ++seenDigits;
            }
            if(seenDigits > 0 && c == '.') {
                result[seenDigits - 1][7] = true;
            }
        }

        return result[digit];
    }

    public static int[] parseSegmentDisplayText(String string) {
        String copy = string.replace(":", "");
        int[] result = new int[4];
        for (int i = 0; i < Math.min(copy.length(), 4); ++i) {
            result[i] = translateCharacter(copy.charAt(i));
        }
        return result;
    }

    public static String getDeviceName(int deviceID) {
        return DeviceFactory.getDeviceInfo(deviceID).deviceDisplayName;
    }

    private static final int[] thermalColorStandard = new int[] {
        0xff000000,0xff100006,0xff17000d,0xff1c0013,0xff200019,0xff24001f,0xff270026,0xff2a002c,
        0xff2d0032,0xff300038,0xff32003e,0xff350044,0xff37004a,0xff3a0050,0xff3c0056,0xff3e005c,
        0xff400062,0xff420068,0xff44006d,0xff460073,0xff470079,0xff49007e,0xff4b0084,0xff4d0089,
        0xff4e008e,0xff500093,0xff510098,0xff53009d,0xff5400a2,0xff5600a7,0xff5700ac,0xff5900b0,
        0xff5a01b5,0xff5c01b9,0xff5d01be,0xff5e01c2,0xff6001c6,0xff6101ca,0xff6201cd,0xff6401d1,
        0xff6501d5,0xff6601d8,0xff6701db,0xff6901de,0xff6a01e1,0xff6b01e4,0xff6c01e7,0xff6d02ea,
        0xff6f02ec,0xff7002ee,0xff7102f1,0xff7202f3,0xff7302f4,0xff7402f6,0xff7502f8,0xff7603f9,
        0xff7703fa,0xff7903fb,0xff7a03fc,0xff7b03fd,0xff7c03fe,0xff7d03fe,0xff7e04ff,0xff7f04ff,
        0xff8004ff,0xff8104ff,0xff8204ff,0xff8305fe,0xff8405fe,0xff8505fd,0xff8605fc,0xff8706fb,
        0xff8706fa,0xff8806f8,0xff8906f7,0xff8a06f5,0xff8b07f3,0xff8c07f2,0xff8d07ef,0xff8e08ed,
        0xff8f08eb,0xff9008e8,0xff9108e6,0xff9109e3,0xff9209e0,0xff9309dd,0xff940ada,0xff950ad6,
        0xff960ad3,0xff970bcf,0xff970bcb,0xff980cc8,0xff990cc4,0xff9a0cc0,0xff9b0dbb,0xff9c0db7,
        0xff9c0eb3,0xff9d0eae,0xff9e0ea9,0xff9f0fa5,0xffa00fa0,0xffa0109b,0xffa11096,0xffa21191,
        0xffa3118c,0xffa41286,0xffa41281,0xffa5137b,0xffa61376,0xffa71470,0xffa7146b,0xffa81565,
        0xffa9165f,0xffaa1659,0xffaa1753,0xffab174d,0xffac1847,0xffad1941,0xffad193b,0xffae1a35,
        0xffaf1b2f,0xffb01b29,0xffb01c22,0xffb11d1c,0xffb21d16,0xffb31e10,0xffb31f09,0xffb42003,
        0xffb52000,0xffb52100,0xffb62200,0xffb72300,0xffb72300,0xffb82400,0xffb92500,0xffba2600,
        0xffba2700,0xffbb2800,0xffbc2800,0xffbc2900,0xffbd2a00,0xffbe2b00,0xffbe2c00,0xffbf2d00,
        0xffc02e00,0xffc02f00,0xffc13000,0xffc23100,0xffc23200,0xffc33300,0xffc43400,0xffc43500,
        0xffc53600,0xffc63700,0xffc63800,0xffc73900,0xffc73a00,0xffc83c00,0xffc93d00,0xffc93e00,
        0xffca3f00,0xffcb4000,0xffcb4100,0xffcc4300,0xffcc4400,0xffcd4500,0xffce4600,0xffce4800,
        0xffcf4900,0xffd04a00,0xffd04c00,0xffd14d00,0xffd14e00,0xffd25000,0xffd35100,0xffd35200,
        0xffd45400,0xffd45500,0xffd55700,0xffd65800,0xffd65a00,0xffd75b00,0xffd75d00,0xffd85e00,
        0xffd96000,0xffd96100,0xffda6300,0xffda6500,0xffdb6600,0xffdc6800,0xffdc6900,0xffdd6b00,
        0xffdd6d00,0xffde6f00,0xffde7000,0xffdf7200,0xffe07400,0xffe07600,0xffe17700,0xffe17900,
        0xffe27b00,0xffe27d00,0xffe37f00,0xffe48100,0xffe48300,0xffe58400,0xffe58600,0xffe68800,
        0xffe68a00,0xffe78c00,0xffe78e00,0xffe89000,0xffe99300,0xffe99500,0xffea9700,0xffea9900,
        0xffeb9b00,0xffeb9d00,0xffec9f00,0xffeca200,0xffeda400,0xffeda600,0xffeea800,0xffeeab00,
        0xffefad00,0xfff0af00,0xfff0b200,0xfff1b400,0xfff1b600,0xfff2b900,0xfff2bb00,0xfff3be00,
        0xfff3c000,0xfff4c300,0xfff4c500,0xfff5c800,0xfff5ca00,0xfff6cd00,0xfff6cf00,0xfff7d200,
        0xfff7d500,0xfff8d700,0xfff8da00,0xfff9dd00,0xfff9df00,0xfffae200,0xfffae500,0xfffbe800,
        0xfffbeb00,0xfffced00,0xfffcf000,0xfffdf300,0xfffdf600,0xfffef900,0xfffefc00,0xffffff00,
    };

    private static final int[] thermalColorGreyscale = new int[] {
        0xff000000,0xff010101,0xff020202,0xff030303,0xff040404,0xff050505,0xff060606,0xff070707,
        0xff080808,0xff090909,0xff0a0a0a,0xff0b0b0b,0xff0c0c0c,0xff0d0d0d,0xff0e0e0e,0xff0f0f0f,
        0xff101010,0xff111111,0xff121212,0xff131313,0xff141414,0xff151515,0xff161616,0xff171717,
        0xff181818,0xff191919,0xff1a1a1a,0xff1b1b1b,0xff1c1c1c,0xff1d1d1d,0xff1e1e1e,0xff1f1f1f,
        0xff202020,0xff212121,0xff222222,0xff232323,0xff242424,0xff252525,0xff262626,0xff272727,
        0xff282828,0xff292929,0xff2a2a2a,0xff2b2b2b,0xff2c2c2c,0xff2d2d2d,0xff2e2e2e,0xff2f2f2f,
        0xff303030,0xff313131,0xff323232,0xff333333,0xff343434,0xff353535,0xff363636,0xff373737,
        0xff383838,0xff393939,0xff3a3a3a,0xff3b3b3b,0xff3c3c3c,0xff3d3d3d,0xff3e3e3e,0xff3f3f3f,
        0xff404040,0xff414141,0xff424242,0xff434343,0xff444444,0xff454545,0xff464646,0xff474747,
        0xff484848,0xff494949,0xff4a4a4a,0xff4b4b4b,0xff4c4c4c,0xff4d4d4d,0xff4e4e4e,0xff4f4f4f,
        0xff505050,0xff515151,0xff525252,0xff535353,0xff545454,0xff555555,0xff565656,0xff575757,
        0xff585858,0xff595959,0xff5a5a5a,0xff5b5b5b,0xff5c5c5c,0xff5d5d5d,0xff5e5e5e,0xff5f5f5f,
        0xff606060,0xff616161,0xff626262,0xff636363,0xff646464,0xff656565,0xff666666,0xff676767,
        0xff686868,0xff696969,0xff6a6a6a,0xff6b6b6b,0xff6c6c6c,0xff6d6d6d,0xff6e6e6e,0xff6f6f6f,
        0xff707070,0xff717171,0xff727272,0xff737373,0xff747474,0xff757575,0xff767676,0xff777777,
        0xff787878,0xff797979,0xff7a7a7a,0xff7b7b7b,0xff7c7c7c,0xff7d7d7d,0xff7e7e7e,0xff7f7f7f,
        0xff808080,0xff818181,0xff828282,0xff838383,0xff848484,0xff858585,0xff868686,0xff878787,
        0xff888888,0xff898989,0xff8a8a8a,0xff8b8b8b,0xff8c8c8c,0xff8d8d8d,0xff8e8e8e,0xff8f8f8f,
        0xff909090,0xff919191,0xff929292,0xff939393,0xff949494,0xff959595,0xff969696,0xff979797,
        0xff989898,0xff999999,0xff9a9a9a,0xff9b9b9b,0xff9c9c9c,0xff9d9d9d,0xff9e9e9e,0xff9f9f9f,
        0xffa0a0a0,0xffa1a1a1,0xffa2a2a2,0xffa3a3a3,0xffa4a4a4,0xffa5a5a5,0xffa6a6a6,0xffa7a7a7,
        0xffa8a8a8,0xffa9a9a9,0xffaaaaaa,0xffababab,0xffacacac,0xffadadad,0xffaeaeae,0xffafafaf,
        0xffb0b0b0,0xffb1b1b1,0xffb2b2b2,0xffb3b3b3,0xffb4b4b4,0xffb5b5b5,0xffb6b6b6,0xffb7b7b7,
        0xffb8b8b8,0xffb9b9b9,0xffbababa,0xffbbbbbb,0xffbcbcbc,0xffbdbdbd,0xffbebebe,0xffbfbfbf,
        0xffc0c0c0,0xffc1c1c1,0xffc2c2c2,0xffc3c3c3,0xffc4c4c4,0xffc5c5c5,0xffc6c6c6,0xffc7c7c7,
        0xffc8c8c8,0xffc9c9c9,0xffcacaca,0xffcbcbcb,0xffcccccc,0xffcdcdcd,0xffcecece,0xffcfcfcf,
        0xffd0d0d0,0xffd1d1d1,0xffd2d2d2,0xffd3d3d3,0xffd4d4d4,0xffd5d5d5,0xffd6d6d6,0xffd7d7d7,
        0xffd8d8d8,0xffd9d9d9,0xffdadada,0xffdbdbdb,0xffdcdcdc,0xffdddddd,0xffdedede,0xffdfdfdf,
        0xffe0e0e0,0xffe1e1e1,0xffe2e2e2,0xffe3e3e3,0xffe4e4e4,0xffe5e5e5,0xffe6e6e6,0xffe7e7e7,
        0xffe8e8e8,0xffe9e9e9,0xffeaeaea,0xffebebeb,0xffececec,0xffededed,0xffeeeeee,0xffefefef,
        0xfff0f0f0,0xfff1f1f1,0xfff2f2f2,0xfff3f3f3,0xfff4f4f4,0xfff5f5f5,0xfff6f6f6,0xfff7f7f7,
        0xfff8f8f8,0xfff9f9f9,0xfffafafa,0xfffbfbfb,0xfffcfcfc,0xfffdfdfd,0xfffefefe,0xffffffff,
    };

    private static final int[] thermalColorHotCold = new int[] {
        0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,
        0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,
        0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,
        0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,0xff0000ff,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,0xff000000,
        0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,
        0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,
        0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,
        0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,0xffff0000,
    };


    public static byte[] convertThermalHighContrastImage(int[] pixels, int colorPalette, Logger logger) {
        BufferedImage image = new BufferedImage(80, 60, BufferedImage.TYPE_INT_ARGB);
        int[] rgbArray = new int[80 * 60];
        int[] palette;
        if (colorPalette == 0) {
            palette = thermalColorStandard;
        } else if (colorPalette == 1) {
            palette = thermalColorGreyscale;
        } else {
            palette = thermalColorHotCold;
        }
        for (int y = 0; y < 60; ++y) {
            for (int x = 0; x < 80; ++x) {
                int stride = y * 80 + x;
                int pixel = pixels[stride];
                rgbArray[stride] = palette[pixel];
            }
        }
        image.setRGB(0, 0, 80, 60, rgbArray, 0, 80);

        ByteArrayOutputStream result = new ByteArrayOutputStream();
        try {
            ImageIO.write(image, "png", result);
        } catch (IOException e) {
            logger.debug("Failed to convert thermal image to PNG: {}", e.getMessage());
        }
        return result.toByteArray();
    }

    public static byte[] convertThermalTemperatureImage(int[] pixels, int colorPalette, Logger logger) {
        int max = Arrays.stream(pixels).max().getAsInt();
        int min = Arrays.stream(pixels).min().getAsInt();
        int interval = max - min;
        int [] relative = Arrays.stream(pixels).map(i -> ((i - min) * 255) / interval).toArray();

        return convertThermalHighContrastImage(relative, colorPalette, logger);
    }

    public static int[] parseLEDMatrixValues(String command, int channel, Logger logger) {
        String[] splt = command.split(",");
        int offset = Integer.valueOf(splt[0]);
        int[] result = new int[64];

        for(int i = channel + 1; i < splt.length; i += 3) {
            result[offset + (i - 1) / 3] = Integer.valueOf(splt[i]);
        }

        return result;
    }
}
