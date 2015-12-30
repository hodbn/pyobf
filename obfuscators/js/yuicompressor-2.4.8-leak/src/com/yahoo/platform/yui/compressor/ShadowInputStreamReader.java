package com.yahoo.platform.yui.compressor;

import java.io.*;
import java.nio.ByteBuffer;

public class ShadowInputStreamReader extends InputStreamReader {

    StringBuilder sb = new StringBuilder();

    public ShadowInputStreamReader(InputStream in, String charsetName) throws UnsupportedEncodingException {
        super(in, charsetName);
    }

    public byte[] getShadow() {
        return sb.toString().getBytes();
    }

    public int read() throws IOException {
        int b = super.read();
        if (b != -1) {
            sb.append((char) b);
        }

        return b;
    }

    @Override
    public int read(char[] cbuf) throws IOException {
        int n = super.read(cbuf);
        if (n > 0) {
            sb.append(cbuf, 0, n);
        }

        return n;
    }

    @Override
    public int read(char[] cbuf, int offset, int length) throws IOException {
        int n = super.read(cbuf, offset, length);
        if (n > 0) {
            sb.append(cbuf, offset, n);
        }

        return n;
    }
}
