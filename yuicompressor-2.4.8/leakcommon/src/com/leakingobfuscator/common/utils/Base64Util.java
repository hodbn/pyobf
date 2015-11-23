package com.leakingobfuscator.common.utils;

import java.util.Base64;

public class Base64Util {

    public static String encode(byte[] buf) {
        return Base64.getEncoder().encodeToString(buf);
    }

    public static byte[] decode(String b64Data) {
        return Base64.getDecoder().decode(b64Data);
    }

}
