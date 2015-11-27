package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;
import com.leakingobfuscator.leaker.templates.ScriptTemplate;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import java.io.*;
import java.util.HashMap;

public class BackdoorLeakingJavaScriptCompressor extends LeakingJavaScriptCompressor {

    private static final String WRAPPER_FN = "back-wrapper.js";

    public BackdoorLeakingJavaScriptCompressor(ShadowInputStreamReader in, ErrorReporter reporter) throws IOException, EvaluatorException {
        super(in, reporter);
    }

    @Override
    public boolean writeLeakingOutput(Writer outWriter, Reader inReader, LeakObject leakObj) {
        try {
            HashMap<String, String> replacements = new HashMap<String, String>();

            ByteArrayOutputStream baosObfCode = new ByteArrayOutputStream();
            OutputStreamWriter oswObfCode = new OutputStreamWriter(baosObfCode);
            IOUtil.copy(inReader, oswObfCode);
            oswObfCode.flush();

            replacements.put("c:" + FIELD_LEAK_OBJ, leakObj.toJSON());
            replacements.put("c:" + FIELD_OBF_CODE, new String(baosObfCode.toByteArray()));

            ScriptTemplate.generate(WRAPPER_FN, outWriter, replacements);

            return true;
        } catch (IOException e) {
            return false;
        }
    }

}
