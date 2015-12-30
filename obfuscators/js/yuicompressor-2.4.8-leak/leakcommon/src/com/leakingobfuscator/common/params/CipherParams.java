package com.leakingobfuscator.common.params;

public class CipherParams {

    public static final String WRAP_CIPHER_NAME = "RSA";
    public static final String WRAP_PROVIDER_NAME = "RSA/ECB/PKCS1Padding";
    public static final int WRAP_KEY_SIZE = 512;

    public static final String SECRET_CIPHER_NAME = "AES";
    public static final String SECRET_PROVIDER_NAME = "AES/CBC/PKCS5PADDING";
    public static final int SECRET_IV_SIZE = 16;
    public static final int SECRET_KEY_SIZE = 128;

}
