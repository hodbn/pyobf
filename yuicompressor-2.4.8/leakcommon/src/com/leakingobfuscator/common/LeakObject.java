package com.leakingobfuscator.common;

import com.leakingobfuscator.common.utils.Base64Util;
import org.json.*;

import java.io.StringWriter;

public class LeakObject {

    public static final String KEY_ENC_SOURCE_CODE = "encSourceCode";
    public static final String KEY_WRAPPED_KEY = "wrappedKey";
    public static final String KEY_ENC_IV = "encIV";

    private byte[] encSourceCode;
    private byte[] wrappedKey;
    private byte[] encIV;

    public LeakObject(byte[] encSourceCode, byte[] wrappedKey, byte[] encIV) {
        this.encSourceCode = encSourceCode;
        this.wrappedKey = wrappedKey;
        this.encIV = encIV;
    }

    public byte[] getEncSourceCode() {
        return encSourceCode;
    }

    public byte[] getWrappedKey() {
        return wrappedKey;
    }

    public byte[] getEncIV() {
        return encIV;
    }

    public static LeakObject fromJSON(String jsonStr) {
        JSONObject rootObj = new JSONObject(jsonStr);

        return new LeakObject(
                Base64Util.decode(rootObj.getString(KEY_ENC_SOURCE_CODE)),
                Base64Util.decode(rootObj.getString(KEY_WRAPPED_KEY)),
                Base64Util.decode(rootObj.getString(KEY_ENC_IV))
        );
    }

    public String toJSON() {
        StringWriter sw = new StringWriter();
        new JSONWriter(sw)
                .object()
                    .key(KEY_ENC_SOURCE_CODE)
                    .value(Base64Util.encode(encSourceCode))
                    .key(KEY_WRAPPED_KEY)
                    .value(Base64Util.encode(wrappedKey))
                    .key(KEY_ENC_IV)
                    .value(Base64Util.encode(encIV))
                .endObject();

        return sw.getBuffer().toString();
    }

}
