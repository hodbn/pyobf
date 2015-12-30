package com.leakingobfuscator.common.utils;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.zip.GZIPInputStream;

public class GZipUtil {

    public static byte[] decompress(byte[] gzBuf) throws IOException {
        return IOUtil.readAllBytes(new GZIPInputStream(new ByteArrayInputStream(gzBuf)));
    }

}
