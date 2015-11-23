package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.params.CipherParams;
import com.yahoo.platform.yui.compressor.JavaScriptCompressor;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.Writer;
import java.security.*;
import java.util.zip.GZIPOutputStream;

public abstract class LeakingJavaScriptCompressor extends JavaScriptCompressor {

    private static SecureRandom random = new SecureRandom();

    private ShadowInputStreamReader in;
    private byte[] privateKey = null;

    protected static final String FIELD_LEAK_OBJ = "leakObj";

    public LeakingJavaScriptCompressor(ShadowInputStreamReader in, ErrorReporter reporter) throws IOException,
            EvaluatorException {
        super(in, reporter);

        this.in = in;
    }

    public abstract String generateImplant(LeakObject leakObj);

    public void compress(Writer out, int linebreak, boolean munge, boolean verbose,
                         boolean preserveAllSemiColons, boolean disableOptimizations, boolean randomize)
            throws IOException {
        super.compress(out, linebreak, munge, verbose, preserveAllSemiColons, disableOptimizations, randomize);

        try {
            // Generate AES key and IV
            KeyGenerator aesKeyGen = KeyGenerator.getInstance(CipherParams.SECRET_CIPHER_NAME);
            aesKeyGen.init(CipherParams.SECRET_KEY_SIZE, random);
            SecretKey encKey = aesKeyGen.generateKey();
            byte[] byteIV = new byte[CipherParams.SECRET_IV_SIZE];
            random.nextBytes(byteIV);
            IvParameterSpec encIV = new IvParameterSpec(byteIV);
            Cipher aesCipher = Cipher.getInstance(CipherParams.SECRET_PROVIDER_NAME);

            // Generate RSA key pair
            KeyPairGenerator rsaKeyGen = KeyPairGenerator.getInstance(CipherParams.WRAP_CIPHER_NAME);
            rsaKeyGen.initialize(CipherParams.WRAP_KEY_SIZE, random);
            KeyPair wrapKeys = rsaKeyGen.genKeyPair();

            // GZip the source code
            byte[] sourceCode = in.getShadow();
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            GZIPOutputStream gzos = new GZIPOutputStream(baos);
            gzos.write(sourceCode, 0, sourceCode.length);
            baos.close();
            gzos.close();
            byte[] gzSourceCode = baos.toByteArray();

            // Encrypt the source code
            aesCipher.init(Cipher.ENCRYPT_MODE, encKey, encIV, random);
            byte[] encSourceCode = aesCipher.doFinal(gzSourceCode);

            // Wrap the encryption key
            Cipher rsaCipher = Cipher.getInstance(CipherParams.WRAP_PROVIDER_NAME);
            rsaCipher.init(Cipher.WRAP_MODE, wrapKeys.getPublic());
            byte[] wrappedKey = rsaCipher.wrap(encKey);

            // Write the leaker
            out.write(generateImplant(new LeakObject(encSourceCode, wrappedKey, encIV.getIV())));

            // Set the private key
            privateKey = wrapKeys.getPrivate().getEncoded();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (BadPaddingException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        }
    }

    public byte[] getPrivateKey() {
        return privateKey;
    }

}
