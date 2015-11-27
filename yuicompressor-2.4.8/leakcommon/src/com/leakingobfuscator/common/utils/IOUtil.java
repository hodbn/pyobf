package com.leakingobfuscator.common.utils;

import java.io.*;

public class IOUtil {

    private static final int BUF_SIZE = 16384;

    public static byte[] readAllBytes(InputStream is) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        copy(is, baos);

        return baos.toByteArray();
    }

    public static void writeAllBytes(OutputStream os, byte[] data) throws IOException {
        os.write(data, 0, data.length);
    }

    public static void copy(InputStream is, OutputStream os) throws IOException {
        byte[] buf = new byte[BUF_SIZE];
        int bytesRead;

        while ((bytesRead = is.read(buf, 0, buf.length)) >= 0) {
            os.write(buf, 0, bytesRead);
        }
    }

    public static void copy(Reader in, Writer out) throws IOException {
        char[] buf = new char[BUF_SIZE];
        int bytesRead;

        while ((bytesRead = in.read(buf, 0, buf.length)) >= 0) {
            out.write(buf, 0, bytesRead);
        }
    }

}
