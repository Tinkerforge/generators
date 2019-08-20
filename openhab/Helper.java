package com.tinkerforge;

public class Helper {

    public static String parseDisplayCommand(String cmd) {
        StringBuilder result = new StringBuilder();

        int backslash_idx = cmd.indexOf("\\");

        while(backslash_idx >= 0) {
            result.append(cmd.substring(0, backslash_idx));
            cmd = cmd.substring(backslash_idx + 1);
            //cmd = cmd.substring(1);

            if(cmd.isEmpty())
                break;

            switch(cmd.charAt(0)) {
                case 'x':
                    cmd = cmd.substring(1);
                    String char_code = cmd.substring(0, 2);
                    if(char_code.length() != 2)
                        break;
                    cmd = cmd.substring(2);
                    result.append(Character.toString((char)Integer.parseInt(char_code, 16)));
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
}
