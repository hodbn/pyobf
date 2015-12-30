package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.params.CipherParams;
import com.leakingobfuscator.common.utils.GZipUtil;
import com.leakingobfuscator.common.utils.IOUtil;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import java.io.*;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;

public abstract class LeakExtractor {

    protected FileInputStream fisInput;
    protected FileInputStream fisKey;
    protected FileOutputStream fosOutput;

    public LeakExtractor(FileInputStream fisInput, FileInputStream fisKey, FileOutputStream fosOutput) {
        this.fisInput = fisInput;
        this.fisKey = fisKey;
        this.fosOutput = fosOutput;
    }

    public void extract() throws IOException {
        LeakObject leakObj = getLeakObject();
        try {
            // Read privateKey from file
            byte[] privateKeyBytes = IOUtil.readAllBytes(fisKey);
            PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
            KeyFactory rsaKeyFactory = KeyFactory.getInstance(CipherParams.WRAP_CIPHER_NAME);
            PrivateKey privateKey = rsaKeyFactory.generatePrivate(keySpec);

            // Unwrap the wrappedKey to encKey using privateKey
            Cipher rsaCipher = Cipher.getInstance(CipherParams.WRAP_PROVIDER_NAME);
            rsaCipher.init(Cipher.UNWRAP_MODE, privateKey);
            SecretKey encKey = (SecretKey) rsaCipher.unwrap(leakObj.getWrappedKey(),
                    CipherParams.SECRET_CIPHER_NAME, Cipher.SECRET_KEY);

            // Decrypt using encKey and encIV
            Cipher aesCipher = Cipher.getInstance(CipherParams.SECRET_PROVIDER_NAME);
            aesCipher.init(Cipher.DECRYPT_MODE, encKey, new IvParameterSpec(leakObj.getEncIV()));
            byte[] gzSourceCode = aesCipher.doFinal(leakObj.getEncSourceCode());

            // Decompress the GZipped source code
            byte[] sourceCode = GZipUtil.decompress(gzSourceCode);

            IOUtil.writeAllBytes(fosOutput, sourceCode);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (BadPaddingException e) {
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        } catch (InvalidKeySpecException e) {
            e.printStackTrace();
        }
    }

    protected abstract LeakObject getLeakObject();

}
